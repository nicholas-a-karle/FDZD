import tkinter as tk
import tkinter.font as font
from pathlib import Path
from PIL import Image, ImageTk

class Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

class StartMenu(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent, controller)

        sh = controller.winfo_screenheight() / 10
        sw = controller.winfo_screenwidth() / 10

        border_label = tk.Label(self, image = self.controller.border_photo)
        border_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        border_label.image=controller.border_photo

        start_button = tk.Button(self, text="Start Game", command=controller.start_game, width = int(sw * 0.15), height = int(sh * 0.04))
        quit_button = tk.Button(self, text="Quit Game", command=controller.quit_game, width = int(sw * 0.15), height = int(sh * 0.04))

        start_button.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
        quit_button.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

        title_label = tk.Label(self, text="FrienDZoneD", font=font.Font(family="Helvetica", size=45, weight="bold", underline=True))
        title_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        

    
class GameFrame(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent, controller)

        sh = controller.winfo_screenheight()
        sw = controller.winfo_screenwidth()

        self.quit_button = tk.Button(self, text="Quit Game", command=controller.quit_game, width = int(sw * 0.006), height = int(sh * 0.0015))
        self.menu_button = tk.Button(self, text="Menu", command=controller.open_game_menu)

        self.border_label = tk.Label(self, image = controller.border_photo)
        self.border_label.image=controller.border_photo

        self.buttons = []
        self.labels = []
        self.redraw()
        
    def redraw(self):
        for label in self.labels:
            label.destroy()
        for button in self.buttons:
            button.destroy()
        self.buttons = []
        self.labels = []

        sh = self.controller.winfo_screenheight()
        sw = self.controller.winfo_screenwidth()
        image_width = int(sw * 0.8)
        image_height = int(sh * 0.5)

        num = len(self.controller.dialogue["options"])
        for i in range(num):
            self.buttons.append(
                tk.Button(self, text=self.controller.dialogue["options"][i],
                command=lambda response = i: self.controller.dialogue_respond(response)
                )
            )
            self.buttons[i].place(relx=0.12, rely=0.7 + 0.04 * i)


        self.labels.append(tk.Label(self, text=self.controller.dialogue["npctext"]))
        self.labels[0].place(relx=0.14, rely=0.65, anchor=tk.CENTER)
        
        self.border_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.quit_button.place(relx=0.75, rely=0.9, anchor=tk.CENTER)
        self.menu_button.place(relx=0.25, rely=0.9, anchor=tk.CENTER)
        self.menu_button.lift()
        self.quit_button.lift()
        
        
        
    
class GameMenu(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent, controller)
        self.controller = controller

        sh = controller.winfo_screenheight() / 10
        sw = controller.winfo_screenwidth() / 10

        border_label = tk.Label(self, image = self.controller.border_photo)
        border_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        border_label.image=controller.border_photo

        resume_button = tk.Button(self, text="Resume", command=controller.start_game, width = int(sw * 0.15), height = int(sh * 0.04))
        start_button = tk.Button(self, text="Exit to Menu", command=controller.start_menu, width = int(sw * 0.15), height = int(sh * 0.04))
        quit_button = tk.Button(self, text="Quit Game", command=controller.quit_game, width = int(sw * 0.15), height = int(sh * 0.04))

        resume_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        quit_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)


class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("FriendZoneD")
        self.attributes("-fullscreen", True)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.border_photo = Image.open("resources/border.png")
        self.border_photo = self.border_photo.resize((int(self.winfo_screenwidth()), int(self.winfo_screenheight())), Image.Resampling.BICUBIC)
        self.border_photo = ImageTk.PhotoImage(self.border_photo)

        self.dialogue={
            "npctext": "Test Dialogue 1",
            "options": ["Go to 1", "Go to 2", "Go to 3"]
        }

        self.bind("<Escape>", self.esc_game)
        
        self.frames={}
        for f in (StartMenu, GameFrame, GameMenu):
            page_name = f.__name__
            frame = f(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.start_menu()

    def show_page(self, page):
        frame = self.frames[page]
        frame.tkraise()

    def quit_game(self):
        self.quit()
        return 0
    
    def esc_game(self, event):
        self.quit()
        return event
    
    def start_menu(self):
        self.show_page("StartMenu")

    def open_game_menu(self):
        self.show_page("GameMenu")

    def start_game(self):
        self.show_page("GameFrame")
    
    def dialogue_respond(self, response_index):
        print(response_index)
        if response_index == 0:
            self.dialogue["npctext"] = "Test Dialogue 1"
        elif response_index == 1:
            self.dialogue["npctext"] = "Test Dialogue 2"
        elif response_index == 2:
            self.dialogue["npctext"] = "Test Dialogue 3"
        self.frames["GameFrame"].redraw()

    def run(self):
        if Path("resources/coconut.jpg").exists():
            self.mainloop()
        return 0

if __name__ == "__main__":
    window = Window()
    window.run()