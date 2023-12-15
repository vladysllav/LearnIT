from typing import Optional, Union, List, Dict

from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import Course


class CourseFilter(Filter):
    name: Optional[str]
    description: Optional[str]
    is_active: Optional[bool]
    rating: Optional[float]

    class Constants(Filter.Constants):
        model = Course
        ordering_field_name = "order_by"
        search_field_name = "search"

    def filter_courses(self, db: Session, skip: int, limit: int) -> Union[List[Course], Dict[str, str]]:
        """
            Filters and retrieves courses based on the provided filter parameters.

            Args:
                db: SQLAlchemy Session object for database access.
                skip: The number of courses to skip before returning results (pagination).
                limit: The maximum number of courses to return.

            Returns:
                A list of `Course` objects if the filtering is successful, or a dictionary
                containing an error message if any errors occur.

            Raises:
                SQLAlchemyError: If any database-related error occurs during the filtering process.

            """

        try:
            query = db.query(Course)

            if self.name:
                query = query.filter(Course.name.ilike(f"%{self.name}%"))
            if self.description:
                query = query.filter(Course.description.ilike(f"%{self.description}%"))

            if self.is_active is not None:
                query = query.filter(Course.is_active == self.is_active)
            if self.rating is not None:
                query = query.filter(Course.rating == self.rating)

            courses = query.offset(skip).limit(limit).all()
            return courses

        except SQLAlchemyError as e:
            return {"error": str(e)}