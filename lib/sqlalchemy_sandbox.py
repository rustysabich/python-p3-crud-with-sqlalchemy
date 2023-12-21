#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    
    Index('index_name', 'name')

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())
    
    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}, " \
            + f"Grade {self.grade}"

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    
    ## Create Records ##
    
    Session = sessionmaker(bind=engine)
    session = Session()

    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        ),
    )
    
    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )

    # session.add(albert_einstein)
    session.bulk_save_objects([albert_einstein, alan_turing])
    session.commit()
    
    ## Read Records ##
    # 1. Method 1
    # students = session.query(Student)
    # print([student for student in students])
    
    # 2. Method 2
    students = session.query(Student).all()
    print(students)
    
    ## Selecting Only Certain Columns ##
    names = session.query(Student.name).all()
    print(names)
    
    ## Ordering ##
    # 1. Method 1: Plainly by a column name
    students_by_name = session.query(
            Student.name).order_by(
            Student.name).all()

    print(students_by_name)
    
    # 2. Method 2: Descending order
    students_by_grade_desc = session.query(
            Student.name, Student.grade).order_by(
            desc(Student.grade)).all()

    print(students_by_grade_desc)
    
    ## Limiting ##
    # 1. Method 1: Using limit(1)
    oldest_student = session.query(
            Student.name, Student.birthday).order_by(
            Student.birthday).limit(1).all()

    print(oldest_student)
    
    # 2. Method 2: Using first()
    oldest_student = session.query(
            Student.name, Student.birthday).order_by(
            Student.birthday).first()

    print(oldest_student)
    
    ## func: For SQL operations
    student_count = session.query(func.count(Student.id)).first()
    print(f"Student count: {student_count}")
    
    ## Filtering ##
    # A typical filter() statement has a column, a standard operator, and a value
    # Note: Chain multiple filter() statements using comma
    query = session.query(Student).filter(Student.name.like('%Alan%'),
        Student.grade == 11).all()

    for record in query:
        print(f"Filtered name {record.id}: {record.name}")
        
    ## Updating Data ##
    # 1. Method 1: Using Python to modify object and commit
    for student in session.query(Student):
        student.grade += 1

    session.commit()

    print([(student.name,
        student.grade) for student in session.query(Student)])
    
    # 2. Method 2: update() method 
    # Allows us to update records without creating objects beforehand
    session.query(Student).update({
        Student.grade: Student.grade + 1
    })

    print([(
        student.name,
        student.grade
    ) for student in session.query(Student)])
    
    ## Deleting Data ##
    # 1. Method 1: Calling delete() on an object
    query = session.query(
        Student).filter(
            Student.name == "Albert Einstein")

    # retrieve first matching record as object
    albert_einstein = query.first()

    # delete record
    session.delete(albert_einstein)
    session.commit()

    # try to retrieve deleted record
    albert_einstein = query.first()

    print(albert_einstein)
    
    # 2. Method 2: Calling delete() from a query
    # Note: Deletes all records returned by a query
    query = session.query(
        Student).filter(
            Student.name == "Albert Einstein")

    query.delete()

    albert_einstein = query.first()

    print(albert_einstein)
