from TAFL5.TAFL5Saver import TAFL5Saver
from TAFL5.TAFL5 import TAFL5
from TAFL5.TAFL5Inputer import TAFL5Inputer
from TAFL5.TAFL5Menu import TAFL5Menu
from TAFLCore.Automate import Automate, AutomateUtils


def main():
    tafl5 = TAFL5()

    saver = TAFL5Saver()
    menu = TAFL5Menu()
    inputer = TAFL5Inputer()

    data_load = saver.load_data()

    alphabet_symbol = []
    alphabet_graph = []
    input_automate = None
    automaton_transition = None
    deparmenize_automate = None

    if data_load == {}:
        alphabet_symbol = inputer.get_alphabet_symbol()
        alphabet_graph = inputer.get_alphabet_graph()
        states = []
        for i in alphabet_graph:
            states.append(
                {
                    "state": [i],
                    "alias": i,
                    "additional_info": None,
                    "is_start": False,
                    "is_end": False
                }
            )
        input_automate = Automate(states=states, signals=alphabet_symbol)
        input_automate = inputer.get_input_automate(input_automate)

        input_automate = inputer.get_started_states(input_automate)
        input_automate = inputer.get_ended_states(input_automate)

        saver.save_all(alphabet_symbol, alphabet_graph, input_automate.to_dict())
    else:
        alphabet_symbol = saver.load_alphabet_symbol()
        alphabet_graph = saver.load_alphabet_graph()
        input_automate = Automate(automate_dict=saver.load_input_automate())

        c = menu.use_save_config_menu(
            alphabet_symbol,
            alphabet_graph,
            str(input_automate)
        )
        match c:
            case 0:
                ...
            case 1:
                alphabet_symbol_ = inputer.get_alphabet_symbol()
                if alphabet_symbol_ is None:
                    ...
                else:
                    alphabet_symbol = alphabet_symbol_
                alphabet_graph_ = inputer.get_alphabet_graph()
                if alphabet_graph_ is None:
                    ...
                else:
                    alphabet_graph = alphabet_graph_
                states = []
                for i in alphabet_graph:
                    states.append(
                        {
                            "state": [i],
                            "alias": i,
                            "additional_info": None
                        }
                    )
                a = Automate(states=states, signals=alphabet_symbol)
                print(a)
                input_automate = inputer.get_input_automate(Automate(states=states, signals=alphabet_symbol), is_change_alphabet=True)
                saver.save_all(alphabet_symbol, alphabet_graph, input_automate.to_dict())


    while True:
        c = menu.main_menu()
        match c:
            case 0:
                print(f"Алфавит входных символов: {alphabet_symbol}")
                print(f"Алфавит автомата: {alphabet_graph}")
                print(input_automate)
                input()
            case 1:
                print(input_automate)
                print("ε-замыкания:")
                e_closures = tafl5.construct_e_closures(input_automate)
                for i in e_closures:
                    print(i)
                print()
                print("Отобразить таблицу переходов автомата")
                automaton_transition = tafl5.get_automaton_transition_table(input_automate, e_closures)
                print(automaton_transition)
                deparmenize_automate = tafl5.deparmenize_automate(automaton_transition)
                print(deparmenize_automate)
                input()
            case 2:
                if deparmenize_automate is None:
                    print("Запустите сначала основное задание ")
                    input()
                    continue
                print(deparmenize_automate)
                word = inputer.get_word_to_validate(deparmenize_automate)
                if tafl5.check_is_valid_word(word, deparmenize_automate):
                    print(f"Автомат допускает слово: {word}")
                else:
                    print(f"Автомат не допускает слово: {word}")
                input()
            case 3:
                alphabet_symbol = inputer.get_alphabet_symbol()
                alphabet_graph = inputer.get_alphabet_graph()
                states = []
                for i in alphabet_graph:
                    states.append(
                        {
                            "state": [i],
                            "alias": i,
                            "additional_info": None,
                            "is_start": False,
                            "is_end": False
                        }
                    )

                input_automate = Automate(states=states, signals=alphabet_symbol)
                input_automate = inputer.get_input_automate(input_automate)

                input_automate = inputer.get_started_states(input_automate)
                input_automate = inputer.get_ended_states(input_automate)

                saver.save_all(alphabet_symbol, alphabet_graph, input_automate.to_dict())
            case 4:
                exit()

if __name__ == "__main__":
    main()
