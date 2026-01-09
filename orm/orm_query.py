from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User

engine = create_engine(
    "postgresql://demo:demo@localhost:5432/demo",
    echo=False
)

Session = sessionmaker(bind=engine)
session = Session()

users = (
    session.query(User)
    .filter(User.profile["active"].astext == "true")
    .filter(User.profile["skills"].contains(["python"]))
    .all()
)

print([u.name for u in users])
