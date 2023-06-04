import sqlalchemy

from .db_session import SqlAlchemyBase


class UsersGames(SqlAlchemyBase):
    __tablename__ = 'users_games'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('users.id'))
    game_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('games.id'))
    is_delivered = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    def __repr__(self):
        return '<UserGames> [{}] {} - {}'.format(self.id, self.user_id, self.game_id)
