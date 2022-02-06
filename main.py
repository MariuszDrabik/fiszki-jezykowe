import tkinter as tk


class MainView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.layout_config()
        self.layout()
        self.config_wigets()

    def layout(self):
        self.master.geometry('600x450+0+0')
        self.master.grid()
        self.master.grid_columnconfigure((0, 1, ), weight=1)

        self.option_label = tk.Label(self.master, text='Przetłumacz słowo:')
        self.option_label.grid(row=1, column=0, padx=0, ipadx=0, pady=(22, 2))

        self.word_p_label = tk.Label(self.master, text='Wylosowane słowo')
        self.word_p_label.grid(row=2, column=0, padx=0, ipadx=0, pady=(2, 2))

        self.add_project_entry = tk.Entry(self.master)
        self.add_project_entry.grid(row=2, column=1, padx=2, ipadx=2, ipady=5,)

        self.add_button = tk.Button(self.master, text='Sprawdź',
                                    command=self.place_holder)
        self.add_button.grid(row=3, padx=10, pady=10, ipadx=2, ipady=2,
                             column=0, columnspan=2)

    def config_wigets(self):
        self.master.configure(bg='#333', relief='flat', padx=10, pady=10)

        self.option_label.config(**self.options_labels, width=15,)
        self.word_p_label.config(bg='#333', fg=self.fg, relief='flat',
                                 font=self.font, width=15,)

        self.add_project_entry.config(**self.options, width=29,)
        self.add_button.config(**self.options, width=25,)

    def layout_config(self):
        self.master.title('Fiszki')

        self.font = ('helvetica', 12)
        self.font_labels = ('helvetica', 11, 'italic')
        self.fg = '#f1f1f1'
        self.bg = '#444'
        self.options = dict(bg=self.bg, fg=self.fg,
                            relief='flat', font=self.font)
        self.options_labels = dict(bg='#333', fg=self.fg,
                                   relief='flat', font=self.font_labels)

    def place_holder(self):
        pass

    def do_nothing(self):
        self.master.destroy()
        print('Zrobione coś zanim zostało zamknięte :P')


if __name__ == '__main__':
    root = tk.Tk()
    myapp = MainView(root)
    root.protocol('WM_DELETE_WINDOW', myapp.do_nothing)
    myapp.mainloop()
