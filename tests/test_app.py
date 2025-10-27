import pytest
from app.main import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_index_page(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b"Available Trains" in res.data

def test_book_page(client):
    res = client.get('/book/1')
    assert res.status_code == 200
    assert b"Book Ticket for" in res.data

def test_confirm_page(client):
    res = client.get('/confirm')
    assert res.status_code == 200
