from MatplotlibWidget import MatplotlibWidget
import numpy as np

class SpeedometerWidget(MatplotlibWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def draw_speedometer(self, speed=0):
        """Рисует спидометр с текущей скоростью."""
        self.figure.clear()  # Очищаем график
        ax = self.figure.add_subplot(111, polar=True)  # Полярная диаграмма

        # Устанавливаем параметры спидометра
        max_speed = 180  # Максимальная скорость
        speed_normalized = np.clip(speed / max_speed, 0, 1) # Угол для стрелки

        # Рисуем шкалу
        theta = np.linspace(-np.pi / 2, np.pi / 2, 100)
        ax.plot(theta, [1.0] * len(theta), color="black", lw=3)

        # Добавляем разметку спидометра
        for i in range(0, max_speed + 1, 20):
            angle = -np.pi / 2 + (i / max_speed) * np.pi
            ax.text(angle, 1.1, f"{i}", ha="center", va="center", fontsize=10)

        # Рисуем стрелку скорости
        angle = -np.pi / 2 + speed_normalized * np.pi
        ax.arrow(0, 0, angle, 0.5, width=0.02, color="red", alpha=0.8)

        # Скрываем лишние элементы
        ax.set_yticks([])
        ax.set_xticks([])
        ax.spines['polar'].set_visible(False)

        self.canvas.draw()  # Обновляем график
