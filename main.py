from TAFL5.TAFL5Saver import TAFL5Saver
from TAFL5.TAFL5 import TAFL5
from TAFL5.TAFL5Inputer import TAFL5Inputer
from TAFL5.TAFL5Menu import TAFL5Menu


def main():
    saver = TAFL5Saver()
    menu = TAFL5Menu()
    inputer = TAFL5Inputer()

    data_load = saver.load_data()

    alphabet_symbol = []
    alphabet_graph = []
    input_automate = {}

    if data_load == {}:
        alphabet_symbol = inputer.load_alphabet_symbol()
        alphabet_graph = inputer.load_alphabet_graph()
        # input_automate = inputer
    else:
        ...

    if alphabet_symbol is not None:
        c = menu.new_load_alphabet_symbol_menu(alphabet_symbol)
        match c:
            case 1 | None:
                ...
            case 2:
                alphabet_symbol = inputer.load_alphabet_symbol(alphabet_symbol)
    else:
        alphabet_symbol = inputer.load_alphabet_symbol()

    if alphabet_graph is not None:
        c = menu.new_load_alphabet_graph_menu(alphabet_graph)
        match c:
            case 1 | None:
                ...
            case 2:
                alphabet_graph = inputer.load_alphabet_graph(alphabet_graph)
    else:
        alphabet_graph = inputer.load_alphabet_graph()


    # TAFL5 = TAFL5()


if __name__ == "__main__":
    main()
