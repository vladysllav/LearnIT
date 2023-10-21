import argparse

from app.db.session import SessionLocal
from app.crud.crud_user import user as user_crud
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.models.user import UserType


def create_superuser(email: str, password: str, first_name: str, last_name: str):
    db = SessionLocal()
    user = user_crud.get_by_email(db=db, email=email)
    
    if not user:
        superuser = UserCreate(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            type=UserType.superadmin
        )
        user_crud.create(db=db, obj_in=superuser)
        print('Superuser created successfully')
        
    else:
        print('Superuser with this email already exists')
        
    
def main():
    parser = argparse.ArgumentParser(description='Create superuser')
    parser.add_argument('email', type=str, help='Enter the email address for the superuser')
    parser.add_argument('password', type=str, help='Enter the password for the superuser')
    parser.add_argument('first_name', type=str, help='Enter your name')
    parser.add_argument('last_name', type=str, help='Enter your last name')
    
    args = parser.parse_args()
    
    email = args.email
    password = args.password
    first_name = args.first_name
    last_name = args.last_name
    
    create_superuser(email, password, first_name, last_name)
    

if __name__ == '__main__':
    main()
    
            
            

        