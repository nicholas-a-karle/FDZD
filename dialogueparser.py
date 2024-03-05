
from conversation import Conversation
import re
import warnings
import gamevariables

# two functions need to be ran
# Conversation.add_node(text="npc_dialogue")
# Conversation.add_edge(fromnode, tonode, text="dialogue_option", commands, checks)

# text format
"""
[npc_dialogue, string]
[\t]|[\s\s+][dialogue_option, string]\s*(optionals)

optionals:
goto [tonode, int]
[var, variable name][+ or -][change, int] <= commands
[var, variable name][> or <][threshold, int] <= checks
"""

# NOTE: All of this can be run, then commands and checks added in after the processing of the file

# KEYWORDS
keys = gamevariables.mod_comms.copy()
keys.extend(gamevariables.chk_comms)
keys.extend(gamevariables.game_comms)
keys.append(gamevariables.goto_command)


def check_if_comment(line):
    if len(line.strip()) < 1: return True
    return line.strip()[0] == '#'

def check_if_note(line):
    return line.strip()[0] == '!'

def check_syntax(line):
    return True

def parse_node_line(line):
    # very simple, woohoo
    return str(line).strip()

def parse_edge_line(line, node):

    print("|____________________________________")

    line = str(line).strip()

    # variable known from previous lines
    fromnode = node
    # variables to be filled
    tonode = -1
    text = ""
    commands = None
    checks = None 

    key_indices = [line.find(key) if key in line else None for key in keys]
    i = 0
    while i < len(key_indices):
        if key_indices[i] == None:
            key_indices.pop(i)
        else: i += 1

    if len(key_indices) == 0: first_command = len(line)
    else: first_command = min(key_indices)

    print("FULL_LINE: \"" + line + "\"")

    text = line[0: first_command].strip()
    line = line[first_command:]
    commands = []
    last_pop = 0

    print("COMMANDS: \"" + line + "\"")

    for i in range(5, len(line)):
        #print(line[i])
        if line[i-3: i] in keys and i > 4:
            print("app1", line[last_pop: i-3].strip())
            commands.append(line[last_pop: i-3].strip())
            last_pop = i-3
        elif line[i-4: i] in keys:
            print("app2", line[last_pop: i-4].strip())
            commands.append(line[last_pop: i-4].strip())
            last_pop = i-4
    print("endapp", line[last_pop:].strip())
    commands.append(line[last_pop:].strip())

    
    print("TEXT: \"" + text + "\"\nALL_COMMANDS:\n", commands)
    print()

    game_state = []
    checks = []
    i = 0
    while i < len(commands):
        is_game_key = False
        for key in gamevariables.game_comms: 
            if key in commands[i]: 
                is_game_key = True
                break
        is_check_key = False
        for key in gamevariables.chk_comms:
            if key in commands[i]:
                is_check_key = True
                break
        is_goto_key = gamevariables.goto_command in commands[i]

        if is_game_key:
            game_state.append(commands.pop(i))
        elif is_check_key:
            checks.append(commands.pop(i))
        elif is_goto_key:
            goto = commands.pop(i)
        else: i += 1

    
    print("TEXT:", text,"\nGAME STATE:\n", game_state, "\nCOMMANDS:\n", commands, "\nREQS:\n", checks)
    
    tonode = process_goto_command(goto)
    game_state = process_game_commands(game_state)
    commands = process_commands(commands)
    checks = process_checks(checks)

    return (fromnode, tonode, text, commands, checks, game_state)

def process_goto_command(goto):
    print("GOTO_COMMAND:", goto)
    return int(goto.replace(gamevariables.goto_command, "").strip())

def process_game_commands(game_state):
    for i in range(len(game_state)):
        game_state[i] = game_state[i].strip()
        game_state[i] = lambda comm = game_state[i]: gamevariables.execute_game_command(comm)
    return game_state

def process_commands(commands):
    for  i in range(len(commands)):
        commands[i] = process_command(commands[i])
        commands[i] = lambda comm = commands[i][0], val = int(commands[i][1]), var = commands[i][2]: gamevariables.modify_variable(val, var, command=comm)
    return commands

def process_command(command):
    #print("Processing:", command)
    command = command.split(" ")
    #print("Into:", command)
    split = ["", "", ""]
    for part in command:
        if part.isalpha():
            if part.isupper():
                split[0] = part
            elif part.islower():
                split[2] = part
        elif part.isdigit():
            split[1] = part
    return split
    

def process_checks(checks):
    for  i in range(len(checks)):
        checks[i] = process_check(checks[i])
        checks[i] = lambda comm = checks[i][0], val = int(checks[i][1]), var = checks[i][2]: gamevariables.check_variable(val, var, check=comm)
    return checks

def process_check(check):
    #print("Processing:", check)
    check = check.split(" ")
    #print("\tInto:", check)
    split = ["", "", ""]
    for part in check:
    #    print("\tFound part \"" + part + "\"")
        if part.isalpha():
            if part.isupper():
    #            print("\t\tClassified as COMMAND")
                split[0] = part
            elif part.islower():
    #            print("\t\tClassified as VARIABLE")
                split[2] = part
        elif part.isdigit():
    #        print("\t\tClassified as NUMERIC")
            split[1] = part
    #print("\tSplit:", split)
    return split

# Process a filepath into a Conversation object
def process(filepath):
    # check that filepath is a string
    try:
        filepath = str(filepath)
    except Exception as e:
        print(e)
        return -1
    
    c = Conversation()
    line_number = 0
    cur_node = -1 # must start here
    with open(filepath) as file:
        for line in file:
            line_number += 1
            if check_if_comment(line): continue
            if check_if_note(line):
                # add to conversation notes, only the last note counts
                c.set_note(line)
            if not check_syntax(line):
                raise SyntaxError("Syntax Error at Line", line_number)
            # line length should be > 1
            if line[0] == "\t" or (len(line) >= 2 and line[0] == ' ' and line[1] == ' '):
                # edge
                edge_data = parse_edge_line(line, cur_node)
                # returns: (fromnode, tonode, text, commands, checks)
                # Conversation.add_edge(fromnode, tonode, text, commands, checks)
                c.add_edge(
                    edge_data[0], edge_data[1],
                    text=edge_data[2],
                    commands=edge_data[3],
                    checks=edge_data[4]
                )

            else:
                # node
                node_text = parse_node_line(line)
                c.add_node(text=node_text)
                cur_node += 1

    return c


if __name__ == "__main__":
    c = process("fileformatexample.txt")
    c.print_graph()
