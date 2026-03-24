import pytest


def test_root_redirects_to_home(client, activities_backup):
    """Test that GET / redirects to /static/index.html"""
    # Arrange: Test client is ready
    
    # Act: Send GET request to root endpoint, don't follow redirects
    response = client.get("/", follow_redirects=False)
    
    # Assert: Verify redirect response
    assert response.status_code in [307, 308]  # Temporary or permanent redirect
    assert "location" in response.headers
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_with_follow(client, activities_backup):
    """Test that following root redirect leads to successful response"""
    # Arrange: Test client is ready
    
    # Act: Send GET request to root endpoint and follow redirects
    response = client.get("/", follow_redirects=True)
    
    # Assert: Verify we reach the static file (will be 200 or component-specific)
    assert response.status_code == 200
