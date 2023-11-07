from fastapi import Depends, HTTPException
from app.models.user import InvitationStatus, User
from app.repositories.base_repository import BaseRepository
from app.schemas.user import CreateUserForInvitation, InvitationCreate
from app.utils import generate_random_password, send_invitation_email
from app.core.security import create_activation_url, get_password_hash


class UserService:
    def __init__(self, user_repo: BaseRepository):
        self.user_repo = user_repo


    def create_user(self, user: CreateUserForInvitation):
        user_data = user.dict()
        user = self.user_repo.get_by_email(user_data['email'])
        if user:
            raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
        user_data['hashed_password'] = get_password_hash(generate_random_password())
        schema = CreateUserForInvitation(**user_data)
        return self.user_repo.create(schema)

    

class InvitationService(UserService):
    def __init__(self, invitation_repo: BaseRepository):
        super().__init__(self.user_repo)
        self.invitation_repo = invitation_repo


    def create_invitation(self, user: User):
        invitation_data = {'email': user.email,
                      'user_id': user.id,
                      'status': InvitationStatus.active}
        schema = InvitationCreate(**invitation_data)
        return self.invitation_repo.create(schema)
    

    def create_user_and_invitate(self, user_schema: CreateUserForInvitation):
        user = self.create_user(user_schema)

        activation_url = create_activation_url(self, user_id=user.id, user_email=user.email)
        send_invitation_email(email_to=user.email, url=activation_url)

        invitation = self.create_invitation(user)
        return user, invitation

# class UserInvitationService:
#     def __init__(self, user_service: UserService = Depends(user_service),
#                  invitation_service: InvitationService = Depends(invitation_service)):
#         self.user_service = user_service
#         self.invitation_service = invitation_service

    
#     def create_user_and_invitate(self, user_schema: CreateUserForInvitation):
#         user = self.user_service.create_user(user_schema)

#         activation_url = create_activation_url(user_id=user.id, user_email=user.email)
#         send_invitation_email(email_to=user.email, url=activation_url)

#         invitation = self.invitation_service.create_invitation(user)

#         return user, invitation
        
    

