"""
Tests for API routes timeline post functionality
"""
import pytest
from unittest.mock import patch, MagicMock
from app import create_app
from app.models.timelinepost import TimelinePost


@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


# Mock TimelinePost to avoid database connection issues
@pytest.fixture
def mock_timeline_post():
    with patch('app.routes.api.TimelinePost') as mock:
        yield mock


def test_post_timeline_post_success(client, mock_timeline_post):
    """Test successful post creation"""
    # Mock successful creation
    mock_post = MagicMock()
    mock_post.name = "John Doe"
    mock_post.email = "john@example.com"
    mock_post.content = "Test content"
    
    mock_timeline_post.select.return_value.where.return_value = []
    mock_timeline_post.create.return_value = mock_post
    
    with patch('app.routes.api.model_to_dict') as mock_model_to_dict:
        mock_model_to_dict.return_value = {
            "name": "John Doe",
            "email": "john@example.com", 
            "content": "Test content"
        }
        
        response = client.post('/api/timeline_post', data={
            'name': 'John Doe',
            'email': 'john@example.com',
            'content': 'Test content'
        })
        
        assert response.status_code == 200
        assert response.json['name'] == 'John Doe'


def test_post_timeline_post_duplicate_email_different_name(client, mock_timeline_post):
    """Test rejection when email exists with different name"""
    existing_post = MagicMock()
    existing_post.name = "Jane Doe"
    existing_post.email = "john@example.com"
    
    mock_timeline_post.select.return_value.where.return_value = [existing_post]
    
    response = client.post('/api/timeline_post', data={
        'name': 'John Doe',
        'email': 'john@example.com',
        'content': 'Test content'
    })
    
    assert response.status_code == 400
    assert response.json['error'] == "Email already associated with a different name"


def test_post_timeline_post_duplicate_name_different_email(client, mock_timeline_post):
    """Test rejection when name exists with different email"""
    existing_post = MagicMock()
    existing_post.name = "John Doe"
    existing_post.email = "jane@example.com"
    
    # Mock email query returns empty, name query returns existing post
    def mock_where(field_condition):
        if "email" in str(field_condition):
            return []
        else:  # name condition
            return [existing_post]
    
    mock_timeline_post.select.return_value.where.side_effect = mock_where
    
    response = client.post('/api/timeline_post', data={
        'name': 'John Doe',
        'email': 'john@example.com',
        'content': 'Test content'
    })
    
    assert response.status_code == 400
    assert response.json['error'] == "Name already associated with a different email"


def test_post_timeline_post_same_email_same_name(client, mock_timeline_post):
    """Test success when same email and same name (allowed)"""
    existing_post = MagicMock()
    existing_post.name = "John Doe"
    existing_post.email = "john@example.com"
    
    mock_timeline_post.select.return_value.where.return_value = [existing_post]
    
    new_post = MagicMock()
    new_post.name = "John Doe"
    new_post.email = "john@example.com"
    new_post.content = "Another post"
    
    mock_timeline_post.create.return_value = new_post
    
    with patch('app.routes.api.model_to_dict') as mock_model_to_dict:
        mock_model_to_dict.return_value = {
            "name": "John Doe",
            "email": "john@example.com",
            "content": "Another post"
        }
        
        response = client.post('/api/timeline_post', data={
            'name': 'John Doe',
            'email': 'john@example.com',
            'content': 'Another post'
        })
        
        assert response.status_code == 200
        assert response.json['name'] == 'John Doe'


def test_get_timeline_post_limit_50(client, mock_timeline_post):
    """Test that GET endpoint limits results to 50 posts"""
    # Create mock posts
    mock_posts = [MagicMock() for _ in range(60)]
    
    mock_query = MagicMock()
    mock_query.order_by.return_value.limit.return_value = mock_posts[:50]
    mock_timeline_post.select.return_value = mock_query
    
    with patch('app.routes.api.model_to_dict') as mock_model_to_dict:
        mock_model_to_dict.side_effect = lambda p: {"id": id(p)}
        
        response = client.get('/api/timeline_post')
        
        assert response.status_code == 200
        assert len(response.json['timeline_posts']) == 50
        
        # Verify limit was called
        mock_query.order_by.return_value.limit.assert_called_once_with(50)
