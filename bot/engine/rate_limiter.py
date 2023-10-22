from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Optional, List

from engine.constants import MAX_REQUESTS
from engine.exceptions import RateLimitError


@dataclass
class User:
    user_tg_id: Optional[str] = None
    requests: int = 0
    update_date: Optional[datetime] = None


class RateLimiter:
    def __init__(self):
        self._users: List[User] = []

    def has_free_requests(self, user_tg_id):
        user_from_list = self._find_user(user_tg_id)

        if user_from_list is None:
            return True

        if user_from_list.update_date is None:
            return True

        current_time = datetime.now()
        if (current_time - user_from_list.update_date) > timedelta(hours=24):
            return True

        if user_from_list.requests < MAX_REQUESTS:
            return True

        return False

    def add_request(self, user_tg_id):
        user_from_list = self._find_user(user_tg_id)
        if user_from_list is None:
            user = User(user_tg_id, 1, datetime.now())
            self._users.append(user)
            return

        current_time = datetime.now()
        if user_from_list.requests >= MAX_REQUESTS:
            if (current_time - user_from_list.update_date) < timedelta(hours=24):
                raise RateLimitError()
            else:
                user_from_list.requests = 0

        user_from_list.update_date = current_time
        user_from_list.requests += 1

    def _find_user(self, user_tg_id) -> Optional[User]:
        for u in self._users:
            if u.user_tg_id != user_tg_id:
                continue

            return u

        return None
