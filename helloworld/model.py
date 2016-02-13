import datetime;
import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm
from sqlalchemy import (
    Table, Column,
    Integer, String, DateTime, Text, 
    ForeignKey, UniqueConstraint, Index)

Base = declarative_base()

#
# Define model
#

article_table = Table('article', Base.metadata,
    Column('id', Integer(), primary_key=True),
    Column('title', String(128), nullable=False),
    Column('body', Text()),
    Column('posted_at', DateTime(), nullable=False)
)

class Article(Base):
    __table__ = article_table

    def __init__(self, title, body=None):
        self.id = None
        self.title = title
        self.body = body
        self.posted_at = datetime.datetime.now()


#
# Prepare a session factory
#

# The factory should be (re)configured when actual configuration is available
Session = orm.scoped_session(orm.sessionmaker())
