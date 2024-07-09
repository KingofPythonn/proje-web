from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

# model for channel

class Channel(Base):
    
    # table name for channels
    __tablename__ = 'channels'

    cId = Column(Integer, primary_key=True, autoincrement=True)
    channelName = Column(String, unique=True)

# model for message

class Message(Base):
    
    # table name for messages
    __tablename__ = 'messages'
    
    mId = Column(Integer, primary_key=True, autoincrement=True)
    
    # foreign key to cId of table channels
    channelId = Column(Integer, ForeignKey("channels.cId"))
    
    messageText = Column(String)
    voteNumber = Column(Integer, default=0)
