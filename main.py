import tkinter
from constants import *

def tksetup(window_root: tkinter.Tk):
  window_root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
  window_root.title(SCREEN_TITLE)
  window_root.resizable(False, False)
  window_root.configure(background=PRIMARY_COLOR)
  welcome_text = tkinter.Label(window_root, text="Please provide your Steam profile URL", font=(DEFAULT_FONT, DEFAULT_FONT_SIZE))
  welcome_text.pack(pady=TITLE_TEXT_PADDING_Y)
  inputBox = tkinter.Text(window_root, height=1, font=(DEFAULT_FONT, DEFAULT_FONT_SIZE))
  inputBox.pack(padx=int(SCREEN_WIDTH/6))
  button = tkinter.Button(window_root, text="click me", font=('Arial', 18), bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, fg=ACENT_COLOR)
  button.pack()

  window_root.mainloop()


def main():
  window_root = tkinter.Tk()
  tksetup(window_root)

 



if __name__ == "__main__":
  main()
