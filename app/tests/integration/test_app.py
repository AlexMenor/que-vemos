from uuid import UUID
from fastapi.testclient import TestClient

from app.app import app, session_handler_dependency, SessionHandlerDependency
from app.data.session_store.session_store import SessionStore
from app.data.watchables_store.in_memory_watchables_store import InMemoryWatchablesStore
from app.entities.session import NotMoreUsersAllowedException, Session
from app.entities.watchable import Watchable, WatchableType

client = TestClient(app)


class CallableMock:
    """ Helper class to allow overriding dependencies """
    def __init__(self, mock):
        self.__mock = mock

    def __call__(self):
        return self.__mock


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
        async def join_user_to_session(self, _):
            raise NotMoreUsersAllowedException

    callable_mock = CallableMock(Mock())

    app.dependency_overrides[session_handler_dependency] = callable_mock

    response = client.post('/session/sí-existo/user')

    assert response.status_code == 409

    app.dependency_overrides = {}


def test_joining_session():
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

    response = client.post('/session/sí-existo/user')

    body = response.json()

    assert response.status_code == 201

    assert 'user_id' in body

    UUID(body['user_id'])

    assert body['session_id'] == session.id

    assert 'watchables' in body

    app.dependency_overrides = {}


