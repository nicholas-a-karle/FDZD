import warnings


class Conversation:
    def __init__(self, note=""):
        self.nodes = []
        self.ptr = 0
        self.note = note
    
    class Node:
        def __init__(self, edges, text):
            self.npctext = text
            self.edges = edges
    
    class Edge:
        def __init__(self, tonode, text, commands, checks, game_state):
            self.tonode = tonode
            self.pctext = text
            # commands are executed when a node is visited and when an edge is crossed
            self.commands = commands
            self.checks = checks
            self.game_state = game_state

    def set_note(self, note=""):
        self.note = note

    def add_node(self, text="NPC Dialogue", edges=None):
        if edges == None: edges = []
        self.nodes.append(Conversation.Node(edges, text))

    def add_edge(self, fromnode, tonode, text="Player Dialogue Option", commands=None, checks=None, game_state=None):
        if commands == None: commands=[]
        if checks == None: checks=[]
        if game_state == None: game_state=[]
        self.nodes[fromnode].edges.append(Conversation.Edge(tonode, text, commands, checks, game_state))

    # executed relative to current node
    def cross(self, option_index):
        if (option_index >= len(self.nodes[self.ptr].edges)):
            warnings.warn("Warning: Option Index not valid in Conversation graph traversal")
            return -1
        # execute edge commands
        for command in self.nodes[self.ptr].edges[option_index].commands: command()
        for game_command in self.nomes[self.ptr].edges[option_index].game_state: game_command()
        # cross the edge
        self.ptr = self.nodes[self.ptr].edges[option_index].tonode

    # return npctext and player options
    def get_text(self):
        dialogue = {
            "npctext": self.nodes[self.ptr].npctext,
            "options": []
        }
        for edge in self.nodes[self.ptr].edges:
            checks_met = True
            for check in edge.checks:
                if not check(): 
                    checks_met = False
                    break
            if checks_met:
                dialogue["options"].append(edge.pctext)
        return dialogue
    
    # print a diagram of the graph
    def print_graph(self):
        print("Conversation Diagram__________________________________________|")
        for i in range(len(self.nodes)):
            print("|", str(i), '\"' + self.nodes[i].npctext + '\"')
            for edge in self.nodes[i].edges:
                print("|\t", '\"' + edge.pctext + '\"' + "\tGOTO", edge.tonode, "\t", (len(edge.commands) + len(edge.game_state)) , "COMMANDS,", len(edge.checks), "CHECKS")
        print("_______________________________________________________________")

def print_dialogue(dialogue):
    print("NPC:", dialogue["npctext"])
    for i in range(len(dialogue["options"])):
        print("\t", str(i), dialogue["options"][i])

if __name__ == "__main__":
    c = Conversation()
    c.add_node(text="Hello") # node 0
    c.add_edge(0, 1, text="Hello")
    c.add_edge(0, 2, text="Go Away")
    c.add_edge(0, 3, text="I hate you")
    c.add_edge(0, 3, text="I really more")
    c.add_node(text="How are you?") # node 1
    c.add_edge(1, 4, text="Good")
    c.add_edge(1, 5, text="Bad")
    c.add_node(text="Fine I'll leave") # node 2
    c.add_node(text="What did I do?") # node 3
    c.add_edge(3, 6, text="I'm leaving")
    c.add_node(text="Well, that's good... Anyways, I'll see you!") # node 4
    c.add_node(text="Well, that's not good... Anyways, I'll see you!") # node 5
    c.add_node(text="* he leaves *") # node 6
    print("================================================================================")
    c.print_graph()
    print("================================================================================")
    print_dialogue(c.get_text())
    c.cross(2)
    print_dialogue(c.get_text())
    c.cross(0)
    print_dialogue(c.get_text())
    print("================================================================================")