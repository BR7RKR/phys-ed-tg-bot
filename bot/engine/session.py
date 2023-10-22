from typing import List, Optional

from engine.exceptions import SessionIsBusyError


class SessionEntity:
    def __init__(self):
        self.session_name: Optional[str] = None
        self.chat_id: Optional[str] = None
        self.additional_info: Optional = None


class BotSessionsBase:
    def __init__(self):
        self._sessions: List[SessionEntity] = []

    def start(self, session: SessionEntity):
        for s in self._sessions:
            if s.chat_id == session.chat_id:
                if s.session_name is not None:
                    raise SessionIsBusyError(s.session_name)

                s.session_name = session.session_name
                return

        self._sessions.append(session)

    def end(self, session: SessionEntity):
        for s in self._sessions:
            if s.chat_id != session.chat_id:
                continue

            if s.session_name != session.session_name:
                continue

            self._sessions.remove(s)
            return

    def get_current_session(self, chat_id):
        for s in self._sessions:
            if s.chat_id != chat_id:
                continue

            return s

        return None
