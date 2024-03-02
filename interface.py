import tkinter as tk

class Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

class StartMenu(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent, controller)
        self.controller = controller

        start_button = tk.Button(self, text="Start Game", command=controller.start_game)
        quit_button = tk.Button(self, text="Quit Game", command=controller.quit_game)

        start_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        quit_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    
class GameFrame(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent, controller)

        quit_button = tk.Button(self, text="Quit Game", command=controller.quit_game)
        quit_button.place(relx=0.95, rely=0.05, anchor=tk.CENTER)

        self.buttons = []
        self.labels = []
        num = len(controller.dialogue)
        for i in range(1, num):
            self.buttons.append(
                tk.Button(self, text=str(i)+".", 
                command=lambda response = i: controller.dialogue_respond(response))
            )
            self.buttons[i-1].place(relx=0.1, rely=0.7 + 0.05 * i)

        if (num > 0):
            self.labels.append(tk.Label(self, text=controller.dialogue[0]))
            self.labels[0].place(relx=0.1, rely=0.6)
        for i in range(1, num):
            self.labels.append(tk.Label(self, text=controller.dialogue[i]))
            self.labels[i].place(relx=0.12, rely=0.7 + 0.05 * i)

    def redraw(self):
        for label in self.labels:
            label.destroy()
        for button in self.buttons:
            button.destroy()
        self.buttons = []
        self.labels = []
        num = len(self.controller.dialogue)
        for i in range(1, num):
            self.buttons.append(
                tk.Button(self, text=str(i)+".", 
                command=lambda response = i: self.controller.dialogue_respond(response))
            )
            self.buttons[i-1].place(relx=0.1, rely=0.7 + 0.05 * i)

        if (num > 0):
            self.labels.append(tk.Label(self, text=self.controller.dialogue[0]))
            self.labels[0].place(relx=0.1, rely=0.6)
        for i in range(1, num):
            self.labels.append(tk.Label(self, text=self.controller.dialogue[i]))
            self.labels[i].place(relx=0.12, rely=0.7 + 0.05 * i)
    
class GameMenu(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent, controller)

class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("FriendZoneD")
        self.attributes("-fullscreen", True)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.dialogue=[
            "Test Dialogue 1",
            "Go to 1",
            "Go to 2",
            "Go to 3"
            ]
        
        self.frames={}
        for f in (StartMenu, GameFrame, GameMenu):
            page_name = f.__name__
            frame = f(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_page("StartMenu")

    def show_page(self, page):
        frame = self.frames[page]
        frame.tkraise()

    def quit_game(self):
        self.quit()
        return 0

    def start_game(self):
        self.show_page("GameFrame")
        return -1
    
    def dialogue_respond(self, response_index):
        print(response_index)
        if response_index == 1:
            self.dialogue[0] = "Test Dialogue 1"
        elif response_index == 2:
            self.dialogue[0] = "Test Dialogue 2"
        elif response_index == 3:
            self.dialogue[0] = "Test Dialogue 3"
        self.frames["GameFrame"].redraw()

    def init_menu(self):
        # TODO: Do this
        return -1

    def run(self):
        self.mainloop()
        return 0

if __name__ == "__main__":
    window = Window()
    window.run()