from fastapi import Depends, HTTPException
from app.models.user import InvitationStatus, User
from app.repositories.base_repository import BaseRepository
from app.schemas.user import CreateUserToInvite, UserSignUp
from app.utils import generate_random_password, send_invitation_email
from app.core.security import create_activation_url, get_password_hash


class UserService:
    def __init__(self, user_repo: BaseRepository):
        self.user_repo = user_repo

    pass
    

class UserInvitationService:
    def __init__(self, user_repo: BaseRepository, invitation_repo: BaseRepository):
        self.user_repo = user_repo
        self.invitation_repo = invitation_repo

    
    def create_user(self, user_schema: CreateUserToInvite):
        user_data = user_schema.dict()
        user_data['hashed_password'] = get_password_hash(generate_random_password())
        user_data['is_active'] = False
        return self.user_repo.create(user_data)
    

    def create_invitation(self, user: User):
        invitation_data = {'email': user.email,
                      'user_id': user.id,
                      'status': InvitationStatus.active}
        return self.invitation_repo.create(invitation_data)
    

    def create_user_and_invite(self, user_schema: CreateUserToInvite):
        user = self.create_user(user_schema)

        activation_url = create_activation_url(user_id=user.id, user_email=user.email)
        send_invitation_email(email_to=user.email, url=activation_url)

        invitation = self.create_invitation(user)
        return user, invitation
    

    def activate_user(self, user_schema: UserSignUp, token_payload: dict):
        user_id = token_payload.get('sub')
        user_email = token_payload.get('email')
        
        user_data = user_schema.dict()
        user_data['hashed_password'] = get_password_hash(user_data.pop('password'))
        user_data['is_active'] = True
        self.user_repo.update(id=user_id, dict_data=user_data)

        invitation = self.invitation_repo.get_by_email(user_email)
        update_invitation = {'status': InvitationStatus.accepted}

        return self.invitation_repo.update(id=invitation.id, dict_data=update_invitation)


    

    

    

