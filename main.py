from cmath import inf
import tkinter as tk
from tkinter import filedialog as fd
from controler import Learnig, FlashCard


class MainView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.layout_config()
        self.layout()
        self.config_wigets()
        self.card = None

    def layout(self):
        self.master.geometry('350x550+0+0')
        # self.master.pack()
        # self.master.grid_columnconfigure((0, 1, ), weight=1)

        self.get_word = tk.Button(self.master, text='Losuj fiszkę',
                                  command=self.get_flash_card)
        self.get_word.pack(padx=10, pady=10, ipadx=2, ipady=2,)

        self.option_label = tk.Label(self.master, text='Przetłumacz słowo:')
        self.option_label.pack(pady=(22, 22))

        self.word_p_label = tk.Label(self.master, text='Wylosowane słowo')
        self.word_p_label.pack(pady=(12, 22))

        self.answer = tk.Entry(self.master)
        self.answer.pack(pady=(12, 22), ipadx=2, ipady=5,)
        self.answer.bind('<Return>', lambda e: self.check_answer(e))

        self.check_button = tk.Button(self.master, text='Sprawdź',
                                    command=self.check_answer)
        self.check_button.pack(padx=10, pady=10, ipadx=2, ipady=2,)
        
        self.messages = tk.Message(self.master, text=' ')
        self.messages.pack(pady=(12, 22))

        self.option = tk.Button(self.master, text='Opcje',
                                command=lambda: self.open_options(OptionWindow))
        self.option.pack(padx=10, pady=10, ipadx=2, ipady=2,)

    def config_wigets(self):
        self.master.configure(bg='#111', relief='flat', padx=10, pady=10)
        self.get_word.config(**self.options, width=30,)
        self.option_label.config(**self.options_labels, width=30,)
        self.word_p_label.config(bg='#111', fg=self.fg, relief='flat',
                                 font=self.font, width=30,)
        self.answer.config(**self.options, width=30,)
        self.check_button.config(**self.options, width=30,)
        self.messages.config(bg='#111', fg=self.fg, relief='flat',
                             font=self.font, width=300, justify='center')
        self.option.config(**self.options, width=30,)

    def layout_config(self):
        self.master.title('Fiszki')

        self.font = ('helvetica', 12)
        self.font_labels = ('helvetica', 11)
        self.fg = '#f1f1f1'
        self.bg = '#444'
        self.options = dict(bg=self.bg, fg=self.fg,
                            relief='flat', font=self.font)
        self.options_labels = dict(bg='#111', fg=self.fg,
                                   relief='flat', font=self.font_labels)

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

        self.info = "Dodaj słowo w języku polskim. Automatycznie przetłumaczymy te słowo i dodamy do bazy"

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

        self.info_2 = '''Możesz także dodać wiele słów naraz wczytaj poniżej plik z rozszerzeniem txt, gdzie każdy wyraz będzie zapisany w osobnej linii'''

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
