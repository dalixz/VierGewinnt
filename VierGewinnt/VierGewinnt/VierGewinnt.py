import VierGewinntUI
import VierGewinntLogic
import _thread
import time

__author__ = "Oliver Kümmerle & David Lingmann"
__version__ = "0.8.1"

if __name__ == "__main__":
    logic = VierGewinntLogic.MainLogic()

    ui = VierGewinntUI.VierGewinntWindow(logic)
    ui.generate_mainloop()