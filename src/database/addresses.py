import datetime
import sqlalchemy

from .db_session import SqlAlchemyBase


class Addresses(SqlAlchemyBase):
    __tablename__ = 'addresses'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    lat = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    lon = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    create_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<Address> [{}] {}'.format(self.id, self.address)
