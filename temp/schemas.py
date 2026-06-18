from pydantic import BaseModel, ConfigDict

class StudentCreate(BaseModel):
    name : str

class StudentResponse(BaseModel):
    id : int
    name : str

    class Config:
        from_attributes =True   

class CourseCreate(BaseModel):
    title : str

class CourseResponse(BaseModel):
    id : int
    title : str
    class Config:
        from_attributes = True

class EnrollmentCreate(BaseModel):
    student_id : int
    course_id : int

class EnrollmentResponse(BaseModel):
    id : int
    title : str
    class Config:
        from_attributes = True

class StudentwithCourses(BaseModel):
    id:int
    name : str
    courses : list[CourseResponse]
    
    model_config = ConfigDict(from_attributes = True)

class CoursewithStudents(BaseModel):
    id : int
    title : str
    students : list[StudentResponse]

    model_config = ConfigDict(from_attributes = True)