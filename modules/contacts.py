import json
from pathlib import Path

class ContactManager:
    def __init__(self):
        self.storage_path = Path("data/contacts.json")
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

    def add_contact(self):
        data = self._load_data()
        print("\n=== Добавление нового контакта ===")
        contact = {
            "id": len(data) + 1,
            "name": input("Имя: ").strip(),
            "phone": input("Телефон: ").strip(),
            "email": input("Email: ").strip()
        }
        data.append(contact)
        self._save_data(data)
        print("✓ Контакт добавлен")

    def list_contacts(self):
        data = self._load_data()
        if not data:
            print("\nСписок контактов пуст")
            return

        print("\n=== Список контактов ===")
        for contact in data:
            print(f"[{contact['id']}] {contact['name']} - {contact['phone']} - {contact['email']}")

    def edit_contact(self):
        self.list_contacts()
        data = self._load_data()
        try:
            contact_id = int(input("\nВведите ID контакта для редактирования: "))
            contact = next((c for c in data if c["id"] == contact_id), None)
            if not contact:
                print("❌ Контакт не найден")
                return

            print(f"\nРедактирование контакта [{contact_id}]")
            contact["name"] = input(f"Имя ({contact['name']}): ").strip() or contact["name"]
            contact["phone"] = input(f"Телефон ({contact['phone']}): ").strip() or contact["phone"]
            contact["email"] = input(f"Email ({contact['email']}): ").strip() or contact["email"]
            self._save_data(data)
            print("✓ Изменения сохранены")
        except ValueError:
            print("❌ Некорректный ID контакта")

    def remove_contact(self):
        self.list_contacts()
        data = self._load_data()
        try:
            contact_id = int(input("\nВведите ID контакта для удаления: "))
            initial_len = len(data)
            data = [c for c in data if c["id"] != contact_id]

            if len(data) == initial_len:
                print("❌ Контакт не найден")
                return

            self._save_data(data)
            print("✓ Контакт удалён")
        except ValueError:
            print("❌ Некорректный ID контакта")

contact_manager = ContactManager()

def menu():
    actions = {
        "1": ("Добавить контакт", contact_manager.add_contact),
        "2": ("Список контактов", contact_manager.list_contacts),
        "3": ("Редактировать контакт", contact_manager.edit_contact),
        "4": ("Удалить контакт", contact_manager.remove_contact),
        "5": ("Назад", None)
    }

    while True:
        print("\n=== Управление контактами ===")
        for key, (name, _) in actions.items():
            print(f"{key}. {name}")

        choice = input("\nВыберите действие: ").strip()
        if choice not in actions:
            print("❌ Некорректный выбор")
            continue

        if choice == "5":
            break

        actions[choice][1]()
