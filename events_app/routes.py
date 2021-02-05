"""Import packages and modules."""
import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from events_app.models import Event, Guest

# Import app and db from events_app package so that we can run app
from events_app import app, db

main = Blueprint('main', __name__)


##########################################
#           Routes                       #
##########################################

@main.route('/')
def index():
    """Show upcoming events to users!"""
    events = Event.query.all()
    return render_template('index.html', events=events)


@main.route('/event/<event_id>', methods=['GET'])
def event_detail(event_id):
    """Show a single event."""
    event = Event.query.filter_by(id=event_id).one()

    context = {
        'event': event
    }

    return render_template('event_detail.html', **context)


@main.route('/event/<event_id>', methods=['POST'])
def rsvp(event_id):
    """RSVP to an event."""
    # TODO: Get the event with the given id from the database
    is_returning_guest = request.form.get('returning')
    guest_name = request.form.get('guest_name')

    if is_returning_guest:
        guest = Guest.query.filter_by(name=guest_name).one()
        guest.events_attending.append(Event.query.filter_by(id=event_id).one())
    else:
        guest_email = request.form.get('email')
        guest_phone = request.form.get('phone')

        event = Event.query.filter_by(id=event_id).one()
        new_guest = Guest(name=guest_name, email=guest_email,
                          phone=guest_phone)
        db.session.add(new_guest)
        db.session.commit()

        guest = Guest.query.filter_by(name=guest_name).one()
        guest.events_attending.append(Event.query.filter_by(id=event_id).one())

    flash('You have successfully RSVP\'d! See you there!')
    return redirect(url_for('main.event_detail', event_id=event_id))


@main.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new event."""
    if request.method == 'POST':
        new_event_title = request.form.get('title')
        new_event_description = request.form.get('description')
        date = request.form.get('date')
        time = request.form.get('time')

        try:
            date_and_time = datetime.strptime(
                f'{date} {time}',
                '%Y-%m-%d %H:%M')
        except ValueError:
            print('there was an error: incorrect datetime format')

        new_event = Event(
            title=new_event_title, description=new_event_description, date_and_time=date)

        flash('Event created.')
        return redirect(url_for('main.index', new_event))
    else:
        return render_template('create.html')


@main.route('/guest/<guest_id>')
def guest_detail(guest_id):
    guest_info = Guest.query.filter_by(id=guest_id).one()
    return render_template('guest_detail.html')
