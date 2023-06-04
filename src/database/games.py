import datetime
import sqlalchemy

from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase


class Games(SqlAlchemyBase):
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text)
    price = sqlalchemy.Column(sqlalchemy.Double, nullable=False)
    genre_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('genres.id'))
    create_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    genres = relationship('Genres', back_populates='games')
    users = relationship('Users', secondary='users_games', back_populates='games')

    def __repr__(self):
        return '<Game> [{}] {}'.format(self.id, self.title)