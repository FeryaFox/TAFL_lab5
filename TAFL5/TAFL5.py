from .TAFL5Saver import TAFL5Saver
from TAFLCore.Automate import Automate, TableState, AutomateUtils
from typing import TypedDict


def get_deltas(state: str, signal: str, result: list, automate: Automate, is_signal: bool) -> list:
    if (r := list(automate[state][signal].value)) and not is_signal:
        is_signal = True
        for i in r:
            result.append({
                "state": i,
                "signal": signal,
                "result": []
            })

    if r := list(automate[state]["e"].value):
        for i in r:
            result.append({
                "state": i,
                "signal": "e",
                "result": []
            })

    if len(result) > 0:
        for i in result:
            get_deltas(
                i["state"],
                signal,
                i["result"],
                automate,
                is_signal
            )
    return result


def transform_deltas(input_list):
    result_list = []

    for item in input_list:
        # Функция для сбора состояний и сигналов в рекурсии
        def collect_states_signals(item, states=[], signals=[]):
            states.append(item['state'])
            signals.append(item['signal'])
            for child in item['result']:
                collect_states_signals(child, states, signals)
            return {"states": states, "signals": signals}

        # Используем вспомогательную функцию для каждого элемента
        result = collect_states_signals(item, [], [])
        result_list.append(result)

    return result_list


def filter_signals_states(transformed_list):
    # Удаление словарей, где все сигналы равны 'e'
    new_list = [d for d in transformed_list if not all(signal == 'e' for signal in d['signals'])]

    # Удаление состояний, соответствующих 'e', если после них есть другие сигналы
    for d in new_list:
        e_indices = []
        for i, signal in enumerate(d['signals']):
            if signal == 'e':
                # Если 'e' не последний сигнал или за 'e' следуют не только сигналы 'e'
                if i < len(d['signals']) - 1 and not all(s == 'e' for s in d['signals'][i + 1:]):
                    e_indices.append(i)

        for index in sorted(e_indices, reverse=True):
            del d['states'][index]
            del d['signals'][index]

    return new_list


# Объединение состояний и удаление дубликатов
def combine_unique_states(filtered_list):
    return list(set(state for item in filtered_list for state in item['states']))


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


        signals_name = automate.get_signals_name().copy()
        signals_name.remove("e")
        transition_automate = Automate(e_closures, signals_name)

        e_states = []
        s_states = []
        for e_closure in e_closures:

            for signal in transition_automate.get_signals_name():
                e_states = []
                s_states = []
                for state in e_closure.state.value:

                    # print(f"({state}, {signal}) -> ", end="")
                    r = []
                    transformed_list = get_deltas(state, signal, r, automate, False)

                    transformed_list = transform_deltas(transformed_list)
                    # print(transformed_list)
                    filtered_list = filter_signals_states(transformed_list)
                    e_states += combine_unique_states(filtered_list)
                    # print(set(e_states))
                    # print()

                    # print("-"*100)
                e_states = set(e_states)
                for state in transition_automate.get_states_alias():
                    if e_states in transition_automate.get_table_state_by_alias(state):
                        s_states.append(state)

                transition_automate[e_closure.alias, signal].value = s_states

        return transition_automate
