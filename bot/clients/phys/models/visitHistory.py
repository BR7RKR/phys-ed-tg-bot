from dataclasses import dataclass
from datetime import date


@dataclass
class VisitHistory:
    date: date
    teacher_name: str
