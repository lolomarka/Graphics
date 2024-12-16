import sys
from PyQt5.QtWidgets import QApplication
import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Создаем основное окно
    main_window = MainWindow.MainWindow()
    main_window.show()

    # Запускаем приложение
    sys.exit(app.exec_())
