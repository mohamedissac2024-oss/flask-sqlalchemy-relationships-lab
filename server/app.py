from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

# --- App setup ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


# --- Helpers ---
def speaker_with_bio(speaker):
    """Format a speaker as a dict, using a default when there is no bio."""
    return {
        'id': speaker.id,
        'name': speaker.name,
        'bio_text': speaker.bio.bio_text if speaker.bio else 'No bio available',
    }


# --- Event endpoints ---
@app.route('/events')
def get_events():
    """Return all events."""
    events = [
        {'id': e.id, 'name': e.name, 'location': e.location}
        for e in Event.query.all()
    ]
    return jsonify(events), 200


@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    """Return all sessions for one event, or 404 if the event doesn't exist."""
    event = db.session.get(Event, id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404

    sessions = [
        {'id': s.id, 'title': s.title, 'start_time': s.start_time.isoformat()}
        for s in event.sessions
    ]
    return jsonify(sessions), 200


# --- Speaker endpoints ---
@app.route('/speakers')
def get_speakers():
    """Return all speakers."""
    speakers = [{'id': s.id, 'name': s.name} for s in Speaker.query.all()]
    return jsonify(speakers), 200


@app.route('/speakers/<int:id>')
def get_speaker(id):
    """Return one speaker with their bio, or 404 if not found."""
    speaker = db.session.get(Speaker, id)
    if not speaker:
        return jsonify({'error': 'Speaker not found'}), 404
    return jsonify(speaker_with_bio(speaker)), 200


# --- Session endpoints ---
@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    """Return all speakers for one session, or 404 if the session doesn't exist."""
    session = db.session.get(Session, id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    return jsonify([speaker_with_bio(s) for s in session.speakers]), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)