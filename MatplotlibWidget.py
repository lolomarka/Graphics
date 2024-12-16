from PyQt5.QtWidgets import QWidget, QVBoxLayout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import(
    FigureCanvasQTAgg as FigureCanvas
)
import numpy as np

class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Создаем макет для виджета
        layout = QVBoxLayout()

        # # Создаем объект Figure и Canvas
        self.figure, self.ax = plt.subplots(figsize=(5, 4), dpi=96)
        self.canvas = FigureCanvas(self.figure)

        layout.addWidget(self.canvas)

        # Применяем макет к виджету
        self.setLayout(layout)

    def example_plot(self):
        """Пример построения графика."""
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        self.ax.clear()  # Очищаем предыдущий график
        self.ax.plot(x, y, label='Sine Wave')
        self.ax.set_title("Пример графика")
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")
        self.ax.legend()
        self.canvas.draw()  # Обновляем отображение

    
        