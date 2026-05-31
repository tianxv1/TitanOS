from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
import uuid
import json
import os


@dataclass
class User:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    username: str = ""
    email: str = ""
    password_hash: str = ""
    full_name: str = ""
    avatar_url: Optional[str] = None
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "avatar_url": self.avatar_url,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        data = data.copy()
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if isinstance(data.get("updated_at"), str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        return cls(**data)


class UserStore:
    def __init__(self, storage_path: str = "database/users.json"):
        self.storage_path = storage_path
        self.users: Dict[str, User] = {}
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for user_data in data.get("users", []):
                        user = User.from_dict(user_data)
                        self.users[user.id] = user
            except Exception:
                pass

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        data = {
            "users": [u.to_dict() for u in self.users.values()],
            "saved_at": datetime.now().isoformat()
        }
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_user(self, username: str, email: str, password_hash: str,
                 full_name: str = "") -> User:
        if any(u.username == username for u in self.users.values()):
            raise ValueError("Username already exists")

        if any(u.email == email for u in self.users.values()):
            raise ValueError("Email already registered")

        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            full_name=full_name
        )
        self.users[user.id] = user
        self._save()
        return user

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        for user in self.users.values():
            if user.username == username:
                return user
        return None

    def update_user(self, user_id: str, **kwargs) -> bool:
        user = self.users.get(user_id)
        if not user:
            return False

        if "username" in kwargs:
            user.username = kwargs["username"]
        if "email" in kwargs:
            user.email = kwargs["email"]
        if "password_hash" in kwargs:
            user.password_hash = kwargs["password_hash"]
        if "full_name" in kwargs:
            user.full_name = kwargs["full_name"]
        if "avatar_url" in kwargs:
            user.avatar_url = kwargs["avatar_url"]
        if "is_active" in kwargs:
            user.is_active = kwargs["is_active"]

        user.updated_at = datetime.now()
        self._save()
        return True

    def delete_user(self, user_id: str) -> bool:
        if user_id in self.users:
            del self.users[user_id]
            self._save()
            return True
        return False

    def list_users(self) -> list:
        return [u.to_dict() for u in self.users.values()]

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_users": len(self.users),
            "active_users": sum(1 for u in self.users.values() if u.is_active)
        }
