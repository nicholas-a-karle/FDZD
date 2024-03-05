
game_variables = {
    "tolerance": 0,
    "opinion": 0
}

mod_comms = [
    "ADD", "SUB"
]
chk_comms = [
    "EQS", "GTE", "LTE"
]
game_comms = [
    "END", "GAMEOVER"
]
goto_command = "GOTO"

def modify_variable(value, variable, command = "ADD"):
    if command == "ADD":
        game_variables[variable] += value
    if command == "SUB":
        game_variables[variable] -= value
    else:
        raise NotImplementedError("ERROR: Modification Command", command, "does not exist")

def check_variable(value, variable, command = "EQS"):
    if command == "EQS":
        return value == variable
    elif command == "GTE":
        return value <= variable
    elif command == "LTE":
        return value >= variable
    else:
        raise NotImplementedError("ERROR: Check Command", command, "does not exist")
    
def execute_game_command(command):
    if command == "END":
        command = command
        # TODO: Go to conversation selector
    elif command == "GAMEOVER":
        command = command
        # TODO: Gameover
    else:
        raise NotImplementedError("ERROR: Game State Command", command, "does not exist")