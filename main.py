import tkinter as tk
from tkinter import filedialog as fd
from turtle import bgcolor
from controler import Learnig, CardRepo


class Btn:

    @staticmethod
    def button(root, text, bg, fg, cmd=None):
        def on_enter(e):
            nice_button['background'] = bg
            nice_button['foreground'] = fg

        def on_leave(e):
            nice_button['background'] = fg
            nice_button['foreground'] = bg

        nice_button = tk.Button(root, text=text, fg=bg, bg=fg,
                                border=0, command=cmd)
        nice_button.bind('<Enter>', on_enter)
        nice_button.bind('<Leave>', on_leave)
        nice_button.pack(fill='x', ipady=5)
        nice_button.config(font='haveltica')


class MainView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.layout_config()
        self.layout()
        self.config_wigets()
        self.get_flash_card()

    def layout(self):
        self.master.geometry('350x550+0+0')
        self.option_label = tk.Label(self.master, text='Przetłumacz słowo:')
        self.option_label.pack(fill='x', pady=(2, 2))
        self.word_p_label = tk.Label(self.master, text='Wylosuj Fiszkę')
        self.word_p_label.pack(fill='x', pady=(2, 2))
        self.answer = tk.Entry(self.master)
        self.answer.pack(fill='x', pady=(12, 2), ipadx=2, ipady=5,)
        self.answer.bind('<Return>', lambda e: self.check_answer(e))
        Btn.button(self.master, 'Sprawdź', '#ffcc66', '#222',
                   self.check_answer)
        Btn.button(self.master, 'Kolejna Fiszka', '#ffcc66', '#222',
                   self.get_flash_card)
        self.messages = tk.Message(self.master, text=' ')
        self.messages.pack(ipadx=1, ipady=5, pady=50,  fill='both')
        Btn.button(self.master, 'Opcje', '#ffcc66', '#222',
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
        self.card = Learnig.from_repo()
        if not self.card:
            self.word_p_label.config(text='Brak słów w bazie')
            return 0
        word = self.card.show_word()
        self.messages.configure(text=' ')
        self.word_p_label.config(text=word)
        return self.card

    def check_answer(self, event=None):
        if not self.card:
            self.messages.config(text='Najpierw wylosuj fiszkę')
            return 0
        ansewer = self.answer.get()
        self.answer.delete(0, 'end')
        message = self.card.check_result(ansewer)
        self.messages.config(text=message)

    def open_options(self, _class):
        self.new = tk.Toplevel(self.master)
        _class(self.new)

    def do_nothing(self):
        self.master.destroy()


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
        self.word_to_add.pack(fill='x', pady=(12, 22), ipadx=2, ipady=5,)
        self.word_to_add.bind('<Return>', lambda e: self.save_word(e))

        Btn.button(self.master, 'Dodaj', '#ffcc66', '#222', self.save_word)

        self.messages = tk.Message(self.master, text=' ')
        self.messages.pack(fill='x', pady=(12, 22))

        self.info_2 = '''Możesz także dodać wiele słów naraz wczytaj poniżej
        plik z rozszerzeniem txt, gdzie każdy wyraz będzie
        zapisany w osobnej linii'''

        self.info_2_label = tk.Message(self.master, text=self.info_2)
        self.info_2_label.pack(pady=(22, 22))

        Btn.button(self.master, 'Dodaj wiele', '#ffcc66', '#222',
                   self.batch_save)

        self.status_label = tk.Label(self.master, text='')
        self.status_label.pack(fill='x', pady=(22, 22))

    def config_wigets(self):
        self.master.configure(bg='#111', relief='flat', padx=10, pady=10)
        self.info_label.config(**self.options_labels, width=300,
                               justify='center')
        self.word_to_add.config(bg='#444', fg=self.fg, relief='flat',
                                font=self.font,)

        self.messages.config(bg='#333', fg=self.fg, relief='flat',
                             font=self.font, width=300, justify='center')
        self.info_2_label.config(**self.options_labels, width=300,
                                 justify='center')

        self.status_label.config(**self.options_labels, width=30,)

    def layout_config(self):
        self.master.title('Fiszki-opcje')
        self.font = ('raleway', 12)
        self.font_labels = ('raleway', 11)
        self.fg = '#ffcc66'
        self.bg = '#141414'
        self.options = dict(bg=self.bg, fg=self.fg, relief='flat',
                            font=self.font)
        self.options_labels = dict(bg='#111', fg=self.fg, relief='flat',
                                   font=self.font_labels)

    def save_word(self, event=None):
        try:
            word = self.word_to_add.get()
            message = CardRepo.translate_word(word)
            self.messages.configure(text=message)
        except TypeError as e:
            print(e)
            self.messages.configure(text='Jakaś lipa - nie ma słowa?')

    def batch_save(self):
        self.file = fd.askopenfilename()
        print(self.file)
        info = CardRepo.batch_translate_word(self.file)
        self.status_label.config(text=info)


if __name__ == '__main__':
    root = tk.Tk()
    myapp = MainView(root)
    root.protocol('WM_DELETE_WINDOW', myapp.do_nothing)
    myapp.mainloop()
