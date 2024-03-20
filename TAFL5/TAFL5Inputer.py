from TAFLCore.BaseInputer import BaseInputer


class TAFL5Inputer(BaseInputer):

    def load_alphabet_symbol(self, previous: list[str] | None = None) -> list[str] | None:
        input_phrase = "Введите пожалуйста алфавит входных символов через пробел(пример: 'a b c)': " \
            if previous is None \
            else f"Введите пожалуйста алфавит входных символов через пробел(пример: 'a b c')(Предыдущий '{' '.join(previous)}'): "
        return self._input_alphabet(input_phrase)

    def load_alphabet_graph(self, previous: list[str] | None = None) -> list[str] | None:
        input_phrase = "Введите пожалуйста алфавит графа через пробел(пример: 'qo q1 q2)': " \
            if previous is None \
            else f"Введите пожалуйста алфавит графа через пробел(пример: 'q0 q1 q2')(Предыдущий '{' '.join(previous)}'): "
        return self._input_alphabet(input_phrase)
