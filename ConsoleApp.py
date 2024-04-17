import os
import time
from number_generator import *
from Printer import ExcelPrinter
from FileManager import FileManager
from SettingsManager import SettingsManager
from DataHandler import DataHandler

CONSENT = ('Y', 'y', 'Yes', 'yes', 'Н', 'н')
REFUSAL = ('N', 'n', 'No', 'no', 'Т', 'т')

file_manager = FileManager()
data_handler = DataHandler()
settings_manager = SettingsManager()


class ConsoleApp:
    def __init__(self):
        print("Приложение запущено")

        print("Загрузка данных...", end="")
        self.data = file_manager.get_data_from_json('data.json') or {}
        time.sleep(1)
        print("Готово.")

        print("Загрузка настроек...", end='')
        settings_manager.load_settings("settings.json")
        time.sleep(1)
        print("Готово.")

    def run_app(self):
        while True:
            self.print_menu()
            command = input()

            time.sleep(0.3)
            os.system('cls')

            match command:
                case "start":
                    self.start_training(settings_manager.settings['number_amount'])
                case "rules":
                    self.rules()
                case "statistic":
                    self.look_statistic()
                case "settings":
                    self.manage_settings()
                case "exit":
                    if self.exit():
                        break
                case _:
                    print("Команда не распознана")
                    time.sleep(1)

    def print_menu(self):
        os.system('cls')
        offset = "* "

        print("Главное меню")
        print(f"{offset}Старт (start)")

        self.print_current_settings()

        # print(f"{offset}Правила (rules)")
        print(f"{offset}Статистика (statistic)")
        print(f"{offset}Настройки (settings)")
        print(f"{offset}Выход (exit)")

    def print_current_settings(self):
        amount = settings_manager.settings['number_amount']
        digits = settings_manager.settings['number_length']
        left = str(settings_manager.settings['left_border'])
        right = str(settings_manager.settings['right_border'])

        left = '0' * (digits - len(left)) + left
        right = '0' * (digits - len(right)) + right

        setting_string = f"({digits}-значные числа | интервал от {left} до {right}" \
                         f" | количество чисел - {amount})"
        print(setting_string)

    def start_training(self, number_amount=10):
        ready = input("Вы готовы начать? [Y/n](по умолчанию \'Y\') ") or 'Y'
        if ready not in CONSENT:
            return

        settings = settings_manager.settings

        numbers = generate_unique_array(
            number_amount,
            settings['number_length'],
            settings['left_border'],
            settings['right_border']
        )

        finished = True
        for number in numbers:
            number = str(number)
            number = '0' * (settings['number_length'] - len(number)) + number
            print(number)

            timer_start = time.time()
            command = input()
            timer_finish = time.time()

            if command and command == 'q' or command == 'й':
                finished = False
                break

            running_time = timer_finish - timer_start

            data_handler.handle_result(self.data, number, running_time)
            os.system('cls')

        if finished:
            print("Тренажер завершен")
            file_manager.save_json_dump(self.data, "data.json")
            self.print_stat_to_excel()
            time.sleep(0.5)
        else:
            print("Работа остановлена")

    def rules(self):
        print("На экране будут появляться различные числа из определенного промежутка "
              "чисел(возможна настройка). Сразу после того, как Вы вспомнили ассоциацию"
              " с этим числом, нажмите Enter для отсечки времени. При необходимости, "
              "чтобы прервать игру, нажмите q/й и Enter.")

    def look_statistic(self):
        print("Для просмотра статистики требуется закрыть приложение и "
              "открыть файл \"statistic.xslx\"")
        time.sleep(2)

    def manage_settings(self):
        settings = settings_manager.settings
        sorted_settings = sorted(list(settings.keys()))

        while True:
            self.print_settings(sorted_settings)

            setting = input("Введите название настройки: ") or '_'
            while setting not in settings:
                if setting == "back":
                    settings_manager.set_settings(settings)
                    settings_manager.save_settings("settings.json")
                    return
                if setting == "default":
                    settings_manager.set_default_settings()
                    return

                print("Настройка не найдена")
                setting = input("Настройка: ") or '_'

            value = input(f"Новое значение {setting}(текущее - {settings[setting]}): ")
            msg = self.validate_value(setting, value)
            if msg:
                print(f"Ошибка: {msg}")
                time.sleep(2.5)
                continue

            if not value:
                default_value = settings_manager.DEFAULT_SETTINGS[setting]
                print(f"Будет выставлено значение по умолчанию: {default_value}")
                settings[setting] = default_value
                time.sleep(1)
            else:
                settings[setting] = int(value)

    def print_settings(self, settings):
        os.system('cls')

        offset = "*-"
        print("* Настройки *")

        for setting in settings:
            print(f"{offset} {setting}")

        print(f"{offset} Сбросить до значений по умолчанию (default)")
        print("<- Назад (back)")

    # костыльная валидация на первое время
    def validate_value(self, setting, value):
        invalid_input = "Некорректный ввод"

        # isdigit() исключает отрицательные
        if not value.isdigit():
            return invalid_input
        value = int(value)

        digits = settings_manager.settings['number_length']
        left = settings_manager.settings['left_border']
        right = settings_manager.settings['right_border']

        match setting:
            case "number_length":
                if value:
                    settings_manager.settings['left_border'] = 0
                    settings_manager.settings['right_border'] = 10 ** value - 1
                else:
                    return invalid_input

            case "left_border":
                is_in_borders = 0 <= value <= 10 ** digits - 1
                if not is_in_borders:
                    return f"Число не {digits}-значное"
                if value > right:
                    return "Левая граница не может быть больше правой"
                settings_manager.settings['number_amount'] = right - value + 1

            case "right_border":
                is_in_borders = 10 ** (digits - 1) <= value <= 10 ** digits - 1
                if not is_in_borders:
                    return f"Число не {digits}-значное"
                if value < left:
                    return "Левая граница не может быть больше правой"
                settings_manager.settings['number_amount'] = value - left + 1

            case "number_amount":
                if not value:
                    return "Количество чисел не может быть равным нулю"

        return None

    def exit(self):
        answer = input("Вы уверены, что хотите выйти? [Y/n] ") or 'Y'
        if answer in CONSENT:
            print("До свидания!")
            return True
        return False

    def print_stat_to_excel(self):
        printer = ExcelPrinter()
        printer.print(self.data)
