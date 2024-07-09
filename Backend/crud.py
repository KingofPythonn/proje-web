from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy.sql import functions

# read channel

def get_channel_by_id(db: Session, channel_id: int):
    return db.query(models.Channel).filter(models.Channel.cId == channel_id).first()

def get_channel_by_name(db: Session, channel_name: str):
    return db.query(models.Channel).filter(models.Channel.channelName == channel_name).first()

def get_all_channels(db: Session):
    return db.query(models.Channel).all()

# read message

def get_message_by_id(db: Session, message_id: int):
    return db.query(models.Message).filter(models.Message.mId == message_id).first()

def get_all_messages(db: Session):
    return db.query(models.Message).all()

def get_messages_in_a_channel(db: Session, channel_id: int):
    return db.query(models.Message).filter(models.Message.channelId == channel_id).all()

# count mixture

def number_of_channels(db: Session):
    return db.query(models.Channel).count()

def number_of_messages(db: Session):
    return db.query(models.Message).count()

def number_of_messages_in_a_channel(db: Session, channel_id: int):
    return db.query(models.Message).filter(models.Message.channelId == channel_id).count()

def number_of_votes_for_a_message(db: Session, message_id: int):
    return db.query(models.Message).filter(models.Message.mId == message_id).first().voteNumber

def number_of_votes(db: Session):
    return db.query(functions.sum(models.Message.voteNumber)).scalar()

# create channel

def create_channel(db: Session, channel: schemas.ChannelCreate):
    db_channel = models.Channel(
        channelName=channel.channelName
    )
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel

# star messages

def get_star_messages_of_channel(db: Session, channel_id: int):
    all_messages = db.query(models.Message).filter(models.Message.channelId == channel_id)
    star_message = all_messages.filter(models.Message.voteNumber != 0).order_by(models.Message.voteNumber).all()
    star_message.reverse()
    return star_message

# important messages

def get_important_messages_of_channel(db: Session, channel_id: int):
    all_messages = db.query(models.Message).filter(models.Message.channelId == channel_id)
    star_message = all_messages.order_by(models.Message.voteNumber).all()
    star_message.reverse()
    return star_message
