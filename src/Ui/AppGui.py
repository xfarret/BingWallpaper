import sys
from datetime import date

from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import *
from apscheduler.triggers.date import DateTrigger

# from Ui.ThreadWorker import ThreadWorker
from Utils import Utils


class AppGui:
    def __init__(self, bing, image):
        self.bing = bing
        self.image = image
        self.lock_mode = False

        self.menu = {}

        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        # Create the icon
        icon = QIcon("icons/bing-symbolic.svg")

        # Create the tray
        tray = QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)

        # Create the menu
        menu = QMenu()
        refresh_action = QAction("Refresh now")
        refresh_action.triggered.connect(self.refresh_now)
        menu.addAction(refresh_action)

        prev_action = QAction("Previous")
        prev_action.triggered.connect(self.previous_image)
        menu.addAction(prev_action)

        next_action = QAction("Next")
        next_action.triggered.connect(self.next_image)
        menu.addAction(next_action)

        menu.addSeparator()

        title_item = QWidgetAction(menu)
        title_label = QLabel(image.title)
        title_label.setContentsMargins(5, 0, 0, 0)
        title_item.setDefaultWidget(title_label)
        menu.addAction(title_item)

        image_item = QWidgetAction(menu)
        img = QImage()
        img.loadFromData(self.image.content)
        img = img.scaledToWidth(400)
        img = img.scaledToHeight(225)
        img_label = QLabel()
        img_label.setPixmap(QPixmap.fromImage(img))
        image_item.setDefaultWidget(img_label)
        menu.addAction(image_item)

        info_item = QWidgetAction(menu)
        info_label = QLabel(image.info)
        info_label.setContentsMargins(5, 0, 0, 0)
        info_item.setDefaultWidget(info_label)
        menu.addAction(info_item)

        copyright_item = QWidgetAction(menu)
        copyright_label = QLabel(image.copyright)
        copyright_label.setContentsMargins(0, 0, 5, 0)
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        copyright_item.setDefaultWidget(copyright_label)
        menu.addAction(copyright_item)

        menu.addSeparator()

        # Add a Quit option to the menu.
        quit = QAction("Quit")
        quit.triggered.connect(self.__quit)
        menu.addAction(quit)

        # Add the menu to the tray
        tray.setContextMenu(menu)

        self.menu['menu'] = menu
        self.menu['title_label'] = title_label
        self.menu['info_label'] = info_label
        self.menu['copyright_label'] = copyright_label
        self.menu['img_label'] = img_label

        self.thread_stop_mode = False
        # self.thread = ThreadWorker(self, self.gui_event_timer)

        # Scheduler's initialisation which aim is to trigger an event
        listener_job = (EVENT_JOB_ADDED |
                        EVENT_JOB_REMOVED |
                        EVENT_JOB_MODIFIED |
                        EVENT_JOB_EXECUTED |
                        EVENT_JOB_ERROR |
                        EVENT_JOB_MISSED)
        self.scheduler = BackgroundScheduler(timezone="Europe/Paris")
        self.scheduler.add_listener(self.err_listener, listener_job)
        tomorrow = Utils.tomorrow("-")
        trigger = DateTrigger(run_date=tomorrow)
        self.scheduler.add_job(self.gui_event_scheduler, trigger)
        self.scheduler.start()

        self.app.exec()

    def refresh_now(self):
        """

        :return:
        """
        self.image = self.bing.get_current_image()
        Utils.refresh_background(self.bing.get_image_path(self.image))
        self.__refresh_ui()
        self.lock_mode = False

    def previous_image(self):
        """

        :return:
        """
        prev_date = Utils.day_before(self.image.date)
        img = self.bing.get_image_by_date(prev_date['year'], prev_date['month'], prev_date['day'])
        if img is not None:
            self.image = img
            Utils.refresh_background(self.bing.get_image_path(self.image))
            self.__refresh_ui()
        self.lock_mode = True

    def next_image(self):
        """

        :return:
        """
        next_date = Utils.day_after(self.image.date)
        img = self.bing.get_image_by_date(next_date['year'], next_date['month'], next_date['day'])
        if img is not None:
            self.image = img
            Utils.refresh_background(self.bing.get_image_path(self.image))
            self.__refresh_ui()
        self.lock_mode = True

    # def gui_event_timer(self):
    #     """
    #
    #     :return:
    #     """
    #     if not self.thread_stop_mode:
    #         if not self.lock_mode:
    #             self.refresh_now()
    #         else:
    #             # We get the new image without changing the background
    #             self.image = self.bing.get_current_image()

    def gui_event_scheduler(self):
        """

        :return:
        """
        print("started")
        self.scheduler.pause()
        if not self.lock_mode:
            self.refresh_now()
        else:
            # We get the new image without changing the background
            self.image = self.bing.get_current_image()
        self.scheduler.remove_all_jobs()
        tomorrow = Utils.tomorrow("-")
        trigger = DateTrigger(run_date=tomorrow)
        self.scheduler.add_job(self.gui_event_scheduler, trigger)
        self.scheduler.resume()

    def err_listener(self, events):
        """

        :param events:
        :return:
        """
        event_name = "Undefined"
        if events.code == EVENT_JOB_ADDED:
            event_name = "Event Job Added"
        if events.code == EVENT_JOB_REMOVED:
            event_name = "Event Job Removed"
        if events.code == EVENT_JOB_MODIFIED:
            event_name = "Event Job Modified"
        if events.code == EVENT_JOB_EXECUTED:
            event_name = "Event Job Executed"
        if events.code == EVENT_JOB_ERROR:
            event_name = "Event Job Error"
        if events.code == EVENT_JOB_MISSED:
            event_name = "Event Job Missed"
        if events.code == EVENT_JOB_SUBMITTED:
            event_name = "Event Job Submited"

        Utils.add_log("Event fired : " + event_name + ", date : " + Utils.current_datetime('-', ':')['str'])
        if events.code == EVENT_JOB_MISSED:
            self.gui_event_scheduler()

    def __refresh_ui(self):
        """

        :return:
        """
        self.menu['title_label'].setText(self.image.title)
        self.menu['info_label'].setText(self.image.info)
        self.menu['copyright_label'].setText(self.image.copyright)
        img = QImage()
        img.loadFromData(self.image.content)
        img = img.scaledToWidth(400)
        img = img.scaledToHeight(225)
        self.menu['img_label'].setPixmap(QPixmap.fromImage(img))

    def __quit(self):
        self.thread_stop_mode = True
        self.scheduler.pause()
        # self.thread.stop()
        self.app.quit()
