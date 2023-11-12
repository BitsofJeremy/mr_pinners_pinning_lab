# pinning_lab/database/models.py

from flask_login import UserMixin
from pinning_lab import db


class Base(db.Model):
    """ Basic Table Structure """
    __abstract__ = True
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    date_created = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )
    date_modified = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )


class Users(UserMixin, Base):
    """ User table """
    __tablename__ = 'users'

    email = db.Column(db.String(128), unique=True)
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    # TODO upload and hash img
    profile_pic = db.Column(db.String(128))
    slots_purchased = db.Column(db.Integer, default=0)

    # images owned
    images = db.relationship(
        'Images',
        backref='users',
        lazy=True
    )


class Images(Base):
    """ Images Table """

    __tablename__ = 'images'

    # Basics
    name = db.Column(db.String(256))
    description = db.Column(db.String(256))
    ipfs_hash = db.Column(db.String(256))
    pinned = db.Column(db.Boolean)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    # Return function
    def __repr__(self):
        return self.name

    def update(self, **kwargs):
        """ Updates a Image information  """
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def serialize(self):
        """ Returns a dictionary of the Image information """
        return {
            'id': self.id,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'name': self.name,
            'description': self.description,
            'ipfs_hash': self.ipfs_hash,
            'pinned': self.pinned,
            'created_by': self.user_id,
         }
