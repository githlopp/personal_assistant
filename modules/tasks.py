import json
from pathlib import Path

class TaskManager:
    def __init__(self):
        self.storage_path = Path("data/tasks.json")
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

    def add_task(self):
        data = self._load_data()
        print("\n=== Добавление новой задачи ===")
        task = {
            "id": len(data) + 1,
            "title": input("Краткое описание: ").strip(),
            "description": input("Подробное описание: ").strip(),
            "done": False,
            "priority": input("Приоритет (Высокий/Средний/Низкий): ").strip(),
            "due_date": input("Срок выполнения (ДД-ММ-ГГГГ): ").strip()
        }
        data.append(task)
        self._save_data(data)
        print("✓ Задача добавлена")

    def list_tasks(self):
        data = self._load_data()
        if not data:
            print("\nСписок задач пуст")
            return

        print("\n=== Список задач ===")
        for task in data:
            status = "Выполнена" if task["done"] else "Не выполнена"
            print(f"[{task['id']}] {task['title']} - {status} ({task['priority']})")

    def mark_task_done(self):
        self.list_tasks()
        data = self._load_data()
        try:
            task_id = int(input("\nВведите ID задачи для отметки как выполненной: "))
            task = next((t for t in data if t["id"] == task_id), None)
            if not task:
                print("❌ Задача не найдена")
                return

            task["done"] = True
            self._save_data(data)
            print("✓ Задача отмечена как выполненная")
        except ValueError:
            print("❌ Некорректный ID задачи")

    def edit_task(self):
        self.list_tasks()
        data = self._load_data()
        try:
            task_id = int(input("\nВведите ID задачи для редактирования: "))
            task = next((t for t in data if t["id"] == task_id), None)
            if not task:
                print("❌ Задача не найдена")
                return

            print(f"\nРедактирование задачи [{task_id}]")
            task["title"] = input(f"Краткое описание ({task['title']}): ").strip() or task["title"]
            task["description"] = input(f"Подробное описание ({task['description']}): ").strip() or task["description"]
            task["priority"] = input(f"Приоритет ({task['priority']}): ").strip() or task["priority"]
            task["due_date"] = input(f"Срок выполнения ({task['due_date']}): ").strip() or task["due_date"]
            self._save_data(data)
            print("✓ Изменения сохранены")
        except ValueError:
            print("❌ Некорректный ID задачи")

    def remove_task(self):
        self.list_tasks()
        data = self._load_data()
        try:
            task_id = int(input("\nВведите ID задачи для удаления: "))
            initial_len = len(data)
            data = [t for t in data if t["id"] != task_id]

            if len(data) == initial_len:
                print("❌ Задача не найдена")
                return

            self._save_data(data)
            print("✓ Задача удалена")
        except ValueError:
            print("❌ Некорректный ID задачи")

task_manager = TaskManager()

def menu():
    actions = {
        "1": ("Добавить задачу", task_manager.add_task),
        "2": ("Список задач", task_manager.list_tasks),
        "3": ("Отметить задачу как выполненную", task_manager.mark_task_done),
        "4": ("Редактировать задачу", task_manager.edit_task),
        "5": ("Удалить задачу", task_manager.remove_task),
        "6": ("Назад", None)
    }

    while True:
        print("\n=== Управление задачами ===")
        for key, (name, _) in actions.items():
            print(f"{key}. {name}")

        choice = input("\nВыберите действие: ").strip()
        if choice not in actions:
            print("❌ Некорректный выбор")
            continue

        if choice == "6":
            break

        actions[choice][1]()
