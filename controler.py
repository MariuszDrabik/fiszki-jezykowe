from googletrans import Translator
from sqlalchemy import create_engine, select, true, update, insert
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from random import randint

Base = declarative_base()
engine = create_engine(f'sqlite:///database/word.db')
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    en_word = Column(String(50))
    pl_word = Column(String(50))
    trials = Column(Integer, default=0)
    known = Column(Boolean, default=False)

    def __repr__(self):
        return (f"User(en_word='{self.en_word}', pl_word='{self.pl_word}',"
                f"trials='{self.trials}', known={self.known})")

    def __str__(self):
        return f"{self.id} {self.en_word} {self.pl_word} {self.trials}"


class CardRepo:  # flascards repo

    @staticmethod
    def save_new_card(en_word, pl_word):
        with session() as s:
            statement = insert(Word).values(en_word=en_word, pl_word=pl_word)
            s.execute(statement)
            s.commit()
        return f'Zapisano parę:\n{pl_word} - {en_word}'

    @staticmethod
    def get_all_words():
        with session() as s:
            statement = select(Word).filter_by(known=False)
            result = s.execute(statement).all()
            return result

    @staticmethod
    def random_word():
        words = CardRepo.get_all_words()
        amount = len(words)-1
        if amount == 0:
            word = None
            print('Brak słów w bazie')
            return word
        number = randint(0, amount)
        word = words[number]
        return word[0]

    @staticmethod
    def get_word(word):
        with session() as s:
            statement = select(Word).filter_by(pl_word=word)
            result = s.execute(statement).all()
            return result

    @staticmethod
    def update_word(word, known=False):
        word_id = word.id
        trials = word.trials
        with session() as s:
            statement = update(Word).where(Word.id == word_id).\
                values(trials=trials, known=known)
            s.execute(statement)
            s.commit()

    @staticmethod
    def translate_word(word):
        if not CardRepo.get_word(word):
            translator = Translator()
            translation = translator.translate(word, src="pl", dest="en")
            save = CardRepo.save_new_card(translation.text.lower(),
                                          word.lower())
            return save
        return 'Te słowo istnieje już w bazie'

    @staticmethod
    def batch_translate_word(file):
        try:
            with open(file, 'r', encoding='utf-8') as file:
                for word in file:
                    word = word.strip()
                    CardRepo.translate_word(word)
        except ValueError as e:
            print('Coś poszło nie tak', e)
            return 'Nie zapisano'
        return 'Zapisano'


class Learnig:

    def __init__(self, word: Word):
        self.word = word

    @classmethod
    def from_repo(cls):
        word = CardRepo.random_word()
        return cls(word)

    def show_word(self):
        word = self.word.pl_word
        return word

    def check_result(self, word):
        if word.lower() == self.word.en_word.lower():
            self.word.trials += 1
            if self.word.trials == 10:
                self.word.known = True
                CardRepo.update_word(self.word, known=self.word.known)
                return 'Super słowo zapamiętane'
            CardRepo.update_word(self.word)
            return 'Brawo udało się zgadnąć słowo'
        else:
            return (f'Nie udało się słowo\n{self.word.pl_word}\n'
                    f'w języku angielskim to:\n{self.word.en_word}')
