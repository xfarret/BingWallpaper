import os.path

import yaml

from Utils import Utils


class Settings:

    def __init__(self, config_yaml_path = None):
        self.icon_list = ['bing-symbolic', 'brick-symbolic', 'high-frame-symbolic', 'mid-frame-symbolic', 'low-frame-symbolic']
        self.resolutions = ['auto', 'UHD', '1920x1200', '1920x1080', '1366x768', '1280x720', '1024x768', '800x600']
        self.markets = ['auto', 'ar-XA', 'da-DK', 'de-AT', 'de-CH', 'de-DE', 'en-AU', 'en-CA', 'en-GB',
                   'en-ID', 'en-IE', 'en-IN', 'en-MY', 'en-NZ', 'en-PH', 'en-SG', 'en-US', 'en-WW', 'en-XA', 'en-ZA',
                   'es-AR',
                   'es-CL', 'es-ES', 'es-MX', 'es-US', 'es-XL', 'et-EE', 'fi-FI', 'fr-BE', 'fr-CA', 'fr-CH', 'fr-FR',
                   'he-IL', 'hr-HR', 'hu-HU', 'it-IT', 'ja-JP', 'ko-KR', 'lt-LT', 'lv-LV', 'nb-NO', 'nl-BE', 'nl-NL',
                   'pl-PL', 'pt-BR', 'pt-PT', 'ro-RO', 'ru-RU', 'sk-SK', 'sl-SL', 'sv-SE', 'th-TH', 'tr-TR', 'uk-UA',
                   'zh-CN', 'zh-HK', 'zh-TW']
        self.marketName = [
            'auto', '(شبه الجزيرة العربية‎) العربية', 'dansk (Danmark)', 'Deutsch (Österreich)',
            'Deutsch (Schweiz)', 'Deutsch (Deutschland)', 'English (Australia)', 'English (Canada)',
            'English (United Kingdom)', 'English (Indonesia)', 'English (Ireland)', 'English (India)', 'English (Malaysia)',
            'English (New Zealand)', 'English (Philippines)', 'English (Singapore)', 'English (United States)',
            'English (International)', 'English (Arabia)', 'English (South Africa)', 'español (Argentina)',
            'español (Chile)',
            'español (España)', 'español (México)', 'español (Estados Unidos)', 'español (Latinoamérica)', 'eesti (Eesti)',
            'suomi (Suomi)', 'français (Belgique)', 'français (Canada)', 'français (Suisse)', 'français (France)',
            '(עברית (ישראל', 'hrvatski (Hrvatska)', 'magyar (Magyarország)', 'italiano (Italia)', '日本語 (日本)', '한국어(대한민국)',
            'lietuvių (Lietuva)', 'latviešu (Latvija)', 'norsk bokmål (Norge)', 'Nederlands (België)',
            'Nederlands (Nederland)',
            'polski (Polska)', 'português (Brasil)', 'português (Portugal)', 'română (România)', 'русский (Россия)',
            'slovenčina (Slovensko)', 'slovenščina (Slovenija)', 'svenska (Sverige)', 'ไทย (ไทย)', 'Türkçe (Türkiye)',
            'українська (Україна)', '中文（中国）', '中文（中國香港特別行政區）', '中文（台灣）'
        ]
        self.backgroundStyle = ['none', 'wallpaper', 'centered', 'scaled', 'stretched', 'zoom', 'spanned']

        if config_yaml_path is None:
            home = Utils.get_home_path()
            self.config_yaml_path = home + "config.yml"
        else:
            self.config_yaml_path = config_yaml_path
        self.params = {}
        self.__read_config_yaml_file()
        self.__set_default_params()

    def __read_config_yaml_file(self):
        if os.path.exists(self.config_yaml_path):
            with open(self.config_yaml_path, 'r') as file:
                config_file = yaml.safe_load(file)
                if 'Bing' in config_file:
                    if 'resolution' in config_file['Bing']:
                        self.params['resolution'] = config_file['Bing']['resolution']

                    if 'market' in config_file['Bing']:
                        self.params['market'] = config_file['Bing']['market']

                    if 'galery_path' in config_file['Bing']:
                        galery_path = config_file['Bing']['galery_path']
                        if not str.endswith(galery_path, "/"):
                            galery_path += "/"
                        self.params['galery_path'] = galery_path

                    if 'interval_check' in config_file['Bing']:
                        self.params['interval_check'] = float(config_file['Bing']['interval_check'])

    def __set_default_params(self):
        if 'resolution' not in self.params:
            self.params['resolution'] = "UHD"
        if 'market' not in self.params:
            self.params['market'] = "fr-FR"
        if 'galery_path' not in self.params:
            home = Utils.get_home_path()
            default_galery_path = home + "/bing"
            if not os.path.exists(default_galery_path):
                os.makedirs(default_galery_path)
            self.params['galery_path'] = default_galery_path
        if 'interval_check' not in self.params:
            self.params['interval_check'] = float(300)
        self.params['file_separator'] = "_"
        self.params["bing_url"] = "https://www.bing.com"
