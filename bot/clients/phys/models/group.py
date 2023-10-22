from dataclasses import dataclass


@dataclass
class Group:
    group_name: str
    visit_value: float
    curator_guid: str
