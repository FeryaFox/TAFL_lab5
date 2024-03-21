from TAFLCore.Automate.TypedDict import TableStateDict
from TAFLCore.Automate import TableState


class AutomateUtils:
    @staticmethod
    def create_table_state_from_dict(table_state_dict: TableStateDict) -> TableState:
        return TableState(**table_state_dict)
