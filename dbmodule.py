# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from sqlalchemy import create_engine, Integer, Column, String, Sequence, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Database configuration
engine = create_engine('postgresql://postgres:admin123@localhost:5432/api-que', echo=True)
Base = declarative_base()


# DDL - ORM definition
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, Sequence('seq_user'), primary_key=True)
    name = Column(String)
    surname = Column(String)
    e_mail = Column(String)
    registration_date = Column(DateTime)
    expiration_date = Column(DateTime)
    api_token = Column(String)

    def __repr__(self) -> str:
        return "User(id = " + str(self.id) + ", name = " + self.name + ", surname = " + self.surname \
               + ", e_mail = " + self.e_mail + ", registration_date = " + self.registration_date + \
               ", expiration_date = " + self.expiration_date + ", api_token = " + self.api_token + ")"


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, Sequence('seq_task'), primary_key=True)
    creation_date = Column(DateTime)
    finish_date = Column(DateTime)
    population_processed_failed = Column(Integer)
    population_processed_success = Column(Integer)
    population_size = Column(Integer)
    status = Column(String)
    id_user = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")


class TaskParameter(Base):
    __tablename__ = 'task_parameter'

    id = Column(Integer, Sequence('seq_task_parameter'), primary_key=True)
    location = Column(String)
    condition = Column(String)
    antecedent = Column(Integer, ForeignKey('task_parameter.id'))
    task_parameter = relationship("TaskParameter")
    id_task = Column(Integer, ForeignKey('task.id'))
    task = relationship("Task")


class SubTask(Base):
    __tablename__ = 'sub_task'

    id = Column(Integer, Sequence('seq_sub_task'), primary_key=True)
    creation_date = Column(DateTime)
    finish_date = Column(DateTime)
    remark = Column(String)
    number_of_probes = Column(Integer)
    id_task_parameter = Column(Integer, ForeignKey('task_parameter.id'))
    task_parameter = relationship("TaskParameter")
    id_task = Column(Integer, ForeignKey('task.id'))
    task = relationship("Task")


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

