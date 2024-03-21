from dataclasses import dataclass
from prettytable import PrettyTable
from .TypedDict import *
from .utils import AutomateUtils


@dataclass
class State:
    value: set[str]

    def __str__(self) -> str:
        return f"{[", ".join(self.value)]}"

    def __contains__(self, item: list[str] | set[str] | str) -> bool:
        if isinstance(item, str):
            return item in self.value
        return self.value.issubset(set(item))

    def append(self, item: set[str] | str) -> None:
        if isinstance(item, str):
            self.value.add(item)
        elif isinstance(item, set):
            self.value += item


@dataclass
class TableState:

    state: State
    alias: str
    additional_info: str | None = None

    def __str__(self) -> str:
        if self.alias is not None and self.additional_info is not None:
            return f"{self.alias} = {self.additional_info} = {{ {str(self.state)} }}"
        elif self.alias is None and self.additional_info is not None:
            return f"{self.additional_info} = {{ {str(self.state)} }}"
        elif self.alias is not None and self.additional_info is None:
            return f"{self.alias} = {{ {str(self.state)} }}"
        elif self.alias is None and self.additional_info is None:
            return f"{{ {str(self.state)} }}"

    def __contains__(self, item: list[str] | State) -> bool:
        item_ = item
        if isinstance(item, State):
            item_ = item.value
        return self.state.value.issubset(set(item_))


@dataclass
class AutomateRow:
    table_state: TableState
    signals: list[str]
    states: list[State]

    def __getitem__(self, item: str) -> State:
        return self.states[self.signals.index(item)]

    def __str__(self) -> str:
        table = PrettyTable()
        table.field_names = [""] + self.signals
        table.add_row(
            [str(self.table_state)] + [self.states[_] for _ in self.states]
        )
        return str(table)


class Automate:
    __signals: list[str]
    __states: list[TableState]
    __matrix: list[list[State]] = []

    def __init__(
            self,
            states: list[TableState] | list[TableStateDict] | None = None,
            signals: list[str] | None = None,
            automate_dict: AutomateDict | None = None
    ) -> None:
        if states is not None and signals is not None:
            self.__signals = signals
            if isinstance(states[0], TableState):
                self.__states = states
            elif isinstance(states[0], TableStateDict):
                self.__states = [AutomateUtils.create_table_state_from_dict(_) for _ in states]
            self.__fill_clear_matrix()
        elif automate_dict is not None:
            self.__states = [AutomateUtils.create_table_state_from_dict(_) for _ in automate_dict["table_states"]]
            self.__signals = automate_dict["table_signals"]
            self.__fill_clear_matrix()

            for state in self.__states:
                for signal in self.__signals:
                    self.__setitem__(
                        (state.alias, signal),
                        automate_dict["states"][self.__get_state_index_by_alias(state.alias)][self.__get_signal_index_by_name(signal)]
                    )

    def __get_state_index_by_alias(self, item: str) -> int:
        index = 0
        for state in self.__states:
            if state.alias == item:
                return index
            index += 1

    def __get_signal_index_by_name(self, name: str) -> int:
        index = 0
        for signal in self.__signals:
            if signal == name:
                return index
            index += 1

    def __fill_clear_matrix(self):
        for state in self.__states:
            row = []
            for signal in self.__signals:
                row.append(State(set([])))
            self.__matrix.append(row)

    def __getitem__(self, item: str | tuple[str, str]) -> AutomateRow | State:
        if isinstance(item, tuple) and len(item) == 2:
            return self.__matrix[item[0]][item[1]]
        elif isinstance(item, str):
            c_state_alias = self.__get_state_index_by_alias(item[0])
            return AutomateRow(
                self.__states[c_state_alias],
                self.__signals,
                self.__matrix[self.__get_state_index_by_alias(item[0])]
            )
        else:
            raise KeyError("Неверный индекс")

    def __setitem__(self, item: tuple[str, str], value: list[str] | State) -> None:
        if isinstance(item, tuple) and len(item) == 2:
            if isinstance(value, State):
                self.__matrix[self.__get_state_index_by_alias(item[0])][self.__get_signal_index_by_name(item[1])] = value
            else:
                for state in self.__states:
                    if state == item[0]:
                        break
                else:
                    raise KeyError("Попытка присвоить несуществующее состоянии")
                if item[1] not in self.__signals:
                        raise KeyError("Попытка присвоить несуществующий сигнал")
                for i in value:
                    if i not in self.__state: # stop here
                        raise KeyError("Попытка присвоить несуществующий сигнал")
                self.__matrix[item[0]][item[1]] = Cell(item[0], item[1], value)
        else:
            raise KeyError("Неверный индекс")

    def __str__(self) -> str:
        table = PrettyTable()
        table.field_names = [""] + self.__signals
        for row in self.__matrix:
            table.add_row(
                [row] + self.__get_row_element(row)
            )
        return str(table)

    def __get_row_element(self, index: str) -> list[str]:
        return [", ".join(x) if (x := self.__matrix[index][_].value) != [] else "*" for _ in self.__matrix[index]]

    def to_dict(self) -> dict[str, dict[str, list[str]]]:
        d = {}
        for row in self.__matrix:
            d[row] = {}
            for column in self.__matrix[row]:
                d[row][column] = self.__matrix[row][column].value

        return d

    @staticmethod
    def dict_to_str_table(d: dict[str, dict[str, list[str]]]) -> str:

        table = PrettyTable()
        states = [_ for _ in d]
        signals = [_ for _ in d[list(d.keys())[0]]]

        table.field_names = [""] + signals

        for state in states:
            ag = [state] + [", ".join(x) if (x := d[state][_]) != [] else "*" for _ in d[state]]
            table.add_row(
                ag
            )
        return str(table)


a =     {"q0": {"a": ["q1"], "b": ["q1"]}, "q1": {"a": ["q0"], "b": ["q1"]}}
print(Automate.dict_to_str_table( a))
