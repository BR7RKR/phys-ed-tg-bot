from datetime import datetime

from .models import VisitHistory, Student
from .models.group import Group


class PhysEdJournalClient:
    def __init__(self, session):
        self._SERVER_URL = "https://api.mospolytech.ru/physedjournal/graphql"
        self._session = session

    async def get_student(self, guid: str):
        query = f'''{{
            student(guid: "{guid}"){{
                group{{
                    groupName
                    curatorGuid
                    visitValue
                }}
                additionalPoints
                pointsForStandards
                visits                
                visitsHistory{{
                    date
                    teacher{{
                        fullName
                    }}
                }}
            }}
        }}
        '''

        async with self._session.post(self._SERVER_URL, json={"query": query}) as resp:
            resp_json = await resp.json()
            data = resp_json["data"]["student"]

            visits = []
            for visit in data["visitsHistory"]:
                visits.append(
                    VisitHistory(
                        datetime.strptime(visit["date"], "%m/%d/%Y").date(),
                        visit["teacher"]["fullName"],
                    )
                )

            group_data = data['group']
            group = Group(
                group_data['groupName'],
                group_data['visitValue'],
                group_data['curatorGuid']
            )

            return Student(
                group,
                data["additionalPoints"],
                data["pointsForStandards"],
                data["visits"],
                visits,
            )
