import json
import os
from datetime import datetime
from typing import Dict, Any

class Storage:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.profile_path = os.path.join(data_dir, "profile.json")
        self.load_profile()

    def load_profile(self) -> Dict[str, Any]:
        if os.path.exists(self.profile_path):
            with open(self.profile_path, 'r') as f:
                return json.load(f)
        return {}

    def save_profile(self, profile_data: Dict[str, Any]) -> None:
        with open(self.profile_path, 'w') as f:
            json.dump(profile_data, f, indent=2)

    def get_context_for_prompt(self) -> str:
        """Generate a context string from the profile data"""
        profile = self.load_profile()
        if not profile:
            return ""

        context = [
            "Here is some important information about me:",
            f"My name is {profile.get('name', 'unknown')}",
            f"I live in {profile.get('location', 'unknown')}",
            f"I work/study as {profile.get('occupation', 'unknown')}",
            "",
            "My interests and hobbies include:",
            profile.get('interests', 'unknown'),
            "",
            "My current goals are:",
            profile.get('goals', 'unknown'),
            "",
            "My preferences:",
            profile.get('preferences', 'unknown')
        ]

        return "\n".join(context)