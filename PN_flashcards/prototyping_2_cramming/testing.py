import tkinter as tk
from tkinter import ttk

class MyTab(ttk.Frame):
    """Frame to be added to each tab of the notebook.

    """

    def __init__(self, master, idx, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._button = ttk.Button(self, text='Tab {}'.format(idx),
                                  command=lambda *args, x=idx: self._handle_button(x, *args),
                                  underline=0)
        self.bind('<space>', lambda *args, x=idx: self._handle_button(x, *args))
        self._button.pack()
        self.pack()


    def _handle_button(self, x, *args):
        print('Button: Tab {}'.format(x))



class MainWdw(ttk.Frame):
    """Main application window.

    """

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._nb = ttk.Notebook(self)

        # Generate several tabs and add a MyTab object to each.
        self._tabs = []
        for x in range(1, 6):
            t = MyTab(self, x)
            self._tabs.append(t)
            self._nb.add(t, text='Tab {}'.format(x))

        self._nb.pack(expand=1, fill='both')
        master.title('Sample')
        self.pack(expand=1, fill='both', padx=2, pady=2)



def main():
    root = tk.Tk()
    app = MainWdw(root)
    root.mainloop()

main()