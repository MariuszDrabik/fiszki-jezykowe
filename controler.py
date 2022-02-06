from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(f'sqlite:///database/word.db')


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
                f"próby='{self.trials}')>")


if __name__ == '__main__':
    Base.metadata.create_all(engine) 
    
    Session = sessionmaker(bind=engine)
    
    session = Session()

    word = Word(en_word='cat', pl_word='kot')
    session.add(word)
    session.commit()
    print(word)
