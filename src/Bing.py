import os.path

import requests

from Settings import Settings
from Image import Image
from Utils import Utils


class Bing:
    def __init__(self, config_file_path=None):
        """
        :param config_file_path: configuration file path
        """
        self.settings = Settings(config_file_path)

    def list_images(self, indice=0):
        """
        Get images list at a specific indice
        :param indice: int
        :return: Optional[json]
        """
        listing_url = self.settings.params["bing_url"] + "/HPImageArchive.aspx?format=js&idx="
        listing_url += str(indice) + "&n=8&mbl=1&mkt=" + self.settings.params["market"]
        res = requests.get(listing_url)
        if res.status_code == 200:
            return res.json()
        return None

    def get_current_image(self, list_images=None):
        """
        Get current image at indice 0 of the images list
        :param list_images: the preloaded list images
        :return: Optional[Image]
        """
        return self.get_image_by_index(0, 0, list_images)

    def get_image_by_index(self, index=0, image_index=0, list_images=None):
        """
        Get an image at a specific position and a specific index and save it on the filesystem
        :param index: index for looking for the list images containing the image required
        :param image_index: the image at index position
        :param list_images: the preloaded list images
        :return: Optional[Image]
        """
        if list_images is not None:
            result_list = list_images
        else:
            result_list = self.list_images(index)
        url_base = result_list["images"][image_index]['urlbase']
        resolution = self.settings.params["resolution"]
        url_image = self.settings.params["bing_url"] + url_base + "_" + resolution + ".jpg&rf=LaDigue_" + resolution + ".jpg&pid=hp"
        image_pathname = self.settings.params['galery_path'] + self.get_formatted_pathname(result_list["images"][image_index]["enddate"])
        title = result_list["images"][image_index]['title']
        copyright = result_list["images"][image_index]['copyright']
        end_date = result_list["images"][image_index]['enddate']

        image = None
        if not os.path.exists(image_pathname):
            res = requests.get(url_image)
            if res.status_code == 200:
                image = Image(res.content, title, copyright, end_date)
                self.save_image(image)
        else:
            with open(image_pathname, "rb") as image:
                f = image.read()
                image = Image(f, title, copyright, end_date)

        if image is not None:
            Utils.save_lock_file(image.date)

        return image

    def get_image_by_date(self, year, month, day):
        """
        Get an image for a specific date
        :param year:
        :param month:
        :param day:
        :return: Optional[Image]
        """
        current_datetime = Utils.simple_current_datetime()
        required_datetime = Utils.simple_datetime(year, month, day)

        nb_interval = current_datetime - required_datetime
        if nb_interval.days <= 12:
            step = nb_interval.days % 7
            list_images = self.list_images(step)
            date_to_search = str(year) + Utils.date_int_to_str(month) + Utils.date_int_to_str(day)
            for key, image in enumerate(list_images['images']):
                if image['enddate'] == date_to_search:
                    return self.get_image_by_index(step, key, list_images)
        return None

    def save_image(self, image):
        """
        Save an image to the gallery path
        :param image:
        :return: the path file saved
        """
        if not os.path.exists(self.settings.params['galery_path']):
            os.mkdir(self.settings.params['galery_path'])

        path_file_name = self.get_image_path(image)
        if not os.path.exists(path_file_name):
            f = open(path_file_name, "wb")
            f.write(image.content)
            f.close()

        return path_file_name

    def get_image_path(self, image):
        """
        Get the path file for an image. It doesn't check if the file exists on the filesystem
        :param image:
        :return: the path file
        """
        title = self.get_formatted_pathname(image.date)
        path_file_name = self.settings.params['galery_path'] + title
        return path_file_name

    def get_formatted_pathname(self, value):
        """
        Format the file name. White spaces are replaced by a file separator defined in the config file, and the
        resolution is added
        :param value: the title of the image
        :return: a value formatted
        """
        separator = self.settings.params['file_separator']
        resolution = self.settings.params['resolution']
        market = self.settings.params['market']
        return str(value) + separator + market + separator + resolution + ".jpg"
