from get_comments import Base, Comment
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///comments.sqlite')
Base.metadata.bind = engine
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

session.query(Comment).filter(Comment.uscisid == "USCIS-2010-0012-7079p").one()
