from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Literal
from database import get_db,Base,engine
from models import Note,User
from schemas import NoteCreate,UserLogin, NoteResponse, UserCreate,UserResponse
from auth import get_hashed_password,verify_password,create_access_token,get_current_user
from fastapi.security import OAuth2PasswordRequestForm
app = FastAPI()

Base.metadata.create_all(bind=engine)

notfound = HTTPException(
            status_code=404,
            detail="Note not found"
        )

@app.post("/notes",response_model= NoteResponse)
def create_note(note : NoteCreate, db : Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    new_note = Note(title = note.title,content = note.content,owner_id=current_user.id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.get("/notes/{id}",response_model=NoteResponse)
def get_note(id : int, db:Session=Depends(get_db),current_user:User = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == id,Note.owner_id==current_user.id).first()
    if not note:
        raise HTTPException(
            status_code=404,
            detail= "Note not found"
        )
    return note

@app.put("/notes/{id}",response_model=NoteResponse)
def update_note(id:int,note : NoteCreate,db :Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    update = db.query(Note).filter(Note.id == id,Note.owner_id==current_user.id).first()
    if not update:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )
    update.title = note.title
    update.content = note.content
    db.commit()
    db.refresh(update)
    return update

@app.delete("/notes/{id}")
def delete_note(id : int, db:Session=Depends(get_db),current_user:User = Depends(get_current_user)):
    delete = db.query(Note).filter(Note.id == id,Note.owner_id==current_user.id).first()
    if not delete:
        raise notfound
    db.delete(delete)
    db.commit()
    return {"message" : "Note Deleted"}

@app.get("/notes", response_model=list[NoteResponse])
def get_notes(
    title: str = None,
    order: Literal["asc", "desc"] = "asc",
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Note).filter(Note.owner_id==current_user.id)

    if title:
        query = query.filter(Note.title.contains(title))

    if order == "asc":
        query = query.order_by(Note.id.asc())
    else:
        query = query.order_by(Note.id.desc())

    return query.offset(skip).limit(limit).all()

@app.post("/signup",response_model=UserResponse)
def signup(user:UserCreate,db:Session=Depends(get_db)):
    new_user = User(username = user.username,email = user.email,hashed_password = get_hashed_password(user.password))
    existing_user = db.query(User).filter(User.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=400,detail="Username already exists")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login")
def login_user(form_data : OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username==form_data.username).first()
    if not existing_user:
        raise notfound
    if not verify_password(form_data.password,existing_user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )
    access_token = create_access_token(
        {
            "sub": existing_user.username
        }
    )
    return {
        "access_token":access_token,
        "token_type" : "bearer"
    }

@app.get("/me")
def get_me(current_user:User =  Depends(get_current_user)):
    return current_user