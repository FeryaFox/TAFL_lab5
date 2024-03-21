from typing import TypedDict
from .TableStateDict import TableStateDict


class AutomateDict(TypedDict):
    table_states: list[TableStateDict]
    table_signals: list[str]
    states: list[list[list[str]]]
