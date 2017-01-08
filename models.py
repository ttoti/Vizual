from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

#Users table/class
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(120), unique=True)
    password = Column(String(60))
    #postings = db.relationship("Posting")

    def __init__(self, name=None, password=None):
        self.username = name
        self.password = self.set_password(password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)
#Postings table
class Posting(Base):
    __tablename__ = 'postings'
    id = Column(Integer, primary_key=True)
    url = Column(String(120), unique=True)
    title = Column(String(120), unique=True)
    author = Column(String(120), unique=True)
    filename = Column(String(120), unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = Column(String(60), unique=False)

    def __init__(self, url=None, title=None, author=None, filename=None, user_id=None, user=None):
        self.url = url
        self.title = title
        self.author = author
        self.filename = filename
        self.user_id = user_id
        self.user = user

    def get_url(self):
        return unicode(self.id)

Base.metadata.create_all(bind=engine)
