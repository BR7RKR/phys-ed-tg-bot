from dataclasses import dataclass
from typing import List

from .group import Group
from .visitHistory import VisitHistory


@dataclass
class Student:
    group: Group
    additional_points: int
    points_for_standard: int
    visits: int
    visits_history: List[VisitHistory]
