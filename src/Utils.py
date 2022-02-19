import datetime
import os
import subprocess
from pathlib import Path

import appscript
import platform

from appscript import app, mactypes


class Utils:

    @staticmethod
    def simple_datetime(year, month, day):
        return datetime.datetime(year, month, day, 0, 0, 0, 0)

    @staticmethod
    def simple_current_datetime():
        now = datetime.datetime.now()
        return Utils.simple_datetime(now.year, now.month, now.day)

    @staticmethod
    def date_info(date_string):
        year = date_string[0:4]
        month = date_string[4:6]
        day = date_string[6:8]
        return {
            'year': int(year),
            'month': int(month),
            'day': int(day)
        }

    @staticmethod
    def today(separator=''):
        today = datetime.date.today()
        return str(today.year) + separator + str(today.month) + separator + str(today.day)

    @staticmethod
    def tomorrow(separator=''):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        return str(tomorrow.year) + separator + str(tomorrow.month) + separator + str(tomorrow.day)

    @staticmethod
    def tomorrow_date():
        today = datetime.date.today()
        return today + datetime.timedelta(days=1)

    @staticmethod
    def yesterday(separator=''):
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        return str(yesterday.year) + separator + str(yesterday.month) + separator + str(yesterday.day)

    @staticmethod
    def day_before(str_date, separator=''):
        date_info = Utils.date_info(str_date)
        current_date = datetime.date(date_info['year'], date_info['month'], date_info['day'])
        day_before = current_date - datetime.timedelta(days=1)
        return {
           'year': day_before.year,
           'month': day_before.month,
           'day': day_before.day,
           'str': str(day_before.year) + separator + str(day_before.month) + separator + str(day_before.day)
        }

    @staticmethod
    def day_after(str_date, separator=''):
        date_info = Utils.date_info(str_date)
        current_date = datetime.date(date_info['year'], date_info['month'], date_info['day'])
        day_after = current_date + datetime.timedelta(days=1)
        return {
            'year': day_after.year,
            'month': day_after.month,
            'day': day_after.day,
            'str': str(day_after.year) + separator + str(day_after.month) + separator + str(day_after.day)
        }

    @staticmethod
    def refresh_background(file_path):
        if platform.system() == 'Darwin':
            SCRIPT = """/usr/bin/osascript<<END
            tell application "Finder"
            set desktop picture to POSIX file "%s"
            end tell
            END"""
            try:
                subprocess.Popen(SCRIPT%file_path, shell=True)
            #try:
            #    app('Finder').desktop_picture.set(mactypes.File(file_path))
            except appscript.reference.CommandError as error:
                Utils.save_error_file(error)

    @staticmethod
    def save_error_file(error):
        lines = list()
        lines.append("message: " + str(error.errormessage) + "\n")
        lines.append("error number: " + str(error.errornumber) + "\n")
        lines.append("command: " + str(error.command) + "\n")
        lines.append("parameters:" + "\n")
        for param in error.parameters:
            lines.append(str(param) + "\n")
        lines.append("------------" + "\n")

        home = Utils.get_home_path()
        f = open(home + "error", "a")
        f.writelines(lines)
        f.close()

    @staticmethod
    def save_lock_file(value):
        home = Utils.get_home_path()
        f = open(home + "lock", "w")
        f.write(value)
        f.close()

    @staticmethod
    def read_lock_file():
        home = Utils.get_home_path()
        value = None
        if os.path.exists(home + "lock"):
            f = open(home + "lock", "r")
            value = f.read()
            f.close()
        return value

    @staticmethod
    def get_home_path():
        home = str(Path.home())
        if not home.endswith('/'):
            home += '/'
        return home

    @staticmethod
    def date_int_to_str(value):
        if value < 10:
            return '0' + str(value)
        return str(value)
