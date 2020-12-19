from uuid import UUID
from fastapi.testclient import TestClient
import pytest

from app.app import app
from app.routes.session_routes import SessionHandlerDependency, session_handler_dependency
from app.data.session_store.session_store import SessionStore
from app.data.watchables_store.in_memory_watchables_store import InMemoryWatchablesStore
from app.entities.session import NotMoreUsersAllowedException, Session
from app.entities.user import User
from app.entities.watchable import Watchable, WatchableType

client = TestClient(app)


class CallableMock:
    """ Helper class to allow overriding dependencies """
    def __init__(self, mock):
        self.__mock = mock

    def __call__(self):
        return self.__mock


@pytest.fixture
def existing_session():
    watchable = Watchable("Narcos", "Se centra en la historia real de una peligrosa difusión y propagación de una red de cocaína por todo el mundo durante los años 70 y 80.", 2015, WatchableType.SERIES)
    session = Session('sí-existo', [watchable])

    class Mock(SessionStore):
        async def save(self, session: Session) -> None:
            pass

        async def get_one(self, _):
            return session

    watchables_store = InMemoryWatchablesStore()

    session_handler_mocked = SessionHandlerDependency(watchables_store, Mock())

    app.dependency_overrides[session_handler_dependency] = session_handler_mocked

    yield session

    app.dependency_overrides = {}

@pytest.fixture
def existing_session_and_user(existing_session):
    existing_user = User('yo-también')
    existing_session.add_user(existing_user)

    yield existing_session, existing_user


@pytest.fixture
def existing_session_and_vote(existing_session_and_user):
    session = existing_session_and_user[0]
    user = existing_session_and_user[1]

    session.vote(user.id, 0, True)

    yield session


def test_create_session():
    response = client.post("/session")
    body = response.json()

    assert response.status_code == 201
    assert 'session_id' in body
    UUID(body['session_id'])


def test_joining_non_existing_session():
    response = client.post('/session/no-existo/user')

    assert response.status_code == 404


def test_joining_with_max_users():
    class Mock:
        async def join_user_to_session(self, _, __):
            raise NotMoreUsersAllowedException

    callable_mock = CallableMock(Mock())

    app.dependency_overrides[session_handler_dependency] = callable_mock

    response = client.post('/session/sí-existo/user')

    assert response.status_code == 409

    app.dependency_overrides = {}


def test_joining_session(existing_session):

    response = client.post(f'/session/{existing_session.id}/user')

    body = response.json()

    assert response.status_code == 201

    assert 'user_id' in body

    UUID(body['user_id'])

    assert body['session_id'] == existing_session.id

    assert 'watchables' in body

def test_voting_without_body():
    response = client.post('/session/no-existo/user/yo-tampoco/vote')

    assert response.status_code == 422


def test_voting_in_non_existing_session():
    response = client.post('/session/no-existo/user/yo-tampoco/vote', json={'watchable_index': 0, 'content': "true"})

    assert response.status_code == 404


def test_voting_with_non_existing_user(existing_session):
    response = client.post(f'/session/{existing_session.id}/user/yo-no/vote', json={'watchable_index': 0, 'content': "true"})

    assert response.status_code == 404

    assert response.json()['detail'] == f'An user with id yo-no could not be found in session {existing_session.id}'


def test_voting_non_existing_watchable(existing_session_and_user):
    response = client.post(f'/session/{existing_session_and_user[0].id}/user/{existing_session_and_user[1].id}/vote', json={'watchable_index': 99, 'content': "true"})

    assert response.status_code == 400

    assert response.json()['detail'] == 'The watchable index 99 is out of bounds'


def test_voting(existing_session_and_user):
    session = existing_session_and_user[0]
    user = existing_session_and_user[1]

    response = client.post(f'/session/{session.id}/user/{user.id}/vote', json={'watchable_index': 0, 'content': "true"})

    assert response.status_code == 201

    assert session.get_votes_of_watchable(0)[0] == 1 and session.get_votes_of_watchable(0)[1] == 1


def test_summary_non_existing_session():
    response = client.get('/session/no-existo/summary')

    assert response.status_code == 404


def test_summary(existing_session_and_vote):
    response = client.get(f'/session/{existing_session_and_vote.id}/summary')
    body = response.json()

    assert response.status_code == 200

    assert 'users' in body

    assert 'votes' in body
