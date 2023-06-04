import datetime
import sqlalchemy

from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase


class Users(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    create_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    games = relationship('Games', secondary='users_games', back_populates='users')

    def __repr__(self):
        return '<User> [{}] {}'.format(self.id, self.user_id)
