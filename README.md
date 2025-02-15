# Event API

This is a simple API for events, sessions, and users.

## Usage

To use this API, you can use the following endpoints:

- `/docs`: To get the documentation of the API.
- `/graphql`: To get the GraphQL API. It's just a basic stuff for events, sessions, and users.

For Events:
- `/event`: To get all events.
- `/event/search`: To search for events with Elasticsearch, it's very simple
- `/event/{id}`: To get an event by id, also update and delete an event.
- `/event/{id}/registrations`: To get all users for an event and delete a user from an event.
- `/event/{id}/register`: To register to an event.

For Sessions:
- `/session`: To get all sessions.
- `/session/{id}`: To get a session by id, also update and delete a session.
- `/session/{id}/registrations`: To get all users for a session and delete a user from a session.
- `/session/{id}/register`: To register to a session.

For Users:
- `/auth/token`: To login and get an access token.
- `/auth/`: To register a new user.

## Installation

To install this API, you can use docker compose:

```bash
docker-compose build
docker-compose up
```

The build inmediatly runs alembic migrations and upgrades the database, but you can also run them manually:

```bash
docker-compose exec api alembic upgrade head
```

And you can run the tests:

```bash
docker-compose exec api pytest
```

## License

This API is licensed under the MIT License.
