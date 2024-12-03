from modules import notes, tasks, contacts, finance, calculator

class PersonalAssistantApp:
    def __init__(self):
        self.modules = {
            'notes': notes,
            'tasks': tasks,
            'contacts': contacts,
            'finance': finance,
            'calculator': calculator
        }
        self.menu_options = {
            '1': ('Управление заметками', 'notes'),
            '2': ('Управление задачами', 'tasks'),
            '3': ('Управление контактами', 'contacts'),
            '4': ('Управление финансовыми записями', 'finance'),
            '5': ('Калькулятор', 'calculator')
        }

    def display_menu(self):
        print("\nДобро пожаловать в Персональный помощник!")
        print("Выберите действие:")
        for key, (name, _) in self.menu_options.items():
            print(f"{key}. {name}")
        print("6. Выход")

    def process_choice(self, choice):
        if choice in self.menu_options:
            module_name = self.menu_options[choice][1]
            self.modules[module_name].menu()
            return True
        elif choice == '6':
            print("Программа завершена. До свидания!")
            return False
        else:
            print("Некорректный ввод. Пожалуйста, попробуйте снова.")
            return True

    def run(self):
        while True:
            self.display_menu()
            user_choice = input("\nВыберите пункт меню: ").strip()
            if not self.process_choice(user_choice):
                break

def main():
    app = PersonalAssistantApp()
    app.run()

if __name__ == "__main__":
    main()
