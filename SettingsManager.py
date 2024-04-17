from FileManager import FileManager

file_manager = FileManager()


class SettingsManager:
    DEFAULT_SETTINGS = {
        'number_length': 3,
        'number_amount': 100,
        'left_border': 100,
        'right_border': 199,
        'time_save_amount_per_number': 25
        # 'time_for_element'
    }
    settings = DEFAULT_SETTINGS

    def load_settings(self, filename="settings.json"):
        self.settings = file_manager.get_data_from_json(filename)\
                        or self.DEFAULT_SETTINGS
        return self.settings

    def save_settings(self, filename="settings.json"):
        file_manager.save_json_dump(self.settings, filename)

    def set_default_settings(self):
        self.settings = self.DEFAULT_SETTINGS

    def set_settings(self, settings):
        self.settings = settings
