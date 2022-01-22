# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from sqlalchemy import create_engine, Integer, Column, String, Sequence
from sqlalchemy.orm import declarative_base, sessionmaker

# Database configuration
engine = create_engine('postgresql://postgres:admin123@localhost:5432/api-que', echo=True)
Base = declarative_base()


# DDL - ORM definition
class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, Sequence('seq_task'), primary_key=True)
    name = Column(String)

    def __repr__(self) -> str:
        return "User(id = " + str(self.id) + ", name = " + self.name + ")"


# DDL - database generation based on the code-in definition
Base.metadata.create_all(engine)

# Session configuration
Session = sessionmaker(bind=engine)
session = Session()


# DML
def add():
    session.add(Task(name='Task 1'))
    session.commit()


def print_all():
    print(session.query(Task).filter_by(name='Task 1').first())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
