import json
from pathlib import Path

class FinanceManager:
    def __init__(self):
        self.storage_path = Path("data/finance.json")
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            self.storage_path.write_text('[]')

    def _load_data(self):
        try:
            return json.loads(self.storage_path.read_text())
        except Exception:
            return []

    def _save_data(self, data):
        self.storage_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    def add_record(self):
        data = self._load_data()
        print("\n=== Добавление финансовой записи ===")
        record = {
            "id": len(data) + 1,
            "amount": float(input("Сумма: ").strip()),
            "category": input("Категория: ").strip(),
            "date": input("Дата (ДД-ММ-ГГГГ): ").strip(),
            "description": input("Описание: ").strip()
        }
        data.append(record)
        self._save_data(data)
        print("✓ Финансовая запись добавлена")

    def list_records(self):
        data = self._load_data()
        if not data:
            print("\nСписок финансовых записей пуст")
            return

        print("\n=== Список финансовых записей ===")
        for record in data:
            print(f"[{record['id']}] {record['amount']} - {record['category']} - {record['date']}")

    def edit_record(self):
        self.list_records()
        data = self._load_data()
        try:
            record_id = int(input("\nВведите ID записи для редактирования: "))
            record = next((r for r in data if r["id"] == record_id), None)
            if not record:
                print("❌ Запись не найдена")
                return

            print(f"\nРедактирование записи [{record_id}]")
            record["amount"] = float(input(f"Сумма ({record['amount']}): ").strip() or record["amount"])
            record["category"] = input(f"Категория ({record['category']}): ").strip() or record["category"]
            record["date"] = input(f"Дата ({record['date']}): ").strip() or record["date"]
            record["description"] = input(f"Описание ({record['description']}): ").strip() or record["description"]
            self._save_data(data)
            print("✓ Изменения сохранены")
        except ValueError:
            print("❌ Некорректный ID записи")

    def remove_record(self):
        self.list_records()
        data = self._load_data()
        try:
            record_id = int(input("\nВведите ID записи для удаления: "))
            initial_len = len(data)
            data = [r for r in data if r["id"] != record_id]

            if len(data) == initial_len:
                print("❌ Запись не найдена")
                return

            self._save_data(data)
            print("✓ Запись удалена")
        except ValueError:
            print("❌ Некорректный ID записи")

finance_manager = FinanceManager()

def menu():
    actions = {
        "1": ("Добавить запись", finance_manager.add_record),
        "2": ("Список записей", finance_manager.list_records),
        "3": ("Редактировать запись", finance_manager.edit_record),
        "4": ("Удалить запись", finance_manager.remove_record),
        "5": ("Назад", None)
    }

    while True:
        print("\n=== Управление финансовыми записями ===")
        for key, (name, _) in actions.items():
            print(f"{key}. {name}")

        choice = input("\nВыберите действие: ").strip()
        if choice not in actions:
            print("❌ Некорректный выбор")
            continue

        if choice == "5":
            break

        actions[choice][1]()
