from pydantic import BaseModel, Field

# channel

class ChannelBase(BaseModel):
    channelName: str

class ChannelCreate(ChannelBase):
    pass

class Channel(ChannelBase):
    cId: int
    class Config:
        orm_mode = True

# message

class MessageBase(BaseModel):
    messageText: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    mId: int
    channelId: int
    voteNumber: int = Field(default=0)
    class Config:
        orm_mode = True
