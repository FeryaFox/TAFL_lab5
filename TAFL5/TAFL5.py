from .TAFL5Saver import TAFL5Saver
from TAFLCore.Automate import Automate, TableState, AutomateUtils


class TAFL5:
    @staticmethod
    def construct_e_closures(automate: Automate) -> list[TableState]:
        e_closures: list[TableState] = []
        j = 0

        started_table_states_aliases = automate.get_started_table_state_aliases()

        achievable_started_table_states_aliases = []

        for alias in started_table_states_aliases:
            achievable_started_table_states_aliases.append(alias)
            if (i := automate[alias, "e"].value) is not None:
                achievable_started_table_states_aliases += i

        achievable_started_table_states_aliases = sorted(achievable_started_table_states_aliases)

        for alias in automate.get_states_alias():

            states = list(([alias] + list(automate[alias, "e"].value)))
            states.sort()

            is_start = False
            is_end = False

            for i in achievable_started_table_states_aliases:
                if i in states:
                    is_start = True

            for i in automate.get_states_alias():
                if len(states) == 1 and states[0] == i and automate.get_table_state_by_alias(i).is_end:
                    is_end = True

            e_closures.append(
                AutomateUtils.create_table_state_from_dict(
                    {
                        "state": states,
                        "alias": f"S{j}",
                        "additional_info": f"Ξ({alias})",
                        "is_start": is_start,
                        "is_end": is_end
                    }
                )
            )
            j += 1
        return e_closures

    @staticmethod
    def get_automaton_transition_table(automate: Automate, e_closures: list[TableState]) -> Automate:
        signals_name = automate.get_signals_name()
        signals_name.remove("e")
        transition_table = Automate(e_closures, signals_name)
        print(transition_table)
