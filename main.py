import sys
from PyQt5 import QtCore

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QCheckBox, \
    QDoubleSpinBox, QTextEdit, QTabWidget, QTableWidget, QTableWidgetItem

from bot import Bot
from worker import Worker

import keyboard


def trap_exc_during_debug(*args):
    # when app raises uncaught exception, print info
    [][1]
    print(args)


# install exception hook: without this, uncaught exception would cause application to exit
sys.excepthook = trap_exc_during_debug


class BotWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        # UI state
        self.ui_state = QLabel()

        # Switch
        self.switch = QCheckBox()
        self.switch.setText('Attack neutral')

        # Thread speed
        self.speed = QDoubleSpinBox()
        self.speed.setMinimum(0.1)
        self.speed.setMaximum(2)
        self.speed.setDecimals(1)
        self.speed.setSingleStep(0.1)
        self.speed.setSuffix('s')
        self.speed.setValue(Worker.interval)
        self.speed.setMaximumWidth(50)

        # Start
        self.btn_start = QPushButton()
        self.btn_start.setText("Start")

        # Stop
        self.btn_stop = QPushButton()
        self.btn_stop.setText("Stop")
        self.btn_stop.setDisabled(True)

        options_hbox = QHBoxLayout()
        options_hbox.addWidget(self.switch)
        options_hbox.addWidget(self.speed)

        btns_hbox = QHBoxLayout()
        btns_hbox.addWidget(self.btn_start)
        btns_hbox.addWidget(self.btn_stop)

        layout = QVBoxLayout()
        layout.addWidget(self.ui_state)
        layout.addLayout(options_hbox)
        layout.addLayout(btns_hbox)

        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

    def setUiState(self, txt):
        self.ui_state.setText(txt)

    def onSwitchToggle(self, action):
        self.switch.toggled.connect(action)

    def onSpeedChange(self, action):
        self.speed.valueChanged.connect(action)

    def onStartClick(self, action):
        self.btn_start.clicked.connect(action)

    def onStopClick(self, action):
        self.btn_stop.clicked.connect(action)


class ConfigWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.log = QTextEdit()

        table = QTableWidget()

        table.insertRow(0)
        table.insertRow(1)
        table.insertRow(2)
        table.insertRow(3)
        table.insertColumn(0)
        table.insertColumn(1)

        item = QTableWidgetItem("editable")
        table.setItem(0, 0, item)

        layout = QVBoxLayout(self)
        layout.addWidget(table)
        self.setLayout(layout)


class LogWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.log = QTextEdit()

        layout = QVBoxLayout(self)
        layout.addWidget(self.log)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

    def append(self, txt):
        self.log.append(txt)


class App(QWidget):
    def __init__(self):
        super().__init__(flags=QtCore.Qt.WindowStaysOnTopHint)

        self.screenWorker = None

        keyboard.add_hotkey('²', self.start_worker)

        self.setWindowTitle("Wow bot")
        self.setWindowIcon(QIcon('./assets/wow_icon.png'))

        # Tabs
        self.bot_widget = BotWidget()
        self.config_widget = ConfigWidget()
        self.log_widget = LogWidget()

        self.bot_widget.onSpeedChange(self.change_worker_interval)
        self.bot_widget.onSwitchToggle(self.toggle_neutral)
        self.bot_widget.onStartClick(self.start_worker)
        self.bot_widget.onStopClick(self.stop_worker)

        main_hbox = QHBoxLayout()

        hbox = QHBoxLayout()

        hbox.addWidget(self.bot_widget)
        hbox.addWidget(self.log_widget)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        main_hbox.addLayout(vbox)

        # main_hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_hbox)
        self.resize(350, 160)
        self.move(460, 780)

    def start_worker(self):
        if self.screenWorker:
            return

        self.bot_widget.setUiState('Starting bot')
        self.bot_widget.btn_start.setDisabled(True)
        self.bot_widget.btn_stop.setEnabled(True)

        worker = Worker()
        # get messages from worker:
        worker.signals.ui.connect(self.on_worker_ui)
        worker.signals.log.connect(self.on_worker_log)
        worker.signals.key.connect(self.on_worker_key)
        worker.signals.done.connect(self.on_worker_done)
        worker.start()

        self.screenWorker = worker

        keyboard.remove_hotkey('²')
        keyboard.add_hotkey('²', self.stop_worker)

    def on_worker_ui(self, ui_txt: str):
        self.bot_widget.setUiState(ui_txt)

    def on_worker_log(self, log_txt: str):
        self.log_widget.append(log_txt)

    def on_worker_key(self, key: str):
        keyboard.send(key)

    def on_worker_done(self):
        self.bot_widget.setUiState('Stopped')
        self.bot_widget.btn_start.setEnabled(True)
        self.bot_widget.btn_stop.setDisabled(True)
        keyboard.remove_hotkey('²')
        keyboard.add_hotkey('²', self.start_worker)

    def stop_worker(self):
        if not self.screenWorker:
            return

        self.screenWorker.stop()
        self.screenWorker.quit()
        self.screenWorker.wait()
        self.screenWorker = None

    @staticmethod
    def change_worker_interval(interval):
        Worker.interval = interval

    @staticmethod
    def toggle_neutral():
        Bot.attack_neutral = not Bot.attack_neutral

    def closeEvent(self, event):
        self.stop_worker()
        event.accept()


if __name__ == "__main__":
    app = QApplication([])

    form = App()
    form.show()

    sys.exit(app.exec_())


