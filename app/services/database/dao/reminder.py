from sqlalchemy import delete
from sqlalchemy.orm import sessionmaker

from app.models import dto, database
from app.models.database import User
from app.services.database.dao.base import BaseDAO


class ReminderDAO(BaseDAO[User]):
    """ORM queries for users table"""

    def __init__(self, session: sessionmaker):
        super().__init__(User, session)

    async def add_reminder(self, reminder: dto.Reminder) -> dto.Reminder:
        """
        Add user to database if not added yet. If added, tries to update parameters.
        :param reminder:
        """

        async with self._session() as session:
            await session.merge(_map_to_db_reminder(reminder))
            await session.commit()
            return reminder

    async def remove_reminder(self, reminder: dto.Reminder) -> dto.Reminder:
        """
        Removes reminder from database.
        :param reminder:
        :return reminder: dto
        """

        async with self._session() as session:
            await session.execute(
                delete(database.Reminder).where(database.Reminder == _map_to_db_reminder(reminder))
            )
            await session.commit()

        return reminder


def _map_to_db_reminder(reminder: dto.Reminder) -> database.Reminder:
    """
    Maps DTO -> database reminder
    :param reminder:
    :return: database reminder
    """

    return database.Reminder(
        user_id=reminder.owner_id,
        text=reminder.text,
        notify_time=reminder.notify_time
    )
