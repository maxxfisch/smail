import os
import json
import tempfile
import shutil
from datetime import datetime
import pytest
from storage import Storage

@pytest.fixture
def temp_data_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def storage(temp_data_dir):
    return Storage(data_dir=temp_data_dir)

def test_init_creates_data_dir(temp_data_dir):
    Storage(data_dir=temp_data_dir)
    assert os.path.exists(temp_data_dir)

def test_load_profile_empty(storage):
    assert storage.load_profile() == {}

def test_save_and_load_profile(storage):
    test_profile = {
        "name": "Test User",
        "location": "Test City",
        "occupation": "Tester"
    }
    storage.save_profile(test_profile)
    
    loaded_profile = storage.load_profile()
    assert loaded_profile["name"] == "Test User"
    assert loaded_profile["location"] == "Test City"
    assert loaded_profile["occupation"] == "Tester"
    assert "last_updated" in loaded_profile

def test_get_context_for_prompt_empty(storage):
    assert storage.get_context_for_prompt() == ""

def test_get_context_for_prompt_with_data(storage):
    test_profile = {
        "name": "Test User",
        "location": "Test City",
        "occupation": "Tester",
        "interests": "Testing",
        "goals": "Write more tests",
        "preferences": "Python"
    }
    storage.save_profile(test_profile)
    
    context = storage.get_context_for_prompt()
    assert "Profile Information:" in context
    assert "Name: Test User" in context
    assert "Location: Test City" in context
    assert "Occupation: Tester" in context
    assert "Interests: Testing" in context
    assert "Goals: Write more tests" in context
    assert "Preferences: Python" in context