"""
Base model for all models in the application
"""

import re

from sqlalchemy.ext.declarative import declared_attr
from sqlmodel import Field, SQLModel

pattern = re.compile(r"(?<!^)(?=[A-Z])")


class BaseModel(SQLModel):
    """
    Base model for all models.
    Attributes:
        id: The id of the model.
        created_at: The time the model was created.
        updated_at: The time the model was updated.
        is_active: The status of the model.
    """

    id: int = Field(
        default=None,
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
        description="The id of the model.",
    )
    is_active: bool = Field(
        default=True, nullable=True, description="The status of the model."
    )

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate the table name from the class name.
        :return: The table name.
        """
        return pattern.sub("_", cls.__name__).lower()
