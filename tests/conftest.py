"""
Pytest configuration and fixtures for FastAPI testing.

This module provides shared fixtures for testing the Mergington High School API,
including a test client and database fixtures.
"""

import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """
    Provides a TestClient for making HTTP requests to the FastAPI application.
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Automatically resets the activities database to its initial state before each test.
    This ensures test isolation and prevents state leakage between tests.
    """
    # Store original state
    original_activities = deepcopy(activities)

    yield

    # Reset to original state after test
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def sample_email():
    """Provides a sample email for testing student signup operations."""
    return "test.student@mergington.edu"


@pytest.fixture
def existing_email():
    """Provides an email of a student already signed up for an activity."""
    return "michael@mergington.edu"


@pytest.fixture
def sample_activity_name():
    """Provides a valid activity name for testing."""
    return "Chess Club"


@pytest.fixture
def nonexistent_activity_name():
    """Provides an invalid activity name for testing error cases."""
    return "Nonexistent Activity"