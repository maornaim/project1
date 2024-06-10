import pytest
from app import app, collection  # Adjust the import if needed based on the location of app.py
from unittest.mock import patch

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<form" in response.data  # Check if the form is in the rendered HTML

def test_add(client):
    with patch('app.collection.insert_one') as mock_insert:
        response = client.post("/add", data={"num1": "2", "num2": "3"})
        assert response.status_code == 200
        assert b"5" in response.data  # Check if the result 5 is in the rendered HTML

        # Check if the data is inserted into MongoDB
        assert mock_insert.called
        args, kwargs = mock_insert.call_args
        assert args[0]['num1'] == "2"
        assert args[0]['num2'] == "3"
        assert args[0]['result'] == 5
