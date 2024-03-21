from TAFL5.TAFL5Saver import TAFL5Saver
from TAFL5.TAFL5 import TAFL5
from TAFL5.TAFL5Inputer import TAFL5Inputer
from TAFL5.TAFL5Menu import TAFL5Menu
from TAFLCore.Automate import Automate


def main():

    saver = TAFL5Saver()
    menu = TAFL5Menu()
    inputer = TAFL5Inputer()

    data_load = saver.load_data()

    alphabet_symbol = []
    alphabet_graph = []
    input_automate = None

    if data_load == {}:
        alphabet_symbol = inputer.load_alphabet_symbol()
        alphabet_graph = inputer.load_alphabet_graph()
        states = []
        for i in alphabet_graph:
            states.append(
                {
                    "state": [i],
                    "alias": i,
                    "additional_info": None
                }
            )
        input_automate = Automate(states=states, signals=alphabet_symbol)
        input_automate = inputer.load_input_automate(input_automate)
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
            case 1:
                ...
            case 2:
                while True:
                    cc = menu.change_save_config_menu()
                    match cc:
                        case 1:
                            alphabet_symbol_ = inputer.load_alphabet_symbol()
                            if alphabet_symbol_ is None:
                                continue
                            alphabet_symbol = alphabet_symbol_
                        case 2:
                            alphabet_graph_ = inputer.load_alphabet_graph()
                            if alphabet_graph_ is None:
                                continue
                            alphabet_graph = alphabet_graph_
                        case 3:
                            input_automate = inputer.load_input_automate(input_automate)
                        case 4:
                            saver.save_all(alphabet_symbol, alphabet_graph, input_automate.to_dict())
                            break

    while True:
        c = menu.main_menu()
        match c:
            case 3:
                print(c)
                exit()

    # TAFL5 = TAFL5()


if __name__ == "__main__":
    main()
