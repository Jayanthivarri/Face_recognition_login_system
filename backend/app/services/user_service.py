"""
User Service - Business logic for user management
Handles user creation, retrieval, and database operations
"""

import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.utils.exceptions import (
    ValidationException,
    NotFoundError,
    DuplicateError,
    InternalServerError
)

logger = logging.getLogger(__name__)


class UserService:
    """
    Service for user management operations.
    
    Handles database operations for user creation, retrieval,
    and management.
    """

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """
        Create a new user in the database.
        
        Args:
            db: SQLAlchemy database session
            user_data: UserCreate schema with user details
            
        Returns:
            Created User model instance
            
        Raises:
            DuplicateError: If email already exists
            InternalServerError: If database operation fails
        """
        try:
            # Check if email already exists
            existing_user = db.query(User).filter(User.email == user_data.email).first()
            if existing_user:
                logger.warning(f"Registration attempt with existing email: {user_data.email}")
                raise DuplicateError(
                    message="User with this email already exists",
                    error_code="USER_EMAIL_EXISTS"
                )
            
            # Create new user
            db_user = User(
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                email=user_data.email,
                age=user_data.age,
                face_embedding=user_data.face_embedding
            )
            
            # Add and commit to database
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            
            logger.info(f"User created successfully: {db_user.id} ({user_data.email})")
            return db_user
            
        except DuplicateError:
            raise
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Database integrity error during user creation: {str(e)}")
            raise DuplicateError(
                message="User creation failed - duplicate data",
                error_code="DATABASE_INTEGRITY_ERROR"
            )
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating user: {str(e)}")
            raise InternalServerError(
                message="Failed to create user",
                details=str(e)
            )

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """
        Retrieve user by ID.
        
        Args:
            db: SQLAlchemy database session
            user_id: User ID
            
        Returns:
            User model instance
            
        Raises:
            NotFoundError: If user not found
        """
        try:
            user = db.query(User).filter(User.id == user_id).first()
            
            if not user:
                logger.warning(f"User not found: {user_id}")
                raise NotFoundError(
                    message="User not found",
                    error_code="USER_NOT_FOUND"
                )
            
            logger.debug(f"Retrieved user: {user_id}")
            return user
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error retrieving user {user_id}: {str(e)}")
            raise InternalServerError(
                message="Failed to retrieve user",
                details=str(e)
            )

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Retrieve user by email.
        
        Args:
            db: SQLAlchemy database session
            email: User email
            
        Returns:
            User model instance or None if not found
            
        Raises:
            InternalServerError: If database operation fails
        """
        try:
            user = db.query(User).filter(User.email == email).first()
            logger.debug(f"Retrieved user by email: {email}")
            return user
            
        except Exception as e:
            logger.error(f"Error retrieving user by email {email}: {str(e)}")
            raise InternalServerError(
                message="Failed to retrieve user",
                details=str(e)
            )

    @staticmethod
    def get_all_users(db: Session) -> List[User]:
        """
        Retrieve all users from database.
        
        Args:
            db: SQLAlchemy database session
            
        Returns:
            List of User model instances
            
        Raises:
            InternalServerError: If database operation fails
        """
        try:
            users = db.query(User).all()
            logger.debug(f"Retrieved {len(users)} users")
            return users
            
        except Exception as e:
            logger.error(f"Error retrieving all users: {str(e)}")
            raise InternalServerError(
                message="Failed to retrieve users",
                details=str(e)
            )

    @staticmethod
    def get_users_with_embeddings(db: Session) -> List[tuple]:
        """
        Retrieve all users with their face embeddings.
        
        Optimized for face matching operations.
        Returns tuples of (user_id, embedding) for efficient processing.
        
        Args:
            db: SQLAlchemy database session
            
        Returns:
            List of (user_id, embedding) tuples
            
        Raises:
            InternalServerError: If database operation fails
        """
        try:
            users = db.query(User.id, User.face_embedding).all()
            logger.debug(f"Retrieved embeddings for {len(users)} users")
            return users
            
        except Exception as e:
            logger.error(f"Error retrieving embeddings: {str(e)}")
            raise InternalServerError(
                message="Failed to retrieve embeddings",
                details=str(e)
            )

    @staticmethod
    def user_exists(db: Session, email: str) -> bool:
        """
        Check if user with email exists.
        
        Args:
            db: SQLAlchemy database session
            email: User email
            
        Returns:
            bool: True if user exists, False otherwise
        """
        try:
            exists = db.query(User).filter(User.email == email).first() is not None
            logger.debug(f"User exists check: {email} = {exists}")
            return exists
            
        except Exception as e:
            logger.error(f"Error checking user existence: {str(e)}")
            return False

    @staticmethod
    def get_user_count(db: Session) -> int:
        """
        Get total number of users in database.
        
        Args:
            db: SQLAlchemy database session
            
        Returns:
            int: Total user count
            
        Raises:
            InternalServerError: If database operation fails
        """
        try:
            count = db.query(User).count()
            logger.debug(f"Total users in database: {count}")
            return count
            
        except Exception as e:
            logger.error(f"Error counting users: {str(e)}")
            raise InternalServerError(
                message="Failed to count users",
                details=str(e)
            )

    @staticmethod
    def get_user_profile(db: Session, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user profile information (without face embedding).
        
        Args:
            db: SQLAlchemy database session
            user_id: User ID
            
        Returns:
            Dict with user profile or None if not found
        """
        try:
            user = db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return None
            
            profile = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "age": user.age,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
            
            logger.debug(f"Retrieved profile for user {user_id}")
            return profile
            
        except Exception as e:
            logger.error(f"Error retrieving profile for user {user_id}: {str(e)}")
            return None

    @staticmethod
    def to_dict(user: User, include_embedding: bool = False) -> Dict[str, Any]:
        """
        Convert User model to dictionary.
        
        Args:
            user: User model instance
            include_embedding: Whether to include face embedding
            
        Returns:
            Dictionary representation of user
        """
        data = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "age": user.age,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
        
        if include_embedding:
            data["face_embedding"] = user.face_embedding
        
        return data
