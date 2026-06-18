from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base, get_db
from models import Student, Course, enrollment
from schemas import StudentCreate,StudentResponse,CoursewithStudents,CourseCreate,CourseResponse,StudentwithCourses, EnrollmentCreate, EnrollmentResponse

app = FastAPI()

Base.metadata.create_all(bind = engine)

@app.post("/students",response_model=StudentResponse)
def create_student(student: StudentCreate, db : Session = Depends(get_db)):
    new_student = Student(name = student.name)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student  

@app.post("/courses",response_model=CourseResponse)
def create_course(course : CourseCreate, db : Session = Depends(get_db)):
    new_course = Course(title = course.title)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@app.post("/enroll")
def enroll_student(enrollment : EnrollmentCreate,db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == enrollment.student_id).first()
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()

    if not student:
        raise HTTPException(
            status_code= 404,
            detail= "Student not found"
        )
    if not course:
        raise HTTPException(
            status_code= 404,
            detail= "Course not found"
        )
    if course in student.courses:
        raise HTTPException(
            status_code= 400,
            detail= "Student already enrolled in this course"
        )
    
    student.courses.append(course)
    db.commit()
    return {"message" : "Enrollment Successfull"}

@app.get("/students",response_model= list[StudentResponse])
def get_students(db : Session = Depends(get_db)):
    students = db.query(Student).all()
    return students

@app.get("/students/{student_id}",response_model= StudentwithCourses )
def get_student(student_id:int,db : Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    return student

@app.get("/courses",response_model= list[CourseResponse])
def get_courses(db : Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses

@app.get("/courses/{course_id}",response_model= CoursewithStudents)
def get_courses(course_id : int,db : Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    return course

@app.get("/enrollments/{student_id}/courses",response_model=list[EnrollmentResponse])
def get_enrollment(student_id: int,db : Session = Depends(get_db)):
    students = db.query(Student).filter(Student.id == student_id).first()
    return students.courses