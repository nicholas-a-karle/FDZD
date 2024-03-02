import warnings


class Conversation:
    def __init__(self):
        self.nodes = []
        self.ptr = 0
    
    class Node:
        def __init__(self, edges, text, commands):
            self.npctext = text
            self.edges = edges
            # commands are executed when a node is visited and when an edge is crossed
            self.commands = commands
    
    class Edge:
        def __init__(self, tonode, text, commands):
            self.tonode = tonode
            self.pctext = text
            # commands are executed when a node is visited and when an edge is crossed
            self.commands = commands

    def add_node(self, text="NPC Dialogue", edges=None, commands=None):
        if commands == None: commands=[]
        if edges == None: edges = []
        self.nodes.append(Conversation.Node(edges, text, commands))

    def add_edge(self, fromnode, tonode, text="Player Dialogue Option", commands=None):
        if commands == None: commands=[]
        self.nodes[fromnode].edges.append(Conversation.Edge(tonode, text, commands))

    # executed relative to current node
    def cross(self, option_index):
        if (option_index >= len(self.nodes[self.ptr].edges)):
            warnings.warn("Warning: Option Index not valid in Conversation graph traversal")
            return -1
        # execute edge commands
        for command in self.nodes[self.ptr].edges[option_index].commands: command()
        # cross the edge
        self.ptr = self.nodes[self.ptr].edges[option_index].tonode
        # execute node commands
        for command in self.nodes[self.ptr].commands: command()

    # return npctext and player options
    def get_text(self):
        return {
            "npctext": self.nodes[self.ptr].npctext,
            "options": [edge.pctext for edge in self.nodes[self.ptr].edges]
        }
    
    # print a diagram of the graph
    def print_graph(self):
        for node in self.nodes:
            print("\t", node.npctext)
            for edge in node.edges:
                print("\t\t", edge.pctext, "\n\t\t   ==>", self.nodes[edge.tonode].npctext)

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