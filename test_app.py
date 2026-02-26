"""
Simple tests for the Flask application.
Run with: python -m pytest test_app.py
"""
import pytest
import json
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_hello_world(client):
    """Test the hello world endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['message'] == 'Hello, World!'
    assert data['status'] == 'success'


def test_health(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['service'] == 'otel-python-example'


def test_process(client):
    """Test the process endpoint with custom spans."""
    response = client.get('/process')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'completed'
    assert data['processed_items'] == 5
    assert data['original_items'] == 5


def test_process_response_structure(client):
    """Test that process endpoint returns expected structure."""
    response = client.get('/process')
    data = json.loads(response.data)
    
    # Verify all expected keys are present
    assert 'status' in data
    assert 'processed_items' in data
    assert 'original_items' in data
