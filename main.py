import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLCDNumber, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Car Dashboard")
        self.setGeometry(100, 100, 800, 800)

        # Initialize dashboard data
        self.speed = 0
        self.target_speed = 0
        self.rpm = 0
        self.target_rpm = 0
        self.fuel_level = 100
        self.temperature = 90
        self.odometer = 0
        self.gear = "N"
        self.gear_ratios = {"R": 250, "N": 0, "1": 250, "2": 200, "3": 120, "4": 60, "5": 20}
        self.speed_history = []
        self.rpm_history = []
        self.history_update_count = 0

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.upper_layout = QHBoxLayout()
        self.layout.addLayout(self.upper_layout)

        self.speedometer_figure = Figure(facecolor='black')
        self.speedometer_canvas = FigureCanvas(self.speedometer_figure)
        self.speedometer_ax = self.speedometer_figure.add_subplot(111, polar=False)
        self.upper_layout.addWidget(self.speedometer_canvas)

        self.tachometer_figure = Figure(facecolor='black')
        self.tachometer_canvas = FigureCanvas(self.tachometer_figure)
        self.tachometer_ax = self.tachometer_figure.add_subplot(111, polar=False)
        self.upper_layout.addWidget(self.tachometer_canvas)

        self.digital_layout = QHBoxLayout()
        self.layout.addLayout(self.digital_layout)

        self.speed_label = QLabel("Speed (km/h):")
        self.speed_label.setStyleSheet("color: green; background-color: black;")
        self.digital_layout.addWidget(self.speed_label)
        self.speed_display = QLCDNumber()
        self.speed_display.setStyleSheet("color: green; background-color: black;")
        self.digital_layout.addWidget(self.speed_display)

        self.rpm_label = QLabel("RPM (x1000):")
        self.rpm_label.setStyleSheet("color: green; background-color: black;")
        self.digital_layout.addWidget(self.rpm_label)
        self.rpm_display = QLCDNumber()
        self.rpm_display.setStyleSheet("color: green; background-color: black;")
        self.digital_layout.addWidget(self.rpm_display)

        self.fuel_label = QLabel("Fuel Level (%):")
        self.fuel_label.setStyleSheet("color: green; background-color: black;")
        self.digital_layout.addWidget(self.fuel_label)
        self.fuel_display = QLCDNumber()
        self.fuel_display.setStyleSheet("color: green; background-color: black;")
        self.digital_layout.addWidget(self.fuel_display)

        self.temp_label = QLabel("Temperature (°C):")
        self.temp_label.setStyleSheet("color: green; background-color: black;")
        self.digital_layout.addWidget(self.temp_label)
        self.temp_display = QLCDNumber()
        self.temp_display.setStyleSheet("color: green; background-color: black;")
        self.digital_layout.addWidget(self.temp_display)

        self.odometer_label = QLabel("Odometer (km):")
        self.odometer_label.setStyleSheet("color: green; background-color: black;")
        self.digital_layout.addWidget(self.odometer_label)
        self.odometer_display = QLCDNumber()
        self.odometer_display.setStyleSheet("color: green; background-color: black;")
        self.digital_layout.addWidget(self.odometer_display)

        self.gear_label = QLabel("Gear:")
        self.gear_label.setStyleSheet("color: green; background-color: black;")
        self.digital_layout.addWidget(self.gear_label)
        self.gear_display = QLabel(self.gear)
        self.gear_display.setStyleSheet("color: green; background-color: black;")
        self.gear_display.setAlignment(Qt.AlignCenter)
        self.digital_layout.addWidget(self.gear_display)

        self.history_figure = Figure(facecolor='black')
        self.history_canvas = FigureCanvas(self.history_figure)
        self.history_ax_speed = self.history_figure.add_subplot(211)
        self.history_ax_rpm = self.history_figure.add_subplot(212)
        self.layout.addWidget(self.history_canvas)

        self.buttons_layout = QHBoxLayout()
        self.layout.addLayout(self.buttons_layout)

        self.gas_button = QPushButton("Gas")
        self.gas_button.clicked.connect(self.increase_speed)
        self.buttons_layout.addWidget(self.gas_button)

        self.brake_button = QPushButton("Brake")
        self.brake_button.clicked.connect(self.decrease_speed)
        self.buttons_layout.addWidget(self.brake_button)

        self.gear_up_button = QPushButton("Gear Up")
        self.gear_up_button.clicked.connect(self.gear_up)
        self.buttons_layout.addWidget(self.gear_up_button)

        self.gear_down_button = QPushButton("Gear Down")
        self.gear_down_button.clicked.connect(self.gear_down)
        self.buttons_layout.addWidget(self.gear_down_button)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_dashboard)
        self.timer.start(10)  # Approximately 60 FPS

    def increase_speed(self):
        self.target_rpm = min(self.target_rpm + 500, 8000)
        if self.gear != "N":
            self.target_speed = min((self.target_rpm / self.gear_ratios[self.gear]) if self.gear_ratios[self.gear] > 0 else 0, 180)

    def decrease_speed(self):
        if self.target_speed > 0:
            self.target_speed = max(self.target_speed - 10, 0)
        if self.target_rpm > 0:
            self.target_rpm = max(self.target_rpm - 500, 0)

    def gear_up(self):
        gears = ["R", "N", "1", "2", "3", "4", "5"]
        current_index = gears.index(self.gear)
        if current_index < len(gears) - 1:
            self.gear = gears[current_index + 1]
            self.update_target_rpm_and_speed()

    def gear_down(self):
        gears = ["R", "N", "1", "2", "3", "4", "5"]
        current_index = gears.index(self.gear)
        if current_index > 0:
            self.gear = gears[current_index - 1]
            self.update_target_rpm_and_speed()

    def update_target_rpm_and_speed(self):
        if self.gear != "N":
            ratio = self.gear_ratios[self.gear]
            self.target_rpm = min(self.speed * ratio, 8000)
            self.target_speed = min(self.rpm / ratio, 180)
        else:
            self.target_rpm = 0

    def update_dashboard(self):
        self.speed += (self.target_speed - self.speed) * 0.1
        self.rpm += (self.target_rpm - self.rpm) * 0.1

        self.fuel_level -= self.rpm / 100000

        if self.speed >= 180:
            self.rpm = min(self.rpm, 8000)
        if self.rpm >= 8000:
            self.speed = min(self.speed, 180)

        self.speed_display.display(round(self.speed))
        self.rpm_display.display(round(self.rpm / 1000, 1))
        self.fuel_display.display(self.fuel_level)
        self.temp_display.display(self.temperature)
        self.odometer += self.speed / 3600
        self.odometer_display.display(round(self.odometer, 2))
        self.gear_display.setText(self.gear)
        self.update_dials()

        if self.history_update_count < 20:
            self.history_update_count += 1
        else:
            self.update_history()
            self.history_update_count = 0

    

    def update_dials(self):
        self.speedometer_ax.clear()
        self.speedometer_ax.set_xlim(-1.5, 1.5)
        self.speedometer_ax.set_ylim(-1.5, 1.5)
        self.speedometer_ax.set_xticks([])
        self.speedometer_ax.set_yticks([])

        theta = np.linspace(-np.pi / 4, 5 * np.pi / 4, 100)
        self.speedometer_ax.plot(np.cos(theta), np.sin(theta), color="gray")
        for i in range(0, 181, 20):
            angle = -np.pi / 4 + i * (3 * np.pi / 2) / 180
            x, y = 1.2 * np.cos(angle), 1.2 * np.sin(angle)
            self.speedometer_ax.text(x, y, str(i), fontsize=8, color="black", ha="center", va="center")

        speed_angle = -np.pi / 4 + self.speed * (3 * np.pi / 2) / 180
        self.speedometer_ax.arrow(0, 0, 0.9 * np.cos(speed_angle), 0.9 * np.sin(speed_angle),
                                  head_width=0.1, head_length=0.1, fc="cyan", ec="cyan")

        self.tachometer_ax.clear()
        self.tachometer_ax.set_xlim(-1.5, 1.5)
        self.tachometer_ax.set_ylim(-1.5, 1.5)
        self.tachometer_ax.set_xticks([])
        self.tachometer_ax.set_yticks([])

        theta = np.linspace(-np.pi / 4, 5 * np.pi / 4, 100)
        self.tachometer_ax.plot(np.cos(theta), np.sin(theta), color="gray")
        for i in range(0, 9):
            angle = -np.pi / 4 + i * (3 * np.pi / 2) / 8
            x, y = 1.2 * np.cos(angle), 1.2 * np.sin(angle)
            self.tachometer_ax.text(x, y, str(i), fontsize=8, color="black", ha="center", va="center")

        rpm_angle = -np.pi / 4 + (self.rpm / 1000) * (3 * np.pi / 2) / 8
        self.tachometer_ax.arrow(0, 0, 0.9 * np.cos(rpm_angle), 0.9 * np.sin(rpm_angle),
                                 head_width=0.1, head_length=0.1, fc="red", ec="red")

        self.speedometer_canvas.draw()
        self.tachometer_canvas.draw()

    def update_history(self):
        self.speed_history.append(self.speed)
        self.rpm_history.append(self.rpm)
        if len(self.speed_history) > 100:
            self.speed_history.pop(0)
            self.rpm_history.pop(0)

        self.history_ax_speed.clear()
        self.history_ax_speed.plot(self.speed_history, color="cyan")
        self.history_ax_speed.set_title("Speed History", color="white")
        self.history_ax_speed.tick_params(colors="white")
        self.history_ax_speed.set_facecolor("black")

        self.history_ax_rpm.clear()
        self.history_ax_rpm.plot(self.rpm_history, color="red")
        self.history_ax_rpm.set_title("RPM History", color="white")
        self.history_ax_rpm.tick_params(colors="white")
        self.history_ax_rpm.set_facecolor("black")

        self.history_canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())
