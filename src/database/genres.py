import datetime
import sqlalchemy

from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase


class Genres(SqlAlchemyBase):
    __tablename__ = 'genres'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text)
    create_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    games = relationship('Games', back_populates='genres')

    def __repr__(self):
        return '<Genre> [{}] {}'.format(self.id, self.title)