from http.client import NETWORK_AUTHENTICATION_REQUIRED
from msilib.schema import Error
from googletrans import Translator
from sqlalchemy import create_engine, select, true, update, insert
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from random import randint

Base = declarative_base()


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    en_word = Column(String(50))
    pl_word = Column(String(50))
    trials = Column(Integer, default=0)
    known = Column(Boolean, default=False)

    def __repr__(self):
        return (f"<User(en='{self.en_word}', pl='{self.pl_word}',"
                f"próby='{self.trials}', {self.known})>")

    def get_tuple(self):
        return (self.id, self.en_word, self.pl_word, self.trials)


class Conection:

    def session_maker(self):
        engine = create_engine(f'sqlite:///database/word.db')
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)
        return session()


class FlashCard:

    def save_new_card(self, en_word, pl_word):
        with Conection().session_maker() as s:
            statement = insert(Word).values(en_word=en_word, pl_word=pl_word)
            s.execute(statement)
            s.commit()
        return f'Zapisano parę:\n{pl_word} - {en_word}'

    def get_unknown_words(self):
        with Conection().session_maker() as s:
            statement = select(Word).filter_by(known=False)
            result = s.execute(statement).all()
            return result

    def check_if_exists(self, word):
        with Conection().session_maker() as s:
            statement = select(Word).filter_by(pl_word=word)
            result = s.execute(statement).all()
            if result:
                return 1
            return 0

    def update_word(self, word, known=False):
        word_id = word.id
        trials = word.trials
        with Conection().session_maker() as s:
            statement = update(Word).where(Word.id == word_id).\
                values(trials=trials, known=known)
            s.execute(statement)
            s.commit()

    def translate_word(self, word):
        if not self.check_if_exists(word):
            translator = Translator()
            translation = translator.translate(word, src="pl", dest="en")
            save = self.save_new_card(translation.text.lower(), word.lower())
            return save
        return 'Te słowo istnieje już w bazie'

    def batch_translate_word(self, file):
        try:
            with open(file, 'r', encoding='utf-8') as file:
                for word in file:
                    word = word.strip()
                    self.translate_word(word)
        except Error as e:
            print('Coś poszło nie tak', e)
            return 'Nie zapisano'
        return 'Zapisano'


class Learnig:
    def __init__(self):
        self.word = self.random_word()

    def random_word(self) -> Word:
        words = FlashCard().get_unknown_words()
        amount = len(words)-1
        try:
            if amount <= 1:
                print(words)
                word = words[0]
                self.word = word[0]
                return self.word
        except IndexError as e:
            print('Brak słów w bazie', e)
            return -1
        number = randint(0, amount)
        word = words[number]
        self.word = word[0]
        return self.word

    def show_word(self):
        word = self.word.pl_word
        return word

    def check_result(self, word):
        if word.lower() == self.word.en_word.lower():
            self.word.trials += 1
            if self.word.trials == 10:
                self.word.known = True
                FlashCard().update_word(self.word, known=self.word.known)
                return 'Super słowo zapamiętane'
            FlashCard().update_word(self.word)
            return 'Brawo udało się zgadnąć słowo'
        else:
            return (f'Nie udało się słowo\n{self.word.pl_word}\n'
                    f'w języku angielskim to:\n{self.word.en_word}')


if __name__ == '__main__':
    translator = Translator()
    translation = translator.translate("Czeremcha", src='pl')
    print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
