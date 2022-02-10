import tkinter as tk
from tkinter import filedialog as fd
from turtle import bgcolor
from controler import Learnig, FlashCard


class MainView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.layout_config()
        self.layout()
        self.config_wigets()
        self.card = None

    def button(self, text, bg, fg, cmd=None):
        def on_enter(e):
            nice_button['background'] = bg
            nice_button['foreground'] = fg

        def on_leave(e):
            nice_button['background'] = fg
            nice_button['foreground'] = bg

        nice_button = tk.Button(self.master, text=text, fg=bg, bg=fg,
                                border=0, command=cmd)
        nice_button.bind('<Enter>', on_enter)
        nice_button.bind('<Leave>', on_leave)
        nice_button.pack(expand=True, fill='x', padx=5, pady=5, ipadx=6,
                         ipady=6)
        nice_button.config(font=self.font)

    def layout(self):
        self.master.geometry('350x550+0+0')

        self.button('Losowanie Fiszki', '#ffcc66', '#222', self.get_flash_card)

        self.option_label = tk.Label(self.master, text='Przetłumacz słowo:')
        self.option_label.pack(fill='x', pady=(22, 22))

        self.word_p_label = tk.Label(self.master, text='Wylosuj Fiszkę')
        self.word_p_label.pack(fill='x', pady=(12, 22))

        self.answer = tk.Entry(self.master)
        self.answer.pack(fill='x', pady=(12, 22), ipadx=2, ipady=5,)
        self.answer.bind('<Return>', lambda e: self.check_answer(e))

        self.button('Sprawdź', '#ffcc66', '#222', self.check_answer)

        self.messages = tk.Message(self.master, text=' ')
        self.messages.pack(pady=(2, 2), fill='both')

        self.button('Opcje', '#ffcc66', '#222',
                    lambda: self.open_options(OptionWindow))

    def config_wigets(self):
        self.master.configure(bg='#111', relief='flat', padx=10, pady=10)

        self.option_label.config(**self.options_labels)
        self.word_p_label.config(bg='#111', fg=self.fg, relief='flat',
                                 font=self.font,)
        self.answer.config(bg='#444', fg=self.fg, relief='flat',
                           font=self.font,)
        self.messages.config(**self.options, justify='center')

    def layout_config(self):
        self.master.title('Fiszki')
        self.font = ('raleway', 12)
        self.font_labels = ('raleway', 11)
        self.fg = '#ffcc66'
        self.bg = '#141414'
        self.options = dict(bg=self.bg, fg=self.fg, relief='flat',
                            font=self.font)
        self.options_labels = dict(bg='#111', fg=self.fg, relief='flat',
                                   font=self.font_labels)

    def get_flash_card(self):
        self.card = Learnig()
        word = self.card.show_word()
        self.messages.configure(text=' ')
        print(word)
        self.word_p_label.config(text=word)

    def check_answer(self, event=None):
        if not self.card:
            self.messages.config(text='Najpierw wylosuj fiszkę')
            return 0
        ansewer = self.answer.get()
        self.answer.delete(0, 'end')
        message = self.card.check_result(ansewer)
        self.messages.config(text=message)
        print(ansewer)

    def open_options(self, _class):
        self.new = tk.Toplevel(self.master)
        _class(self.new)

    def do_nothing(self):
        self.master.destroy()
        print('Zrobione coś zanim zostało zamknięte :P')


class OptionWindow(tk.Toplevel):
    def __init__(self, master):
        print(myapp.new.state())
        self.master = master
        self.layout_config()
        self.layout()
        self.config_wigets()
        self.file = tk.StringVar

    def layout(self):
        self.master.geometry('350x550+0+0')

        self.info = '''Dodaj słowo w języku polskim. Automatycznie
        przetłumaczymy te słowo i dodamy do bazy'''

        self.info_label = tk.Message(self.master, text=self.info)
        self.info_label.pack(pady=(22, 22))

        self.word_to_add = tk.Entry(self.master)
        self.word_to_add.pack(pady=(12, 22), ipadx=2, ipady=5,)
        self.word_to_add.bind('<Return>', lambda e: self.save_word(e))

        self.add_button = tk.Button(self.master, text='Dodaj',
                                    command=self.save_word)
        self.add_button.pack(padx=10, pady=10, ipadx=2, ipady=2,)

        self.messages = tk.Message(self.master, text=' ')
        self.messages.pack(pady=(12, 22))

        self.info_2 = '''Możesz także dodać wiele słów naraz wczytaj poniżej
        plik z rozszerzeniem txt, gdzie każdy wyraz będzie
        zapisany w osobnej linii'''

        self.info_2_label = tk.Message(self.master, text=self.info_2)
        self.info_2_label.pack(pady=(22, 22))

        self.add_multi_button = tk.Button(self.master, text='Dodaj wiele',
                                          command=self.batch_save)
        self.add_multi_button.pack(padx=10, pady=10, ipadx=2, ipady=2,)

        self.status_label = tk.Label(self.master, text='')
        self.status_label.pack(pady=(22, 22))

    def config_wigets(self):
        self.master.configure(bg='#333', relief='flat', padx=10, pady=10)
        self.info_label.config(**self.options_labels, width=300,
                               justify='center')
        self.word_to_add.config(**self.options, width=30,)
        self.add_button.config(**self.options, width=30,)
        self.messages.config(bg='#333', fg=self.fg, relief='flat',
                             font=self.font, width=300, justify='center')
        self.info_2_label.config(**self.options_labels, width=300,
                                 justify='center')
        self.add_multi_button.config(**self.options, width=30,)
        self.status_label.config(**self.options_labels, width=30,)

    def layout_config(self):
        self.master.title('Fiszki - opcje')
        self.font = ('helvetica', 12)
        self.font_labels = ('helvetica', 11)
        self.fg = '#f1f1f1'
        self.bg = '#444'
        self.options = dict(bg=self.bg, fg=self.fg,
                            relief='flat', font=self.font)
        self.options_labels = dict(bg='#333', fg=self.fg,
                                   relief='flat', font=self.font_labels)

    def save_word(self, event=None):
        word = self.word_to_add.get()
        message = FlashCard().translate_word(word)
        self.messages.configure(text=message)

    def batch_save(self):
        self.file = fd.askopenfilename()
        info = FlashCard().batch_translate_word(self.file)
        self.status_label.config(text=info)


if __name__ == '__main__':
    root = tk.Tk()
    myapp = MainView(root)
    root.protocol('WM_DELETE_WINDOW', myapp.do_nothing)
    myapp.mainloop()
