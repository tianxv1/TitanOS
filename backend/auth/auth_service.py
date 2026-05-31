from typing import Optional, Dict, Any
from datetime import timedelta
from .user_store import UserStore, User
from .jwt import JWTManager


class AuthService:
    def __init__(self):
        self.user_store = UserStore()
        self.jwt_manager = JWTManager()

    def register(self, username: str, email: str, password: str,
                 full_name: str = "") -> Dict[str, Any]:
        try:
            password_hash = self.jwt_manager.get_password_hash(password)
            user = self.user_store.add_user(username, email, password_hash, full_name)

            access_token = self.jwt_manager.create_access_token(
                data={"sub": user.id, "username": user.username}
            )

            return {
                "status": "success",
                "message": "User registered successfully",
                "user": user.to_dict(),
                "access_token": access_token,
                "token_type": "bearer"
            }
        except ValueError as e:
            return {"status": "error", "message": str(e)}

    def login(self, email: str, password: str) -> Dict[str, Any]:
        user = self.user_store.get_user_by_email(email)
        if not user:
            return {"status": "error", "message": "Invalid email or password"}

        if not user.is_active:
            return {"status": "error", "message": "User account is inactive"}

        if not self.jwt_manager.verify_password(password, user.password_hash):
            return {"status": "error", "message": "Invalid email or password"}

        access_token = self.jwt_manager.create_access_token(
            data={"sub": user.id, "username": user.username}
        )

        return {
            "status": "success",
            "message": "Login successful",
            "user": user.to_dict(),
            "access_token": access_token,
            "token_type": "bearer"
        }

    def login_by_username(self, username: str, password: str) -> Dict[str, Any]:
        user = self.user_store.get_user_by_username(username)
        if not user:
            return {"status": "error", "message": "Invalid username or password"}

        if not user.is_active:
            return {"status": "error", "message": "User account is inactive"}

        if not self.jwt_manager.verify_password(password, user.password_hash):
            return {"status": "error", "message": "Invalid username or password"}

        access_token = self.jwt_manager.create_access_token(
            data={"sub": user.id, "username": user.username}
        )

        return {
            "status": "success",
            "message": "Login successful",
            "user": user.to_dict(),
            "access_token": access_token,
            "token_type": "bearer"
        }

    def verify_token(self, token: str) -> Dict[str, Any]:
        if not self.jwt_manager.validate_token(token):
            return {"status": "error", "message": "Invalid or expired token"}

        payload = self.jwt_manager.decode_access_token(token)
        user_id = payload.get("sub")

        user = self.user_store.get_user_by_id(user_id)
        if not user:
            return {"status": "error", "message": "User not found"}

        return {
            "status": "success",
            "user": user.to_dict()
        }

    def refresh_token(self, token: str) -> Dict[str, Any]:
        if not self.jwt_manager.validate_token(token):
            return {"status": "error", "message": "Invalid or expired token"}

        payload = self.jwt_manager.decode_access_token(token)
        user_id = payload.get("sub")
        username = payload.get("username")

        new_token = self.jwt_manager.create_access_token(
            data={"sub": user_id, "username": username}
        )

        return {
            "status": "success",
            "access_token": new_token,
            "token_type": "bearer"
        }

    def change_password(self, user_id: str, old_password: str, new_password: str) -> Dict[str, Any]:
        user = self.user_store.get_user_by_id(user_id)
        if not user:
            return {"status": "error", "message": "User not found"}

        if not self.jwt_manager.verify_password(old_password, user.password_hash):
            return {"status": "error", "message": "Old password is incorrect"}

        new_password_hash = self.jwt_manager.get_password_hash(new_password)
        self.user_store.update_user(user_id, password_hash=new_password_hash)

        return {"status": "success", "message": "Password changed successfully"}

    def get_user(self, user_id: str) -> Optional[User]:
        return self.user_store.get_user_by_id(user_id)

    def update_profile(self, user_id: str, **kwargs) -> Dict[str, Any]:
        success = self.user_store.update_user(user_id, **kwargs)
        if not success:
            return {"status": "error", "message": "User not found"}

        user = self.user_store.get_user_by_id(user_id)
        return {"status": "success", "user": user.to_dict()}

    def delete_user(self, user_id: str, password: str) -> Dict[str, Any]:
        user = self.user_store.get_user_by_id(user_id)
        if not user:
            return {"status": "error", "message": "User not found"}

        if not self.jwt_manager.verify_password(password, user.password_hash):
            return {"status": "error", "message": "Incorrect password"}

        self.user_store.delete_user(user_id)
        return {"status": "success", "message": "User deleted successfully"}

    def get_stats(self) -> Dict[str, Any]:
        return self.user_store.get_stats()
