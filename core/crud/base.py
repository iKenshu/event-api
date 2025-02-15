"""
This is the base crud file.
"""

from typing import Any, Generic, List, Optional, TypeVar

import strawberry
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel as PydanticBaseModel
from sqlmodel import Session, select

from core.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=PydanticBaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=PydanticBaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    A base class for CRUD operations.
    Attributes:
        model: The database model to perform CRUD operations on.
    """

    def __init__(self, model: ModelType):
        """
        Initialize the CRUD operations.

        Args:
            model: The database model to perform CRUD operations
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Get a model by id.

        Args:
            db: The database session.
            id: The id of the model to get.

        Returns:
            The model with the given id.
        """
        statement = select(self.model).where(
            self.model.id == id, self.model.is_active == True
        )
        return db.exec(statement).one_or_none()

    def all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        alive_only: bool = True,
    ) -> List[ModelType]:
        """
        Get all models.

        Args:
            db: The database session.

        Returns:
            All models.
        """
        statement = select(self.model)
        if alive_only:
            statement = statement.where(self.model.is_active == True)
        statement = statement.offset(skip).limit(limit)
        results = db.exec(statement).all()
        return results

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new model.

        Args:
            db: The database session.
            obj_in: The model to create.

        Returns:
            The created model.
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        """
        Update a model.

        Args:
            db: The database session.
            db_obj: The model to update.
            obj_in: The updated model.

        Returns:
            The updated model.
        """
        if isinstance(obj_in, BaseModel):
            update_data = obj_in.model_dump(exclude_unset=True)
        else:
            update_data = {
                key: value
                for key, value in obj_in.__dict__.items()
                if value is not None
            }

        obj_data = jsonable_encoder(db_obj)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: Any) -> ModelType:
        """
        Delete a model.

        Args:
            db: The database session.
            id: The id of the model to remove.

        Returns:
            The removed model.
        """
        statement = select(self.model).where(self.model.id == id)
        db_obj = db.exec(statement).one_or_none()
        if not db_obj:
            return None
        db_obj.is_active = False
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def hard_delete(self, db: Session, id: Any) -> ModelType:
        """
        Hard delete a model.

        Args:
            db: The database session.
            id: The id of the model to remove.

        Returns:
            The removed model.
        """
        statement = select(self.model).where(self.model.id == id)
        db_obj = db.exec(statement).one_or_none()
        if not db_obj:
            return None
        db.delete(db_obj)
        db.commit()
        return db_obj
