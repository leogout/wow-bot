import time
from PyQt5.QtCore import pyqtSignal, QThread, QObject
import screen
import formatter
from bot import VindictBot, ProtectionBot


class WorkerSignals(QObject):
    ui = pyqtSignal(str)
    log = pyqtSignal(str)
    key = pyqtSignal(str)
    done = pyqtSignal()


class Worker(QThread):
    interval = 0.5

    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()
        self.running = False
        #self.bot = ProtectionBot()
        self.bot = VindictBot()

    def run(self):
        self.running = True

        while self.running:
            time.sleep(Worker.interval)
            data = screen.get_data()

            self.signals.ui.emit(formatter.paladin(data))

            p_spell = self.bot.react(data)

            if p_spell is not None:
                log = '{}'.format(p_spell['label'])
                key = p_spell['spell']['key']

                self.signals.key.emit(key)
                self.signals.log.emit(log)

        self.signals.done.emit()

    def stop(self):
        self.running = False
