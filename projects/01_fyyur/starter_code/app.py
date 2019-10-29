#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import json
import dateutil.parser
import babel
import datetime
from flask import Flask, render_template, request, jsonify, Response, flash, redirect, url_for, current_app as app
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
from forms import *
from models import db, Venue, Artist, Show
from flask_whooshalchemyplus import index_all
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if format == 'full':
      format="EEEE MMMM, d, y"
  elif format == 'medium':
      format="EE MM, dd, y"
  return babel.dates.format_datetime(value, locale='en', format=format)

app.jinja_env.filters['date'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # fetch_venues = Venue.query.group_by("city", "state")
  fetch_venues = db.session.query(Venue).group_by(Venue.id, Venue.state, Venue.city).all()
  if not fetch_venues:
    flash('There are no venues yet')
    return render_template('pages/venues.html')
  venue_array = []
  venue_keys = ['id', 'name', 'city', 'state']
  for venue in fetch_venues:
    venue_info = [venue.id, venue.name, venue.city, venue.state]
    venue_array.append(dict(zip(venue_keys, venue_info)))
  return render_template('pages/venues.html', venues=venue_array)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  index_all(app)
  search_term=request.form.get('search_term', '')
  result = Venue.query.whoosh_search(search_term).all()
  count = len(result)
  return render_template('pages/search_venues.html', results=result,
                         search_term=request.form.get('search_term', ''),
                         count=count)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  venue = Venue.query.filter_by(id=venue_id).first()
  data = venue.__dict__
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(csrf_enabled=True)
  if form.validate_on_submit():
    venue_data = dict(
      name=form.name.data,
      genres=list(form.genres.data),
      address=form.address.data,
      city=form.city.data,
      state=form.state.data,
      phone=form.phone.data,
      website=form.website.data,
      facebook_link=form.facebook_link.data,
      seeking_talent=form.seeking_talent.data,
      seek_description=form.seek_description.data,
      image_link=form.image_link.data
      )
    check_venue = Venue.query.filter_by(name=form.name.data).first()
    if check_venue:
      flash('A venue with that name already exists')
      return render_template('pages/home.html')
    new_venue = Venue(**venue_data)
    new_venue.save()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  else:
    errors = form.errors
    for key, error in errors.items():
      flash(f"{key}  Error " + " => " + f"{error[0]} :(")
    return render_template('pages/home.html')
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
  check_venue = Venue.query.filter_by(id=venue_id).first()
  if not check_venue:
    return "Venue doesnot exist"
  try:
    db.session.delete(check_venue)
    db.session.commit()
    db.session.close()
    flash(f'{check_venue.name} was deleted')
    return jsonify({'message': 'deleted'})
  except:
    db.session.rollback()
    error=True
    db.session.close()
    flash("An error occured!! Delete failed")
    return render_template('pages/venues.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists_result = Artist.query.all()
  return render_template('pages/artists.html', artists=artists_result)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  index_all(app)
  search_term=request.form.get('search_term', '')
  result = Artist.query.whoosh_search(search_term).all()
  count = len(result)
  return render_template('pages/search_artists.html', count=count, 
                         results=result, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  artist = Artist.query.filter_by(id=artist_id).first()
  data = artist.__dict__
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.filter_by(id=artist_id).first()
  artist = artist.__dict__
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  artist = Artist.query.filter_by(id=artist_id).first()
  form = ArtistForm(crsf_enabled=True)
  try:
    if form.validate_on_submit():
      artist.name = form.name.data
      artist.city = form.city.data
      artist.genres = form.genres.data
      artist.state = form.state.data
      artist.phone = form.phone.data
      artist.seeking_venue = form.seeking_venue.data
      artist.seek_description = form.seek_description.data
      artist.website = form.website.data
      artist.image_link = form.image_link.data
      artist.facebook_link = form.facebook_link.data
      db.session.commit()
      db.session.close()
  except:
    db.session.rollback()
    db.session.close()        
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.filter_by(id=venue_id).first()
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  venue = Venue.query.filter_by(id=venue_id).first()
  form = VenueForm(crsf_enabled=True)
  try:
    if form.validate_on_submit():
      venue.name = form.name.data
      venue.city = form.city.data
      venue.state = form.state.data
      venue.address = form.address.data
      venue.phone = form.phone.data
      venue.genres = form.genres.data
      venue.seeking_talent = form.seeking_talent.data
      venue.seek_description = form.seek_description.data
      venue.image_link = form.image_link.data
      venue.website = form.website.data
      venue.facebook_link = form.facebook_link.data
      db.session.commit()
      db.session.close()
      flash(f"{venue.name} data was updated")
  except:
    db.session.rollback()
    db.session.close()    
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(csrf_enabled=True)
  if form.validate_on_submit():
    artist_data = dict(
      name=form.name.data,
      genres=list(form.genres.data),
      city=form.city.data,
      state=form.state.data,
      phone=form.phone.data,
      website=form.website.data,
      facebook_link=form.facebook_link.data,
      seeking_venue=form.seeking_venue.data,
      seek_description=form.seek_description.data,
      image_link=form.image_link.data
      )
    check_artist = Artist.query.filter_by(name=form.name.data).first()
    if check_artist:
      flash('Artist with that name already exists')
      return render_template('pages/home.html')
    new_artist = Artist(**artist_data)
    new_artist.save()
    flash('Artist ' + request.form['name'] + ' was successfully added!')
  else:
    errors = form.errors
    for key, error in errors.items():
      flash(f'{key}  Error ' + " => " + f"{error[0]} :(")
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  today = datetime.date.today()
  shows = db.session.query(Show).filter(Show.date >= today).all()
  artist_data = []
  venue_data = []
  for show in shows:
    artist_info = Artist.query.filter_by(id=show.artist_id).first()
    venue_info = Venue.query.filter_by(id=show.venue_id).first()
    artist_data.append(artist_info)
    venue_data.append(venue_info)
  return render_template('pages/shows.html', shows=shows,
                         artists=artist_data, venues=venue_data)

@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm(csrf_enabled=True)
  artist = Artist.query.filter_by(id=form.artist_id.data).first()
  venue = Venue.query.filter_by(id=form.venue_id.data).first()
  if not artist:
    flash(" Artist doesnot exist")
    return render_template('pages/home.html')
  elif artist.seeking_venue is False:
    flash("Artist not available")
    return render_template('pages/home.html')
  elif not venue:
    flash("Venue doesnot exists")
    return render_template('pages/home.html')
  if form.validate_on_submit():
    show_data = dict(
      name=form.name.data,
      artist_id=form.artist_id.data,
      artist_image_link=artist.image_link,
      artist_name=artist.name,
      venue_id=form.venue_id.data,
      venue_name=venue.name,
      start_time=form.start_time.data,
      end_time=form.end_time.data,
      date=form.date.data,
      show_fee=form.fee.data
      )
    check_show = Show.query.filter_by(name=form.name.data, venue_id=form.venue_id.data).first()
    if check_show:
      flash('Show already exists already exists')
      return render_template('pages/home.html')
    new_show = Show(**show_data)
    new_show.save()
    flash('Show ' + request.form['name'] + ' was successfully added!')
  else:
    errors = form.errors
    for key, error in errors.items():
      flash(f'{key}  Error ' + " => " + f"{error[0]} :(")
  return render_template('pages/home.html')

 
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
