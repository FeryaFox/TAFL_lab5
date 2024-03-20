from dataclasses import dataclass
from prettytable import PrettyTable


@dataclass
class Cell:
    __signal: str
    __state: str
    value: list[str]

    @property
    def signal(self) -> str:
        return self.__signal

    @signal.setter
    def signal(self, value: str) -> None:
        if self.__signal is not None:
            raise AttributeError("Сигнал уже было задано и не может быть изменено.")
        self.__signal = value

    @property
    def state(self) -> str:
        return self.__state

    @state.setter
    def state(self, value: str) -> None:
        if self.__state is not None:
            raise AttributeError("Состояние уже было задано и не может быть изменено.")
        self.__state = value


@dataclass
class AutomateRow:
    __signals: list[str]
    __state: str
    value: dict[str, Cell]

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

    def __init__(self, states: list[str] | None = None, signals: list[str] | None = None, a_dict: dict[str, dict[str, list[str]]] | None = None) -> None:
        if states is not None and signals is not None:
            self.__signals = signals
            self.__states = states
            for state in states:
                for signal in signals:
                    self.__matrix[state] = {}
                    self.__matrix[state][signal] = Cell(state, signal, [])
        elif a_dict is not None:
            ...
            # закончил туть

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
                for i in value:
                    if i not in self.__states:
                        raise KeyError("Попытка присвоить несуществующее состоянии")
                for i in item:
                    if i not in self.__signals:
                        raise KeyError("Попытка присвоить несуществующий сигнал")
                self.__matrix[item[0]][item[1]] = Cell(item[0], item[1], value)
        else:
            raise KeyError("Неверный индекс")

    def __str__(self) -> str:
        table = PrettyTable()
        table.field_names = [""] + self.__signals
        for row in self.__matrix:
            a = self.__get_row_element(row)
            table.add_row(
                [row] + a
            )
        return str(table)

    def __get_row_element(self, index: str) -> list[str]:
        return [", ".join(x) if (x := self.__matrix[index][_].value) != [] else "*" for _ in self.__matrix[index]]

    def to_dict(self) -> dict[str, dict[str, list[str]]]:
        return {} # закончил туть
