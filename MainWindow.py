from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from MatplotlibWidget import MatplotlibWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Настройка главного окна
        self.setWindowTitle("Спидометр")
        self.setGeometry(100, 100, 800, 600)

        self.acceleration_inertia = 0.01

        # Основной виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Макет
        self.layout = QVBoxLayout(self.central_widget)

        # Виджет для графиков
        self.speedometer = MatplotlibWidget()
        self.layout.addWidget(self.speedometer)

        # Кнопки управления
        self.gas_button = QPushButton("Газ")
        self.gas_button.pressed.connect(self.start_acceleration)  # Удержание увеличивает ускорение
        self.gas_button.released.connect(self.stop_acceleration)  # Отпускание прекращает прирост
        self.layout.addWidget(self.gas_button)

        self.brake_button = QPushButton("Тормоз")
        self.brake_button.pressed.connect(self.start_deceleration)  # Удержание уменьшает ускорение
        self.brake_button.released.connect(self.stop_deceleration)  # Отпускание прекращает замедление
        self.layout.addWidget(self.brake_button)

        # Основной таймер для обновления графика (≈60 FPS)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_speedometer)
        self.timer.start(16)  # 16 мс ≈ 60 FPS

        # Переменные состояния
        self.current_speed = 0       # Текущая скорость
        self.acceleration = 0        # Текущее ускорение
        self.acceleration_delta = 0  # Изменение ускорения (нажимается "Газ" или "Тормоз")

    def start_acceleration(self):
        """Начинает увеличение ускорения."""
        self.acceleration_delta = 0.05  # Плавное увеличение ускорения

    def stop_acceleration(self):
        """Прекращает увеличение ускорения."""
        self.acceleration_delta = 0  # Прекращаем изменение ускорения

    def start_deceleration(self):
        """Начинает уменьшение ускорения."""
        self.acceleration_delta = -0.05  # Плавное уменьшение ускорения

    def stop_deceleration(self):
        """Прекращает уменьшение ускорения."""
        self.acceleration_delta = 0  # Прекращаем изменение ускорения

    def update_speedometer(self):
        """Обновляет скорость и график спидометра."""
        max_speed = 180  # Максимальная скорость
        min_speed = 0    # Минимальная скорость

        # Плавное изменение ускорения
        self.acceleration += self.acceleration_delta
        self.acceleration = max(-0.5, min(0.5, self.acceleration))  # Ограничиваем ускорение

        # Обновляем текущую скорость с учетом ускорения
        self.current_speed += self.acceleration
        self.current_speed = max(min_speed, min(max_speed, self.current_speed))  # Ограничиваем скорость

        # Обновляем график
        self.speedometer.draw_speedometer(self.current_speed)
        if (self.acceleration > 0):
            self.acceleration -= self.acceleration_inertia
        elif self.acceleration < 0:
            self.acceleration += self.acceleration_inertia
        if abs(self.acceleration) < self.acceleration_inertia:
            self.acceleration = 0
