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
        self.setGeometry(100, 100, 800, 600)

        # Initialize dashboard data
        self.speed = 0
        self.rpm = 0
        self.fuel_level = 100
        self.temperature = 90
        self.odometer = 0
        self.gear = "N"
        self.gear_ratios = {"N": 0, "1": 100, "2": 80, "3": 60, "4": 40, "5": 20, "R": 100}

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Upper layout for gauges
        self.upper_layout = QHBoxLayout()
        self.layout.addLayout(self.upper_layout)

        # Speedometer (Dial)
        self.speedometer_figure = Figure()
        self.speedometer_canvas = FigureCanvas(self.speedometer_figure)
        self.speedometer_ax = self.speedometer_figure.add_subplot(111, polar=False)
        self.upper_layout.addWidget(self.speedometer_canvas)

        # Tachometer (Dial)
        self.tachometer_figure = Figure()
        self.tachometer_canvas = FigureCanvas(self.tachometer_figure)
        self.tachometer_ax = self.tachometer_figure.add_subplot(111, polar=False)
        self.upper_layout.addWidget(self.tachometer_canvas)

        # Digital displays layout
        self.digital_layout = QHBoxLayout()
        self.layout.addLayout(self.digital_layout)

        # Speedometer (Digital)
        self.speed_label = QLabel("Speed (km/h):")
        self.speed_label.setStyleSheet("""QLCDNumber { 
                                                    background-color: black; 
                                                    color: green; }""")
        self.digital_layout.addWidget(self.speed_label)
        self.speed_display = QLCDNumber()
        self.speed_display.setStyleSheet("""QLCDNumber { 
                                                    background-color: black; 
                                                    color: green; }""")
        self.digital_layout.addWidget(self.speed_display)

        # Tachometer (Digital)
        self.rpm_label = QLabel("RPM (x1000):")
        self.rpm_label.setStyleSheet("""QLCDNumber { 
                                                    background-color: black; 
                                                    color: green; }""")
        self.digital_layout.addWidget(self.rpm_label)
        self.rpm_display = QLCDNumber()
        self.rpm_display.setStyleSheet("""QLCDNumber { 
                                                    background-color: black; 
                                                    color: green; }""")
        self.digital_layout.addWidget(self.rpm_display)

        # Fuel level
        self.fuel_label = QLabel("Fuel Level (%):")
        self.fuel_label.setStyleSheet("""QLCDNumber { 
                                                    background-color: black; 
                                                    color: green; }""")
        self.digital_layout.addWidget(self.fuel_label)
        self.fuel_display = QLCDNumber()
        self.fuel_display.setStyleSheet("""QLCDNumber { 
                                                    background-color: black; 
                                                    color: green; }""")
        self.digital_layout.addWidget(self.fuel_display)

        # Temperature
        self.temp_label = QLabel("Temperature (°C):")
        self.temp_label.setStyleSheet("""QLCDNumber { 
                                                    background-color: black; 
                                                    color: green; }""")
        self.digital_layout.addWidget(self.temp_label)
        self.temp_display = QLCDNumber()
        self.temp_display.setStyleSheet("""QLCDNumber { 
                                                    background-color: black; 
                                                    color: green; }""")
        self.digital_layout.addWidget(self.temp_display)

        # Odometer
        self.odometer_label = QLabel("Odometer (km):")
        self.odometer_label.setStyleSheet("""QLCDNumber { 
                                                    background-color: black; 
                                                    color: green; }""")
        self.digital_layout.addWidget(self.odometer_label)
        self.odometer_display = QLCDNumber()
        self.odometer_display.setStyleSheet("""QLCDNumber { 
                                                    background-color: black; 
                                                    color: green; }""")
        self.digital_layout.addWidget(self.odometer_display)

        # Gear indicator
        self.gear_label = QLabel("Gear:")
        self.gear_label.setStyleSheet("""QLCDNumber { 
                                                    background-color: black; 
                                                    color: green; }""")
        self.digital_layout.addWidget(self.gear_label)
        self.gear_display = QLabel(self.gear)
        self.gear_display.setStyleSheet("""QLCDNumber { 
                                                    background-color: black; 
                                                    color: green; }""")
        self.gear_display.setAlignment(Qt.AlignCenter)
        self.digital_layout.addWidget(self.gear_display)

        # Control buttons
        self.gas_button = QPushButton("Gas")
        self.gas_button.clicked.connect(self.increase_speed)
        self.layout.addWidget(self.gas_button)

        self.brake_button = QPushButton("Brake")
        self.brake_button.clicked.connect(self.decrease_speed)
        self.layout.addWidget(self.brake_button)

        self.gear_up_button = QPushButton("Gear Up")
        self.gear_up_button.clicked.connect(self.gear_up)
        self.layout.addWidget(self.gear_up_button)

        self.gear_down_button = QPushButton("Gear Down")
        self.gear_down_button.clicked.connect(self.gear_down)
        self.layout.addWidget(self.gear_down_button)

        # Update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_dashboard)
        self.timer.start(100)

    def increase_speed(self):
        if self.gear != "N" and self.speed < 200:
            self.speed += 10
            self.rpm = min(self.speed * self.gear_ratios[self.gear], 8000)

    def decrease_speed(self):
        if self.speed > 0:
            self.speed -= 10
            self.rpm = max(0, self.speed * self.gear_ratios[self.gear])

    def gear_up(self):
        gears = ["N", "1", "2", "3", "4", "5", "R"]
        current_index = gears.index(self.gear)
        if current_index < len(gears) - 1:
            self.gear = gears[current_index + 1]

    def gear_down(self):
        gears = ["N", "1", "2", "3", "4", "5", "R"]
        current_index = gears.index(self.gear)
        if current_index > 0:
            self.gear = gears[current_index - 1]

    def update_dashboard(self):
        self.speed_display.display(self.speed)
        self.rpm_display.display(self.rpm / 1000)
        self.fuel_display.display(self.fuel_level)
        self.temp_display.display(self.temperature)
        self.odometer += self.speed / 3600
        self.odometer_display.display(round(self.odometer, 2))
        self.gear_display.setText(self.gear)
        self.update_dials()

    def update_dials(self):
        # Update speedometer dial
        self.speedometer_ax.clear()
        self.speedometer_ax.set_xlim(-1.5, 1.5)
        self.speedometer_ax.set_ylim(-1.5, 1.5)
        self.speedometer_ax.set_xticks([])
        self.speedometer_ax.set_yticks([])

        # Draw static speedometer
        theta = np.linspace(-np.pi / 4, 5 * np.pi / 4, 100)
        self.speedometer_ax.plot(np.cos(theta), np.sin(theta), color="gray")
        for i in range(0, 181, 20):
            angle = -np.pi / 4 + i * (3 * np.pi / 2) / 180
            x, y = 1.2 * np.cos(angle), 1.2 * np.sin(angle)
            self.speedometer_ax.text(x, y, str(i), fontsize=8, ha="center", va="center")

        # Draw speed pointer
        speed_angle = -np.pi / 4 + self.speed * (3 * np.pi / 2) / 180
        self.speedometer_ax.arrow(0, 0, 0.9 * np.cos(speed_angle), 0.9 * np.sin(speed_angle),
                                head_width=0.1, head_length=0.1, fc="blue", ec="blue")

        # Update tachometer dial
        self.tachometer_ax.clear()
        self.tachometer_ax.set_xlim(-1.5, 1.5)
        self.tachometer_ax.set_ylim(-1.5, 1.5)
        self.tachometer_ax.set_xticks([])
        self.tachometer_ax.set_yticks([])

        # Draw static tachometer
        theta = np.linspace(-np.pi / 4, 5 * np.pi / 4, 100)
        self.tachometer_ax.plot(np.cos(theta), np.sin(theta), color="gray")
        for i in range(0, 9):
            angle = -np.pi / 4 + i * (3 * np.pi / 2) / 8
            x, y = 1.2 * np.cos(angle), 1.2 * np.sin(angle)
            self.tachometer_ax.text(x, y, str(i), fontsize=8, ha="center", va="center")

        # Draw rpm pointer
        rpm_angle = -np.pi / 4 + (self.rpm / 1000) * (3 * np.pi / 2) / 8
        self.tachometer_ax.arrow(0, 0, 0.9 * np.cos(rpm_angle), 0.9 * np.sin(rpm_angle),
                                head_width=0.1, head_length=0.1, fc="red", ec="red")

        self.speedometer_canvas.draw()
        self.tachometer_canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())
