import threading
from threading import Thread


class ThreadWorker(Thread):
    def __init__(self, app, fn_call):
        super().__init__()
        self.event = threading.Event()
        self.app = app
        self.fn_call = fn_call

    def run(self):
        while not self.app.thread_stop_mode:
            print("start")
            self.event.wait(float(self.app.bing.settings.params['interval_check']))
            self.fn_call()
            print("end")

    def stop(self):
        self.event.set()
