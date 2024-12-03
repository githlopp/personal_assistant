import datetime
import json
from pathlib import Path

class NoteManager:
    def __init__(self):
        self.storage_path = Path("data/notes.json")
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

    def create_note(self):
        data = self._load_data()
        print("\n=== Создание новой заметки ===")
        metadata = {
            "id": len(data) + 1,
            "created_at": datetime.datetime.now().isoformat(),
            "title": input("Название: ").strip(),
            "text": input("Содержание: ").strip(),
            "tags": [tag.strip() for tag in input("Теги (через запятую): ").split(",") if tag.strip()]
        }
        data.append(metadata)
        self._save_data(data)
        print("✓ Заметка сохранена")

    def list_notes(self):
        data = self._load_data()
        if not data:
            print("\nСписок заметок пуст")
            return
        
        print("\n=== Список заметок ===")
        for note in data:
            tags = ", ".join(note["tags"]) if note["tags"] else "без тегов"
            print(f"[{note['id']}] {note['title']} ({tags})")

    def edit_note(self):
        self.list_notes()
        data = self._load_data()
        try:
            note_id = int(input("\nВведите ID заметки для редактирования: "))
            note = next((n for n in data if n["id"] == note_id), None)
            if not note:
                print("❌ Заметка не найдена")
                return
            
            print(f"\nРедактирование заметки [{note_id}]")
            note["title"] = input(f"Название ({note['title']}): ").strip() or note["title"]
            note["text"] = input(f"Содержание ({note['text']}): ").strip() or note["text"]
            new_tags = input(f"Теги ({', '.join(note['tags'])}): ").strip()
            if new_tags:
                note["tags"] = [tag.strip() for tag in new_tags.split(",") if tag.strip()]
            
            self._save_data(data)
            print("✓ Изменения сохранены")
        except ValueError:
            print("❌ Некорректный ID заметки")

    def remove_note(self):
        self.list_notes()
        data = self._load_data()
        try:
            note_id = int(input("\nВведите ID заметки для удаления: "))
            initial_len = len(data)
            data = [n for n in data if n["id"] != note_id]
            
            if len(data) == initial_len:
                print("❌ Заметка не найдена")
                return
                
            self._save_data(data)
            print("✓ Заметка удалена")
        except ValueError:
            print("❌ Некорректный ID заметки")

note_manager = NoteManager()

def menu():
    actions = {
        "1": ("Создать заметку", note_manager.create_note),
        "2": ("Список заметок", note_manager.list_notes),
        "3": ("Редактировать заметку", note_manager.edit_note),
        "4": ("Удалить заметку", note_manager.remove_note),
        "5": ("Назад", None)
    }
    
    while True:
        print("\n=== Управление заметками ===")
        for key, (name, _) in actions.items():
            print(f"{key}. {name}")
            
        choice = input("\nВыберите действие: ").strip()
        if choice not in actions:
            print("❌ Некорректный выбор")
            continue
            
        if choice == "5":
            break
            
        actions[choice][1]()
