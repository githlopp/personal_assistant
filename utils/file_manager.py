import json
import csv

class FileManager:
    @staticmethod
    def load_json(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Ошибка чтения JSON. Проверьте файл.")
            return []

    @staticmethod
    def save_json(file_path, data):
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @staticmethod
    def export_to_csv(file_path, data):
        if not data:
            print("Нет данных для экспорта.")
            return
        keys = data[0].keys()
        with open(file_path, "w", newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def import_from_csv(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                return [row for row in reader]
        except FileNotFoundError:
            print("Файл не найден.")
            return []
