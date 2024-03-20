from TAFLCore.BaseMenu import BaseMenu


class TAFL5Menu(BaseMenu):

    @BaseMenu.clear_wrapper
    def new_load_alphabet_symbol_menu(self, previous_alphabet: list[str]) -> int | None:
        print(f"Уже есть сохраненный алфавит входных символов '{' '.join(previous_alphabet)}'. Вы хотите использовать "
              f"его?")
        menu_choice = self.get_choose(
            [
                "Да",
                "Нет"
            ]
        )

        return menu_choice

    @BaseMenu.clear_wrapper
    def new_load_alphabet_graph_menu(self, previous_alphabet: list[str]) -> int | None:
        print(f"Уже есть сохраненный алфавит графа '{' '.join(previous_alphabet)}'. Вы хотите использовать "
              f"его?")
        menu_choice = self.get_choose(
            [
                "Да",
                "Нет"
            ]
        )

        return menu_choice

    @BaseMenu.clear_wrapper
    def change_alphabet_menu(self) -> int | None:
        print("Изменение алфавита: ")
        menu_choice = self.get_choose(
            [
                "Входных символов",
                "Графа",
                "Назад"
            ]
        )

        return menu_choice

    @BaseMenu.clear_wrapper
    def main_menu(self) -> int:
        menu_choice = self.get_choose(
            [
                "Бред",
                "Изменить алфавиты",
                "Выход"
            ]
        )
        return menu_choice
