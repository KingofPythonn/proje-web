from fastapi import FastAPI, Depends, Request, Response
from database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, crud

# fast api set

app = FastAPI()

# database set

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# frontend set

origins = [
    "*",
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

# routes set

# route 1 -> creation

@app.post("/creation", status_code=200, response_model=schemas.Channel)
async def creation(channel: schemas.ChannelCreate, db: Session = Depends(get_db)):
    db_channel = crud.create_channel(db=db, channel=channel)
    
    return db_channel

# route 2 -> show

@app.get("/show")
async def show(db: Session = Depends(get_db)):
    
    channels = crud.get_all_channels(db=db)
    
    result = {
        "channels": channels
    }
    
    return result

@app.get("/show/{channelId}")
async def show(channelId: int, db: Session = Depends(get_db)):
    
    channels = crud.get_all_channels(db=db)
    messages = crud.get_messages_in_a_channel(db=db, channel_id=channelId)
    print(channelId)
    result = {
        "channels": channels,
        "messages": messages
    }
    
    return result

@app.put("/show/{channelId}", response_model=schemas.Message)
async def show_vote(messageId: int, db: Session = Depends(get_db)):
    
    message_model = db.query(models.Message).filter(models.Message.mId == messageId).first()
    
    message_model.voteNumber = message_model.voteNumber+1
    db.add(message_model)
    db.commit()
    
    return message_model







# route 3 -> stars

# route 3 -> stars

@app.get("/stars", status_code=200)
async def stars(db: Session = Depends(get_db)):
    
    channels = crud.get_all_channels(db=db)
    
    result = {
        "channels": channels
    }
    
    return result


@app.get("/stars/{channelId}", status_code=200)
async def stars(channelId: int, db: Session = Depends(get_db)):
    
    channels = crud.get_all_channels(db=db)
    messages = crud.get_star_messages_of_channel(db=db, channel_id=channelId)
    
    result = {
        "channels": channels,
        "messages": messages
    }
    
    return result




# route 4 -> report

@app.get("/report", status_code=200)
async def report(db: Session = Depends(get_db)):
    
    number_of_channels = crud.number_of_channels(db=db)
    number_of_messages = crud.number_of_messages(db=db)
    number_of_votes = crud.number_of_votes(db=db)
    
    result = {
        "number_of_channels": number_of_channels,
        "number_of_messages": number_of_messages,
        "number_of_votes": number_of_votes
    }
    
    return result

# route 5 -> important

@app.get("/important", status_code=200)
async def important(db: Session = Depends(get_db)):
    
    channels = crud.get_all_channels(db=db)
    
    result = {
        "channels": channels
    }
    
    return result

@app.get("/important/{channelId}", status_code=200)
async def important(channelId: int, db: Session = Depends(get_db)):
    
    channels = crud.get_all_channels(db=db)
    messages = crud.get_important_messages_of_channel(db=db, channel_id=channelId)
    
    result = {
        "channels": channels,
        "messages": messages
    }
    
    return result
