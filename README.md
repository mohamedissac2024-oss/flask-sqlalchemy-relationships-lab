# Flask SQLAlchemy Relationships Lab

A Flask-SQLAlchemy backend for an event management company (EventWise). It models events, sessions, speakers and bios, and exposes them through JSON endpoints.

## Relationships

- **Event → Sessions:** one-to-many. Deleting an event deletes its sessions.
- **Speaker → Bio:** one-to-one. Deleting a speaker deletes their bio.
- **Session ↔ Speaker:** many-to-many through the `session_speakers` table.

## Setup

```bash
pipenv install
pipenv shell
cd server
export FLASK_APP=app.py
export FLASK_RUN_PORT=5555
flask db init
flask db migrate -m "Create tables with relationships"
flask db upgrade head
python seed.py
flask run
```

## Endpoints

| Method | Route                     | Description                                                |
| ------ | ------------------------- | ---------------------------------------------------------- |
| GET    | `/events`                 | List all events                                            |
| GET    | `/events/<id>/sessions`   | List sessions for an event (404 if not found)              |
| GET    | `/speakers`               | List all speakers                                          |
| GET    | `/speakers/<id>`          | Speaker with bio, or "No bio available" (404 if not found) |
| GET    | `/sessions/<id>/speakers` | Speakers for a session (404 if not found)                  |

## Tests

Run `pytest` from the `server` directory. All 13 tests pass.

![Passing tests](screenshot.png)
