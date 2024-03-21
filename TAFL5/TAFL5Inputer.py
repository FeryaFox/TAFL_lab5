from TAFLCore.BaseInputer import BaseInputer
from TAFLCore.Automate import Automate
from TAFLCore.BaseMenu import BaseMenu
import curses
from threading import Thread


class TAFL5Inputer(BaseInputer):
    def load_alphabet_symbol(self, previous: list[str] | None = None) -> list[str] | None:
        input_phrase = "Введите пожалуйста алфавит входных символов через пробел(пример: 'a b c)(e заразервировано)': " \
            if previous is None \
            else f"Введите пожалуйста алфавит входных символов через пробел(пример: 'a b c')(e  заразервировано)(Предыдущий '{' '.join(previous)}'): "
        while True:
            alphabet = self._input_alphabet(input_phrase)
            if "e" in alphabet:
                continue
            break
        return alphabet + ["e"]

    def load_alphabet_graph(self, previous: list[str] | None = None) -> list[str] | None:
        input_phrase = "Введите пожалуйста алфавит графа через пробел(пример: 'qo q1 q2)': " \
            if previous is None \
            else f"Введите пожалуйста алфавит графа через пробел(пример: 'q0 q1 q2')(Предыдущий '{' '.join(previous)}'): "
        return self._input_alphabet(input_phrase)

    @staticmethod
    def load_input_automate(automate: Automate) -> Automate:
        BaseMenu.clear()
        for state in automate.get_states_alias():
            for signal in automate.get_signals_name():
                print(automate)
                while True:

                    try:
                        print(f"Допустимые состояния: {", ".join(automate.get_all_states())}")
                        input_states = input(f"Введите состояния для ({state}, {signal})(через проблел)(например: 'q0 q1 q2') :").split()
                    except KeyboardInterrupt:
                        return automate

                    if not input_states:
                        return automate

                    if not automate.check_correct_states(input_states):
                        print("Вы ввели состояние, которого нет в автомате")
                        continue
                    automate[state, signal] = input_states
                    BaseMenu.clear()
                    break
        return automate
