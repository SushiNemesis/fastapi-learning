from sqlalchemy import Integer, Column, String,Float, ForeignKey, Table
from database import Base
from sqlalchemy.orm import relationship 

enrollment = Table(
    "enrollment",Base.metadata,
    Column("student_id",Integer,ForeignKey("students.id")),
    Column("course_id",Integer, ForeignKey("courses.id")) 
                   )

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    courses = relationship("Course",secondary=enrollment,back_populates="students")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer,primary_key=True)
    title = Column(String)

    students = relationship("Student",secondary=enrollment,back_populates="courses")
