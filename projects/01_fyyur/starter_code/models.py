# from app import app as app
from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app
from constants import searchable_fields
import flask_whooshalchemyplus

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

db = SQLAlchemy()


class BaseModel(object):
    __searchable__ =  searchable_fields # indexed fields
    """
    Class for handling database operations
    """
    
    def save(self):
        """
        Method for saving new data resource to the database
        """
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            error=True
        finally:
            db.session.close()


class Venue(db.Model, BaseModel):
    """
    Model class for creating and manipulating venue objects
    """
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    genres = db.Column(db.PickleType) # Array containing venue genres
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seek_description = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    past_shows = db.Column(db.PickleType) # Array of dict objects for past shows
    upcoming_shows = db.Column(db.PickleType) # Array dict objects for upcoming shows
    past_shows_count = db.Column(db.Integer, default=0)
    upcoming_shows_count = db.Column(db.Integer, default=0)
    venue_shows = db.relationship('Show', cascade='all, delete', backref='Venue', lazy=True)

    def __repr__(self):
        return f"<Venue obj: {self.name}>"


class Artist(db.Model, BaseModel):
    """
    Model class for creating and manipulating artist objects
    """
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    genres = db.Column(db.PickleType) # Array containing genres
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seek_description = db.Column(db.String(300))
    image_link = db.Column(db.String(500))
    past_shows = db.Column(db.PickleType) # Array of dict objects for past shows
    upcoming_shows = db.Column(db.PickleType) # Array of dict objects for upcoming shows
    past_shows_count = db.Column(db.Integer, default=0)
    upcoming_shows_count = db.Column(db.Integer, default=0)
    artist_shows = db.relationship('Show', cascade='all, delete', backref='Artist', lazy=True)
    
    def __repr__(self):
        return f"<Artist obj: {self.name}>"


class Show(db.Model, BaseModel):
    """
    Model class for creating and manipulating show objects
    """
    __tablename__ = 'Show'
    __searchable__ = []
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id', ondelete='CASCADE'),
                          nullable=False)
    artist_image_link = db.Column(db.String(300))
    artist_name = db.Column(db.String(120))
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id', ondelete='CASCADE'),
                         nullable=False)
    venue_name = db.Column(db.String(120))
    date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.String(120), nullable=False)
    end_time = db.Column(db.String(120), nullable=False)
    show_fee = db.Column(db.String(120), nullable=False)
    
    def __repr__(self):
        return f"<Show obj: {self.name}>"
