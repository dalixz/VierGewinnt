import VierGewinnt
from tkinter import *
import random

class VierGewinntWindow:
    def __init__(self, VierGewinntLogic):
        self.logic = VierGewinntLogic
        self.window = None
        self.current_screen_name = None
        #self.default_background_color = "#303030"
        self.yellow = "#faff00"
        self.blue = "#19baff"
        self.holes = []

    def generate_mainloop(self):
        self.window = Tk()
        self.window.title("Vier Gewinnt")
        self.window.geometry("500x300")
        #self.window.tk_setPalette(self.default_background_color)
        self.window.after(10, self.update_screen)
        self.window.mainloop()

    def update_screen(self):
        # timer muss immer wieder neu registriert werden
        self.window.after(10, self.update_screen)

        if not self.logic.get_started() and self.current_screen_name != "startscreen":
            self.current_screen_name = "startscreen"
            self.draw_startscreen()

        if self.logic.get_started() and self.current_screen_name != "gamefield":
            self.current_screen_name = "gamefield"
            self.draw_gamefield()

    def draw_startscreen(self):
        print("drawing startscreen")

        l1 = Label(self.window, text="Vier Gewinnt", font=(None, 32))
        l1.pack()

        self.window.after(500, self.blink_headline, l1)

        Label(self.window, text="v" + VierGewinnt.__version__ + " by " + VierGewinnt.__author__, font=(None, 14)).pack()
        Label(self.window, text="Spielmodus:", font=(None, 12)).pack(pady=20)

        self.play_mode = IntVar(None, 1)

        Radiobutton(self.window, text="2 Spieler", variable=self.play_mode, value=1).pack()
        Radiobutton(self.window, text="Gegen KI", variable=self.play_mode, value=2).pack()

        Button(self.window, text="Spiel starten", command=self.on_startgame_click).pack(pady=40)


    def blink_headline(self, label):
        #aufhören zu blinken wenn startscreen nicht mehr angezeigt wird
        if self.current_screen_name != "startscreen":
            return

        #farbwechsel alle 200 ms
        self.window.after(200, self.blink_headline, label)

        if label.cget("fg") == self.yellow:
            label.config(fg=self.blue)
        else:
            label.config(fg=self.yellow)

    def on_startgame_click(self):
        #Logik starten - use_ki = self.play_mode == 2
        self.logic.start_game(self.play_mode == 2)

    def draw_gamefield(self):
        #Fenster leeren
        self.clear_widgets()

        canvas = Canvas(self.window, width=400, height=400)
        canvas.pack()
        canvas.create_oval(10, 10, 30, 30)

    def clear_widgets(self):
        for widget in self.window.winfo_children():
            widget.destroy()