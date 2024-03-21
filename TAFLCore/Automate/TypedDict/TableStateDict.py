from typing import TypedDict


class TableStateDict(TypedDict):
    state: set[str]
    alias: str
    additional_info: str | None
