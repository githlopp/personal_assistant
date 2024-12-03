def menu():
    while True:
        print("\nКалькулятор:")
        print("Введите выражение для вычисления (например, 2 + 2) или 'назад' для возврата в меню:")
        expression = input("Ваше выражение: ").strip()
        if expression.lower() == "назад":
            break
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            print(f"Результат: {result}")
        except ZeroDivisionError:
            print("Ошибка: Деление на ноль.")
        except Exception as e:
            print(f"Ошибка в выражении: {e}")
