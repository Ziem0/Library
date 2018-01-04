from controller.main_controller import Controller
from ui.ui import UI
from ui.mol_ui import ReadersUI
from dao.dao import Dao

def main():

    ui = UI()
    ui_readers = ReadersUI()
    dao = Dao()
    controller = Controller(ui, ui_readers, dao)


if __name__ == '__main__':
    main()

