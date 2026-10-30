from fastapi.testclient import TestClient
from main import app
import pytest
from db import get_db
import psycopg
import models
from psycopg.rows import dict_row

# url for test db
TEST_DATABASE_URL = "postgresql://test_user:test_password@localhost:5432/test_db"

# prepare tables before test
@pytest.fixture(scope='session', autouse=True)
def setup_test_database():
    with psycopg.connect(TEST_DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(models.CREATE_STATUS_ENUM)
            cur.execute(models.CREATE_USERS_TABLE)
            cur.execute(models.CREATE_NOTES_TABLE)
            cur.execute(models.CREATE_NOTES_INDEX)
            cur.execute(models.CREATE_USER_NOTES_INDEX)
        conn.commit()
    yield

@pytest.fixture(autouse=True)
def clean_tables():
    yield
    with psycopg.connect(TEST_DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE notes, users RESTART IDENTITY CASCADE")
        conn.commit()

# create test data
@pytest.fixture
def create_test_user():
    with psycopg.connect(TEST_DATABASE_URL, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(models.POST_USER, ('User1', ))
            user = cur.fetchone()
        conn.commit()
        return user

@pytest.fixture
def create_test_note(create_test_user):
    test_user = create_test_user
    with psycopg.connect(TEST_DATABASE_URL, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(models.POST_NOTE, ('note1', 'note1 content','draft', test_user['id']))
            note = cur.fetchone()
        conn.commit()
    return note

# create override get_db, and set override_dict(needs for exchange depends(get_db) by test)
def override_get_db():
    with psycopg.connect(TEST_DATABASE_URL, row_factory=dict_row) as conn:
        yield conn

@pytest.fixture(scope='session', autouse=True)
def manage_dependency_override():
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()

client = TestClient(app)

def test_read_root():
    response = client.get("/health")
    assert response.status_code == 200

def test_add_user():
    user_data = {'name': 'user1'}
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    response_data = response.json()
    assert 'id' in response_data
    assert response_data['name'] == 'user1'
    response_user_id = response_data['id']

    with psycopg.connect(TEST_DATABASE_URL, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(models.GET_USER, (response_user_id, ))
            user = cur.fetchone()
    assert user is not None
    assert user['name'] == 'user1'

def test_get_user(create_test_user):
    test_user = create_test_user
    response = client.get("/users/{}".format(test_user['id']))
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['name'] == test_user['name']

def test_add_note(create_test_user):
    test_user = create_test_user
    note_data = {'title': 'note1', 'content':'note1 content', 'status':'draft', 'user_id': test_user['id']}
    response = client.post("/notes", json=note_data)
    assert response.status_code == 201
    response_data = response.json()
    assert 'id' in response_data
    assert response_data['title'] == 'note1'
    assert response_data['content'] == 'note1 content'
    assert response_data['status'] == 'draft'
    assert response_data['user_id'] == test_user['id']
    response_id_note = response_data['id']
    with psycopg.connect(TEST_DATABASE_URL, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(models.GET_NOTE, (response_id_note, ))
            note = cur.fetchone()
    assert note is not None
    assert note['title'] == 'note1'
    assert note['content'] == 'note1 content'
    assert note['status'] == 'draft'
    assert note['user_id'] == test_user['id']

def test_get_note(create_test_note):
    test_note = create_test_note
    response = client.get("/notes/{}".format(test_note['id']))
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['id'] == test_note['id']
    assert response_data['title'] == 'note1'
    assert response_data['content'] == 'note1 content'
    assert response_data['status'] == 'draft'
    assert response_data['user_id'] == test_note['user_id']
