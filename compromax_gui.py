from pathlib import Path
import sys

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT, FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide2 import QtWidgets, QtCore
from PySide2.QtGui import QIcon
import matplotlib.pyplot as plt
import numpy as np

import compromaximize
import utils

VISUAL_SAMPLES = 2000


class MainCompromaximizer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.sig = np.zeros((2, 2000))
        self.result = np.zeros((2, 2000))
        self._visual_sig = np.zeros((2, VISUAL_SAMPLES))
        self._visual_result = np.zeros((2, VISUAL_SAMPLES))
        self.fn_signal = Path("")
        self.fs = 48000
        self.limit_gain = 20
        self.window_duration = 0.1
        self.compromax = compromaximize.Compromaximizer(self.limit_gain)

        self.setWindowTitle("Compromaximizer")
        app_icon = QIcon("assets/compromax64.png")
        self.setWindowIcon(app_icon)

        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        container_layout = QtWidgets.QVBoxLayout(self._main)

        # top bar
        layout_filename = QtWidgets.QHBoxLayout()
        self._textedit_filename = QtWidgets.QLineEdit("Dateiname?")
        self._button_open_file = QtWidgets.QPushButton("Open...")
        self._button_open_file.clicked.connect(self._open_file)

        # plot
        self._figure = Figure()
        self._figure.set_tight_layout(dict(pad=0.3))
        self._axes: plt.Axes = self._figure.add_subplot(111)
        self._canvas = FigureCanvasQTAgg(self._figure)
        self._navigation_toolbar = NavigationToolbar2QT(self._canvas, self)

        # bottom bar
        layout_output = QtWidgets.QHBoxLayout()
        self._slider_max_gain = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self._slider_max_gain.setMinimum(1)
        self._slider_max_gain.setMaximum(100)
        self._slider_max_gain.setValue(self.limit_gain)
        self._slider_max_gain.valueChanged.connect(self._slider_max_gain_value_changed)
        self._slider_max_gain.sliderReleased.connect(self._slider_max_gain_slider_released)
        self._label_max_gain = QtWidgets.QLabel()
        self._slider_max_gain_value_changed()
        self._button_save = QtWidgets.QPushButton("Save...")
        self._button_save.clicked.connect(self._save_file)

        # integrate into layout
        container_layout.addLayout(layout_filename)
        layout_filename.addWidget(self._textedit_filename)
        layout_filename.addWidget(self._button_open_file)
        container_layout.addWidget(self._canvas)
        container_layout.addWidget(self._navigation_toolbar)
        container_layout.addLayout(layout_output)
        layout_output.addWidget(self._slider_max_gain)
        layout_output.addWidget(self._label_max_gain)
        layout_output.addWidget(self._button_save)

    def _slider_max_gain_value_changed(self):
        self.limit_gain = self._slider_max_gain.value()
        self._label_max_gain.setText(f"Maximum gain: {self.limit_gain:4}")
        self.compromax.limit_gain = self.limit_gain

    def _slider_max_gain_slider_released(self):
        self.result = self.compromax.process(self.sig, self.fs, self.window_duration)
        self.update_plot()

    def _open_file(self):
        fn_signal, _ = QtWidgets.QFileDialog.getOpenFileName(filter="*.wav")
        if fn_signal != "":
            self.fn_signal = Path(fn_signal)
            self._textedit_filename.setText(fn_signal)
            self.sig, self.fs = utils.load_soundfile(fn_signal)
            self._slider_max_gain_slider_released()

    def _save_file(self):
        pn_out = self.fn_signal.parent
        fn_out = pn_out / (self.fn_signal.stem + f"_comp{self.limit_gain}.wav")
        fn_signal_out, _ = QtWidgets.QFileDialog.getSaveFileName(filter="*.wav", dir=str(fn_out))
        if fn_signal_out != "":
            utils.write_soundfile(fn_signal_out, self.result.T, self.fs)

    def update_plot(self):
        self._axes.clear()
        indices = np.floor(np.linspace(0, self.sig.shape[1], VISUAL_SAMPLES, endpoint=False)).astype(np.int)
        self._visual_result = self.result[:, indices]
        self._visual_sig = self.sig[:, indices]
        stacked = np.vstack((self._visual_result, self._visual_sig)).T
        self._axes.plot(stacked)
        self._figure.canvas.draw()
        self._figure.canvas.flush_events()


if __name__ == '__main__':
    qapp = QtWidgets.QApplication(sys.argv)

    main = MainCompromaximizer()
    main.show()

    sys.exit(qapp.exec_())
