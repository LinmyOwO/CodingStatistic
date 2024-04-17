import json


class FileManager:
    def save_json_dump(self, data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file)

    def get_data_from_json(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return None
