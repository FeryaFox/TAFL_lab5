from TAFLCore.BaseSaver import BaseSaver


class TAFL5Saver(BaseSaver):

    def __init__(self):
        super().__init__()

    @BaseSaver.load_decorator
    def load_data(self) -> dict:
        return self._data

    @BaseSaver.load_decorator
    def load_alphabet_symbol(self) -> list[str] | None:
        try:
            return self._data["alphabet_symbol"]
        except KeyError:
            return None

    @BaseSaver.save_decorator
    def save_alphabet_symbol(self, alphabet_symbol: list[str]) -> None:
        self._data["alphabet_symbol"] = alphabet_symbol

    @BaseSaver.load_decorator
    def load_alphabet_graph(self) -> list[str] | None:
        try:
            return self._data["alphabet_graph"]
        except KeyError:
            return None

    @BaseSaver.save_decorator
    def save_alphabet_graph(self, alphabet_graph: list[str]) -> None:
        self._data["alphabet_graph"] = alphabet_graph
