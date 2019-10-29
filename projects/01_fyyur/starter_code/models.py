# from app import app as app
from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

db = SQLAlchemy()

class Venue(db.Model):
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
    venue_shows = db.relationship('Show', backref='Venue', lazy=True)
    
    def __init__(self):
        self.operate = DbOperations(self, db)
        
    def __repr__(self):
        return f"<Venue obj: {name}>"
        
    def save(self):
        """
        Add venue resource
        """
        self.operate.save()
        
    def delete(self):
        """
        Delete venue resource
        """
        self.operate.delete()

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
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
    artist_shows = db.relationship('Show', backref='Artist', lazy=True)
    
    def __init__(self):
        self.operate = DbOperations(self, db)
        
    def __repr__(self):
        return f"<Artist obj: {name}>"
        
    def save(self):
        """
        Add artist resource
        """
        self.operate.save()
        
    def delete(self):
        """
        Delete artist resource
        """
        self.operate.delete()
    
class Show(db.Model):
    """
    Model class for creating and manipulating show objects
    """
    __tablename__ = 'Show'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.String(120), nullable=False)
    end_time = db.Column(db.String(120), nullable=False)
    show_fee = db.Column(db.String(120), nullable=False)
    
    def __init__(self):
        self.operate = DbOperations(self, db)
        
    def __repr__(self):
        return f"<Show obj: {name}>"
        
    def save(self):
        """
        Add show resource
        """
        self.operate.save()
        
    def delete(self):
        """
        Delete show resource
        """
        self.operate.delete()
    
class DbOperations(object):
    """
    Class for handling database operations
    """
    def __init__(self, resource_instance, db):
        self.resource_instance = resource_instance
        self.db = db
        
    def save(self):
        """
        Method for saving new data resource to the database
        """
        try:
            self.db.session.add(self.resource_instance)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            error=True
        finally:
            self.db.session.close()
            
    def delete(self):
        """
        Method for deleting a data resource from the database
        """
        try:
            self.db.session.delete(self.resource_instance)
            self.db.session.commit()
        except:
            self.db.session.rollback()
            error=True
        finally:
            self.db.session.close()

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
