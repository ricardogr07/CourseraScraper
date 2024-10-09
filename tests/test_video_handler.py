import pytest
import os
from unittest.mock import patch, mock_open
from src.handlers.video_handler import VideoHandler

# Test video URL
VIDEO_URL = "https://d3c33hcgiwev3.cloudfront.net/61235b4c-7330-4e92-9952-94f43e80a428_76cceeb3f26746e18cbfa1b6b7da8f9d_GMT20241007-210427_Recording_1920x1080_WEBM_720.webm?Expires=1728604800&Signature=QVqWE-S3w9076BAc2kqLXccdFKe0JIIkM~k~dqt-6rZFxjbApqOhyRPGKmPBfvJwXVISX9fjX~V6mGpwFdEz-eLCtwERD8K9GtVhTJCb3mY5H1WjaCSs3B5kRO0RfuTrHM~y40D3jyXzP2UHf~gWhS84qxOxKldlCS3z21al-LY_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"

# Mock response for download
class MockResponse:
    @staticmethod
    def iter_content(chunk_size=1):
        return iter([b"some binary data"])
    
    @staticmethod
    def raise_for_status():
        pass  # Simulate a successful status code

@pytest.fixture
def video_handler():
    """Fixture for VideoHandler."""
    return VideoHandler(VIDEO_URL)

@patch('requests.get')
def test_download_video(mock_get, video_handler):
    # Mock the requests.get call to return a mocked response
    mock_get.return_value = MockResponse()
    
    file_name = video_handler.download_video()
    
    # Check if the file path returned is correct
    expected_file_name = VIDEO_URL.split("/")[-1].split("?")[0]
    assert file_name == expected_file_name, "The video handler should return the correct file name"
    
    # Check if the file is created
    assert os.path.exists(file_name), "The video file should be created"

    # Clean up the downloaded file after test
    os.remove(file_name)

