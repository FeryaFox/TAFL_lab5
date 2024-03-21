from _ast import alias
from dataclasses import dataclass
from prettytable import PrettyTable


@dataclass
class State:
    value: set[str]

    def __str__(self) -> str:
        return f"{[", ".join(self.value)]}"

    def __contains__(self, item: list[str] | set[str] | str) -> bool:
        if isinstance(item, str):
            return item in self.value
        return self.to_set().issubset(set(item))


@dataclass
class TableState:

    state: State
    alias: str | None = None
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
    states: list[State] # stop here
    __signals: list[str]
    __state: State
    value: dict[str, State]

    @property
    def signals(self) -> list[str]:
        return self.__signals

    @signals.setter
    def signals(self, value: list[str]) -> None:
        if self.__signals is not None:
            raise AttributeError("Сигнал уже было задано и не может быть изменено.")
        self.__signals = value

    @property
    def state(self) -> str:
        return self.__state

    @state.setter
    def state(self, value: str) -> None:
        if self.__state is not None:
            raise AttributeError("Состояние уже было задано и не может быть изменено.")
        self.__state = value

    def __str__(self) -> str:
        return f"{self.__state}: {self.value}"


class Automate:
    __signals: list[str]
    __states: list[str]
    __matrix: dict[str, dict[str, Cell]] = {}

    def __init__(
            self,
            states: list[str] | None = None,
            signals: list[str] | None = None,
            a_dict: dict[str, dict[str, list[str]]] | None = None
    ) -> None:
        if states is not None and signals is not None:
            self.__signals = signals
            self.__states = states
            self.__fill_clear_matrix()
        elif a_dict is not None:
            self.__states = [_ for _ in a_dict]
            self.__signals = [_ for _ in a_dict[list(a_dict.keys())[0]]]
            self.__fill_clear_matrix()
            for state in self.__states:
                for signal in self.__signals:
                    self.__setitem__((state, signal), a_dict[state][signal])

    def __fill_clear_matrix(self):
        for state in self.__states:
            for signal in self.__signals:
                self.__matrix[state] = {}
                self.__matrix[state][signal] = Cell(state, signal, [])

    def __getitem__(self, item: str | tuple[str, str]) -> AutomateRow | Cell:
        if isinstance(item, tuple) and len(item) == 2:
            return self.__matrix[item[0]][item[1]]
        elif isinstance(item, str):
            return AutomateRow(self.__signals, self.__states[self.__states.index(item)], self.__matrix[item])
        else:
            raise KeyError("Неверный индекс")

    def __setitem__(self, item: tuple[str, str], value: list[str] | Cell) -> None:
        if isinstance(item, tuple) and len(item) == 2:
            if isinstance(value, Cell):
                self.__matrix[item[0]][item[1]] = value
            else:
                if item[0] not in self.__states:
                        raise KeyError("Попытка присвоить несуществующее состоянии")
                if item[1] not in self.__signals:
                        raise KeyError("Попытка присвоить несуществующий сигнал")
                for i in value:
                    if i not in self.__states:
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
