import json
import os
from datetime import datetime
from typing import Dict, Any

class Storage:
    def __init__(self, data_dir: str = "data") -> None:
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.profile_path = os.path.join(data_dir, "profile.json")

    def load_profile(self) -> Dict[str, Any]:
        if os.path.exists(self.profile_path):
            with open(self.profile_path, 'r') as f:
                return json.load(f)
        return {}

    def save_profile(self, profile_data: Dict[str, Any]) -> None:
        existing_data = self.load_profile()
        existing_data.update(profile_data)
        existing_data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.profile_path, 'w') as f:
            json.dump(existing_data, f, indent=2)

    def get_context_for_prompt(self) -> str:
        profile = self.load_profile()
        if not profile:
            return ""

        context = ["Profile Information:"]
        if profile.get('name'):
            context.append(f"Name: {profile['name']}")
        if profile.get('location'):
            context.append(f"Location: {profile['location']}")
        if profile.get('occupation'):
            context.append(f"Occupation: {profile['occupation']}")
        if profile.get('interests'):
            context.append(f"Interests: {profile['interests']}")
        if profile.get('goals'):
            context.append(f"Goals: {profile['goals']}")
        if profile.get('preferences'):
            context.append(f"Preferences: {profile['preferences']}")

        return "\n".join(context)