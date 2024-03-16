from fastapi import HTTPException
import re

from app.models.user import Invitation, InvitationStatus, User
from app.repositories.base_repository import BaseRepository
from app.schemas.user import CreateUserToInvite, UserSignUp

from app.utils import generate_random_password, send_invitation_email
from app.core.security import create_activation_url, decode_access_token, get_password_hash, verify_password


class UserService:
    def __init__(self, user_repo: BaseRepository):
        self.user_repo = user_repo

    def create_user(self, user_schema: CreateUserToInvite) -> User:
        user = self.user_repo.get_by_email(email=user_schema.email)
        if user:
            raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
            )
        user_data = user_schema.dict()
        user_data['hashed_password'] = get_password_hash(generate_random_password())
        user_data['is_active'] = False

        user = self.user_repo.create(user_data)
        return user

    def authenticate(self, email: str, password: str) -> User:
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    def validate_password(self, password: str) -> tuple[bool, str]:
        if not re.search(r"\d", password):
            return False, "Password must contain at least one digit."
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter."
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter."

        return True, "Password is valid"


class InvitationService:
    def __init__(self, user_repo: BaseRepository, invitation_repo: BaseRepository):
        self.user_repo = user_repo
        self.invitation_repo = invitation_repo
        self.user_service = UserService(self.user_repo)

    def create_invitation(self, user: User) -> Invitation:
        invitation_data = {'email': user.email,
                      'user_id': user.id,
                      'status': InvitationStatus.active}
        invitation = self.invitation_repo.create(invitation_data)
        return invitation

    def invite_user(self, user: User) -> Invitation:
        activation_url = create_activation_url(user_id=user.id, user_email=user.email)
        send_invitation_email.apply_async(kwargs={'email_to': user.email, 'url': activation_url}, countdown=1)
        invitation = self.create_invitation(user)
        return invitation

    def activate_user(self, user_schema: UserSignUp, token: str) -> User:
        token_payload = decode_access_token(token)
        if not token_payload:
            raise HTTPException(status_code=401, detail="Token has expired")
        user_id = token_payload.get('sub')
        user_email = token_payload.get('email')

        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
            status_code=400,
            detail="User doesn't exists",
            )
        user_data = user_schema.dict()

        password = user_data.pop('password')
        validation_response, msg = self.user_service.validate_password(password)
        if not validation_response:
            raise HTTPException(status_code=400, detail=msg)

        user_data['hashed_password'] = get_password_hash(password)
        user_data['is_active'] = True
        user = self.user_repo.update(id=user_id, dict_data=user_data)

        invitation = self.invitation_repo.get_by_email(user_email)
        update_invitation = {'status': InvitationStatus.accepted}
        self.invitation_repo.update(id=invitation.id, dict_data=update_invitation)
        return user
