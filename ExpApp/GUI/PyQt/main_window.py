import sys

import matplotlib
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QDoubleSpinBox, QLineEdit, QLabel, QRadioButton, QSpinBox, QComboBox

from ExpApp.API.Connector import Connector
from ExpApp.GUI.PyQt.Widgets.graphs import GraphWidget
from ExpApp.Utils.ExperimentParams import ExperimentParams
from ExpApp.Utils.Recorder import Recorder
from ExpApp.Utils.constants import WINDOW_X, WINDOW_Y
from ExpApp.tests.read_sample import ReadSample

matplotlib.use("Qt4Agg")
import time
import threading


class CustomMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(CustomMainWindow, self).__init__()
        self.communicator = Communicate()
        self.is_recording = False
        self.recorder = None

        self.setWindowTitle("ExpApp")
        self.setGeometry(100, 100, WINDOW_X, WINDOW_Y)

        # Default parameters
        self.exp_params = ExperimentParams()

        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        # Create graph frame
        graph_col_span = 8
        self.graph_layout = QtWidgets.QGridLayout()
        self.graph_frame = QtWidgets.QFrame(self)
        self.graph_frame.setLayout(self.graph_layout)
        self.main_layout.addWidget(self.graph_frame, 0, 0, 3, graph_col_span)
        self.myFig = GraphWidget()
        self.graph_layout.addWidget(self.myFig)
        my_data_loop = threading.Thread(name='my_data_loop', target=self.data_send_loop, daemon=True,
                                        args=(self.add_data_callback_func,))
        my_data_loop.start()

        # Create control panel frame
        cpr = 0
        self.control_panel_layout = QtWidgets.QGridLayout()
        self.control_panel_frame = QtWidgets.QFrame(self)
        self.control_panel_frame.setLayout(self.control_panel_layout)
        self.main_layout.addWidget(self.control_panel_frame, cpr, graph_col_span, 1, 3)

        # Pause button
        self.pause_button = QPushButton('Pause graph')
        self.is_paused = False
        self.pause_button.clicked.connect(lambda: self.pause_graphs())
        self.control_panel_layout.addWidget(self.pause_button, cpr, 0, 1, 3)
        cpr += 1

        # Record panel
        self.record_button = QPushButton('Record')
        self.record_button.clicked.connect(lambda: self.start_record())
        self.record_time_input = QDoubleSpinBox()
        self.record_count = 1
        self.record_time_input.setValue(self.exp_params.record_time)
        self.record_time_input.setSingleStep(0.1)
        self.record_time_input.valueChanged.connect(self.set_record_time)
        self.control_panel_layout.addWidget(self.record_time_input, cpr, 0)
        self.control_panel_layout.addWidget(self.record_button, cpr, 1, 1, 2)
        cpr += 1

        # Experiment setup panel
        # File name
        self.exp_name_prefix_input = QLineEdit()
        self.exp_name_prefix_input.setText(self.exp_params.name_prefix)
        self.exp_name_prefix_input.editingFinished.connect(self.set_exp_name)
        self.control_panel_layout.addWidget(QLabel("File Name Prefix: "), cpr, 0, 1, 1)
        self.control_panel_layout.addWidget(self.exp_name_prefix_input, cpr, 1, 1, 2)
        cpr += 1
        # Gender
        self.control_panel_layout.addWidget(QLabel("Gender:"), cpr, 0, 1, 1)
        self.exp_m_input = QRadioButton("male")
        self.exp_m_input.setChecked(self.exp_params.gender == self.exp_m_input.text())
        self.exp_m_input.toggled.connect(lambda checked: self.set_exp_gender(self.exp_m_input.text(), checked))
        self.exp_f_input = QRadioButton("female")
        self.exp_f_input.setChecked(self.exp_params.gender == self.exp_f_input.text())
        self.exp_f_input.toggled.connect(lambda checked: self.set_exp_gender(self.exp_f_input.text(), checked))
        self.control_panel_layout.addWidget(self.exp_m_input, cpr, 1, 1, 1)
        self.control_panel_layout.addWidget(self.exp_f_input, cpr, 2, 1, 1)
        cpr += 1
        # Age
        self.control_panel_layout.addWidget(QLabel("Age:"), cpr, 0, 1, 1)
        self.exp_age_input = QSpinBox()
        self.exp_age_input.setValue(self.exp_params.age)
        self.exp_age_input.editingFinished.connect(self.set_exp_age)
        self.control_panel_layout.addWidget(self.exp_age_input, cpr, 1, 1, 2)
        cpr += 1
        # Electrodes
        self.exp_electrodes_input = QLineEdit()
        self.exp_electrodes_input.setText(self.exp_params.electrodes)
        self.exp_electrodes_input.editingFinished.connect(self.set_electrodes)
        self.control_panel_layout.addWidget(QLabel("Electrodes:"), cpr, 0, 1, 1)
        self.control_panel_layout.addWidget(self.exp_electrodes_input, cpr, 1, 1, 2)
        cpr += 1

        # Experiment selection
        self.exp_selection_box = QComboBox()
        self.exp_selection_box.addItems(self.exp_params.options)
        self.exp_selection_box.currentIndexChanged.connect(self.set_exp)
        self.exp_run_button = QPushButton("Run")
        self.exp_run_button.clicked.connect(self.exp_run)
        self.control_panel_layout.addWidget(self.exp_run_button, cpr, 0, 1, 1)
        self.control_panel_layout.addWidget(self.exp_selection_box, cpr, 1, 1, 2)

        # Experiment window
        self.flash_window = QtWidgets.QMdiSubWindow()
        # self.flash_window.setGeometry(100, 100, 300, 300)

        self.show()

    def set_exp(self):
        self.exp_params.experiment = self.exp_selection_box.currentText()

    def exp_run(self):
        file_name = self.exp_params.to_file_name()
        self.recorder = Recorder(file_name)
        self.exp_params.exp_id += 1

        # Run experiment window separately
        # self.flash_window.showFullScreen()

    def set_electrodes(self):
        self.exp_params.electrodes = self.exp_electrodes_input.text()

    def set_exp_age(self):
        self.exp_params.age = self.exp_age_input.value()

    def set_exp_gender(self, value, checked):
        if checked:
            self.exp_params.gender = value

    def set_exp_name(self):
        self.exp_params.name_prefix = self.exp_name_prefix_input.text()

    def set_record_time(self):
        self.exp_params.record_time = self.record_time_input.value()

    def start_record(self):
        t = threading.Timer(self.record_time, lambda: self.stop_record())
        self.is_recording = True
        self.record_button.setDisabled(True)
        t.start()
        # record

    def stop_record(self):
        self.is_recording = False
        self.record_button.setDisabled(False)
        self.record_count = self.record_count + 1
        self.recorder.stop()

    def pause_graphs(self):
        self.is_paused = not self.is_paused
        self.pause_button.setText('Resume graph' if self.is_paused else 'Pause graph')

    def add_data_callback_func(self, value):
        if not self.is_paused:
            self.myFig.addData(value)
        if self.is_recording:
            self.recorder = Recorder()  # TODO change
            self.recorder.record_sample(value)

    def data_handler(self, sample):
        self.communicator.data_signal.emit(sample.channel_data)

    def data_send_loop(self, add_data_callback_func):
        self.communicator.data_signal.connect(add_data_callback_func)
        mock = False
        # mock = True
        if mock:
            reader = ReadSample()
            sample = reader.read_sample()

            while sample is not None:
                time.sleep(1. / 255.)
                value = sample.channel_data
                self.communicator.data_signal.emit(value)
                sample = reader.read_sample()
        else:
            board = Connector()
            board.attach_handlers(self.data_handler)


class Communicate(QtCore.QObject):
    data_signal = QtCore.pyqtSignal(list)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QtWidgets.QApplication(sys.argv)
    myGUI = CustomMainWindow()
    sys.exit(app.exec_())
