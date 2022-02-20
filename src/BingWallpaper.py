#!/usr/bin/env python3
import argparse
import time

from Bing import Bing
from Ui.AppGui import AppGui
from Utils import Utils


def check_image(bing, check_date=None):
    if check_date is None:
        image = bing.get_current_image()
    else:
        date_info = Utils.date_info(check_date)
        image = bing.get_image_by_date(date_info['year'], date_info['month'], date_info['day'])
        if image is None:
            image = check_image(bing)
    if image is not None:
        file_path =bing.get_image_path(image)
        if file_path is not None:
            Utils.refresh_background(file_path)
    return image


def check_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--daemon", action="store_true", help="daemon mode")
    parser.add_argument("-c", "--config", help="yaml config file path")
    parser.add_argument("-g", "--gui", action="store_true", help="gui mode")
    parser.add_argument("-ymd", "--date", help="specify a date with format year month day")
    return parser.parse_args()


if __name__ == '__main__':
    args = check_arguments()
    bing = Bing(args.config)

    if args.gui is not None:
        lock_date = Utils.read_lock_file()
        # si la date est celle d'hier alors on charge la nouvelle image, sinon on charge l'image spécifique
        if lock_date is not None and lock_date == Utils.yesterday():
            image = check_image(bing)
        else:
            image = check_image(bing, lock_date)
        app = AppGui(bing, image)

    else:
        if args.date is not None:
            check_image(bing, args.date)
        else:
            check_image(bing)

            if args.daemon:
                while True:
                    time.sleep(bing.settings.params['interval_check'])
                    lock_date = Utils.read_lock_file()
                    if lock_date is None or lock_date != Utils.today():
                        print("checking image")
                        check_image(bing)
