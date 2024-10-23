import random  # Імпортуємо модуль для генерації випадкових чисел.
import json    # Імпортуємо модуль для роботи з JSON.
import os      # Імпортуємо модуль для роботи з файловою системою.

class ConstantTable:
    """Клас для операцій з таблицею констант."""

    def __init__(self, default_constants=None):
        """
        Ініціалізація таблиці констант.

        :param default_constants: Словник, що представляє початкові значення таблиці констант.
                                  Якщо не вказано, використовується стандартна таблиця.
        """
        if default_constants is None:
            # Якщо початкові значення не надані, використовуємо стандартну таблицю констант.
            default_constants = {
                0: 1, 1: 0, 2: 3, 3: 2,
                4: 5, 5: 4, 6: 7, 7: 6,
                8: 9, 9: 8, 10: 11, 11: 10,
                12: 13, 13: 12, 14: 15, 15: 14
            }
        self.constants = default_constants.copy()  # Копія для редагування.
        # Генеруємо зворотну таблицю для констант, необхідну для дешифрування.
        self.inverse_constants = self.generate_inverse_constants()

    def generate_inverse_constants(self):
        """Генерує зворотну таблицю для констант."""
        return {v: k for k, v in self.constants.items()}

    def substitution(self, input_byte: int) -> int:
        """Пряме перетворення для таблиці констант."""
        # Витягаємо ліву та праву тетради з вхідного байта
        left_nibble = (input_byte >> 4) & 0xF  # Витягуємо ліву тетраду
        right_nibble = input_byte & 0xF         # Витягуємо праву тетраду
        # Повертаємо новий байт, який утворюється шляхом заміни значень з таблиці констант
        return (self.constants[left_nibble] << 4) | self.constants[right_nibble]

    def inverse_substitution(self, input_byte: int) -> int:
        """Зворотне перетворення для таблиці констант."""
        # Витягаємо ліву та праву тетради з вхідного байта
        left_nibble = (input_byte >> 4) & 0xF  # Витягуємо ліву тетраду
        right_nibble = input_byte & 0xF        # Витягуємо праву тетраду
        # Повертаємо новий байт, який утворюється шляхом зворотної заміни значень з таблиці констант
        return (self.inverse_constants[left_nibble] << 4) | self.inverse_constants[right_nibble]

    def edit(self):
        """Редагування таблиці констант користувачем."""
        print("\nРедагування таблиці констант:")
        new_values = []  # Список для нових значень
        for i in range(16):  # Проходимо через всі 16 можливих значень
            while True:
                new_value = input(f"Введіть нове значення для констант[{i}] (поточне: {self.constants[i]}): ")
                if new_value.isdigit():
                    new_value = int(new_value)
                    # Перевіряємо, чи нове значення унікальне та в межах від 0 до 15
                    if 0 <= new_value < 16 and new_value not in new_values:
                        new_values.append(new_value)  # Додаємо нове значення до списку
                        break
                    else:
                        print("Значення має бути унікальним та в межах від 0 до 15.")
                else:
                    print("Невірний формат введення. Значення має бути числом.")
        # Оновлюємо таблицю констант з новими значеннями
        self.constants = {i: new_values[i] for i in range(16)}
        self.inverse_constants = self.generate_inverse_constants()  # Оновлюємо зворотну таблицю

    def generate_random_constants(self):
        """Генерує випадкову таблицю констант з унікальними значеннями від 0 до 15."""
        values = list(range(16))  # Створюємо список можливих значень
        random.shuffle(values)  # Перемішуємо їх випадковим чином
        # Оновлюємо таблицю констант новими значеннями
        self.constants = {i: values[i] for i in range(16)}
        self.inverse_constants = self.generate_inverse_constants()  # Оновлюємо зворотну таблицю
        print("Таблиця констант була успішно згенерована випадковим чином.")

    def display(self):
        """Виводить поточну таблицю констант на екран."""
        print("\nТаблиця констант:")
        for k, v in self.constants.items():
            # Виводимо значення у форматі ключ: значення
            print(f"{k}: {v}")

    def save_constants(self, path: str):
        """Зберігає таблицю констант у файл JSON."""
        if not path.endswith('.json'):
            print("Шлях повинен закінчуватись на '.json'.")
            return

        data = {"constants": self.constants}  # Створюємо словник для збереження
        with open(path, "w") as f:
            json.dump(data, f)  # Записуємо таблицю констант у файл
        print(f"Таблиця констант була успішно збережена в файл {path}.")

    def load_constants(self, path: str):
        """Завантажує таблицю констант з файлу JSON."""
        if not path.endswith('.json'):
            print("Шлях повинен закінчуватись на '.json'.")
            return

        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
                # Конвертуємо значення на int
                self.constants = {int(k): int(v) for k, v in data.get("constants", {}).items()}
                self.inverse_constants = self.generate_inverse_constants()  # Оновлюємо зворотну таблицю
                print(f"Таблиця констант була успішно завантажена з файлу {path}.")
        else:
            print(f"Файл {path} не знайдено.")  # Повідомлення про відсутність файлу

class PermutationFormula:
    """Клас для операцій з формулою перестановки."""

    def __init__(self, default_permutation=None):
        """
        Ініціалізація формули перестановки.

        :param default_permutation: Список, що представляє початкові значення формули перестановки.
                                    Якщо не вказано, використовується стандартна формула.
        """
        if default_permutation is None:
            # Якщо початкові значення не надані, використовуємо стандартну формулу перестановки.
            default_permutation = [1, 5, 2, 0, 3, 7, 4, 6]
        self.permutation_values = default_permutation.copy()  # Копія для редагування

    def permutation(self, input_byte: int) -> int:
        """Пряме перетворення для формули перестановки."""
        output_byte = 0  # Ініціалізуємо вихідний байт
        for i in range(8):  # Проходимо через всі 8 біт
            # Виконуємо перестановку згідно формули
            output_byte |= ((input_byte >> i) & 1) << self.permutation_values[i]
        return output_byte

    def inverse_permutation(self, input_byte: int) -> int:
        """Зворотне перетворення для формули перестановки."""
        inverse_permutation = [self.permutation_values.index(i) for i in range(8)]  # Зворотна перестановка
        output_byte = 0  # Ініціалізуємо вихідний байт
        for i in range(8):  # Проходимо через всі 8 біт
            # Виконуємо зворотну перестановку
            output_byte |= ((input_byte >> i) & 1) << inverse_permutation[i]
        return output_byte

    def edit(self):
        """Редагування формули перестановки користувачем."""
        print("\nРедагування формули перестановки:")
        new_values = []  # Список для нових значень
        for i in range(8):  # Проходимо через всі 8 можливих значень
            while True:
                new_value = input(f"Введіть нове значення для перестановки[{i}] (поточне: {self.permutation_values[i]}): ")
                if new_value.isdigit():
                    new_value = int(new_value)
                    # Перевіряємо, чи нове значення унікальне та в межах від 0 до 7
                    if 0 <= new_value < 8 and new_value not in new_values:
                        new_values.append(new_value)  # Додаємо нове значення до списку
                        break
                    else:
                        print("Значення повинно бути унікальним і в межах від 0 до 7.")
                else:
                    print("Невірний формат введення.")
        # Оновлюємо формулу перестановки з новими значеннями
        self.permutation_values = new_values

    def generate_random_permutation(self):
        """Генерує випадкову формулу перестановки з унікальними значеннями від 0 до 7."""
        self.permutation_values = random.sample(range(8), 8)  # Генеруємо випадкову перестановку
        print("Формула перестановки була успішно згенерована випадковим чином.")

    def display(self):
        """Виводить поточну формулу перестановки на екран."""
        print("\nФормула перестановки:")
        for index, value in enumerate(self.permutation_values):
            # Виводимо значення формули перестановки
            print(f"{index}: {value}")

    def save_permutation(self, path: str):
        """Зберігає формулу перестановки у файл JSON."""
        if not path.endswith('.json'):
            print("Шлях повинен закінчуватись на '.json'.")
            return

        data = {"permutation": self.permutation_values}  # Створюємо словник для збереження
        with open(path, "w") as f:
            json.dump(data, f)  # Записуємо формулу перестановки у файл
        print(f"Формула перестановки була успішно збережена в файл {path}.")

    def load_permutation(self, path: str):
        """Завантажує формулу перестановки з файлу JSON."""
        if not path.endswith('.json'):
            print("Шлях повинен закінчуватись на '.json'.")
            return

        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
                # Оновлюємо формулу перестановки новими значеннями
                self.permutation_values = data.get("permutation", self.permutation_values)
                print(f"Формула перестановки була успішно завантажена з файлу {path}.")
        else:
            print(f"Файл {path} не знайдено.")  # Повідомлення про відсутність файлу

class SPBlockCipher:
    """Основний клас, який об'єднує S-блок та P-блок для шифрування та дешифрування."""

    def __init__(self):
        """Ініціалізація класу SPBlockCipher, створюючи екземпляри ConstantTable та PermutationFormula."""
        self.constant_table = ConstantTable()  # Створюємо екземпляр таблиці констант
        self.permutation_formula = PermutationFormula()  # Створюємо екземпляр формули перестановки

    def constant_substitution(self, input_byte: int) -> int:
        """Пряме перетворення для таблиці констант."""
        return self.constant_table.substitution(input_byte)  # Викликаємо підстановку в таблиці констант

    def inverse_constant_substitution(self, input_byte: int) -> int:
        """Зворотне перетворення для таблиці констант."""
        return self.constant_table.inverse_substitution(input_byte)  # Викликаємо зворотну підстановку в таблиці констант

    def permutation(self, input_byte: int) -> int:
        """Пряме перетворення для формули перестановки."""
        return self.permutation_formula.permutation(input_byte)  # Викликаємо перестановку у формулі перестановки

    def inverse_permutation(self, input_byte: int) -> int:
        """Зворотне перетворення для формули перестановки."""
        return self.permutation_formula.inverse_permutation(input_byte)  # Викликаємо зворотну перестановку у формулі перестановки

    def reset_constant_table(self):
        """Скидає таблицю констант до початкових значень."""
        self.constant_table = ConstantTable()  # Створюємо новий екземпляр таблиці констант з початковими значеннями

    def reset_permutation_formula(self):
        """Скидає формулу перестановки до початкових значень."""
        self.permutation_formula = PermutationFormula()  # Створюємо новий екземпляр формули перестановки з початковими значеннями

    def display_constant_table(self):
        """Виводить поточну таблицю констант на екран."""
        self.constant_table.display()  # Викликаємо метод для відображення таблиці констант

    def display_permutation_formula(self):
        """Виводить поточну формулу перестановки на екран."""
        self.permutation_formula.display()  # Викликаємо метод для відображення формули перестановки

    def edit_constant_table(self):
        """Редагування таблиці констант."""
        self.constant_table.edit()  # Викликаємо метод редагування в таблиці констант

    def edit_permutation_formula(self):
        """Редагування формули перестановки."""
        self.permutation_formula.edit()  # Викликаємо метод редагування в формулі перестановки

    def save_constant_table(self, path: str):
        """Зберігає таблицю констант у файл."""
        self.constant_table.save_constants(path)  # Викликаємо метод для збереження таблиці констант

    def load_constant_table(self, path: str):
        """Завантажує таблицю констант з файлу."""
        self.constant_table.load_constants(path)  # Викликаємо метод для завантаження таблиці констант

    def save_permutation_formula(self, path: str):
        """Зберігає формулу перестановки у файл."""
        self.permutation_formula.save_permutation(path)  # Викликаємо метод для збереження формули перестановки

    def load_permutation_formula(self, path: str):
        """Завантажує формулу перестановки з файлу."""
        self.permutation_formula.load_permutation(path)  # Викликаємо метод для завантаження формули перестановки

def get_input_byte():
    """
    Отримує введення від користувача в одному з форматів: двійковому, десятковому або шістнадцятковому.
    Перевіряє формат та коректність введення.
    """
    while True:
        user_input = input("Введіть 8-бітне число (двійкове, десяткове або шістнадцяткове): ")
        
        # Перевірка на двійковий формат (8 біт)
        if all(bit in '01' for bit in user_input) and len(user_input) == 8:
            return int(user_input, 2)  # Повертаємо значення в десятковому форматі
        
        # Перевірка на десятковий формат
        try:
            value = int(user_input)
            if 0 <= value <= 255:
                return value  # Повертаємо десяткове значення
        except ValueError:
            pass  # Неправильний формат, продовжуємо перевіряти
        
        # Перевірка на шістнадцятковий формат
        try:
            value = int(user_input, 16)
            if 0 <= value <= 255:
                return value  # Повертаємо десяткове значення
        except ValueError:
            pass  # Неправильний формат

        # Повідомлення про помилку при неправильному введенні
        print("Неправильний формат! Введіть 8-бітне число (від 0 до 255 в десятковому форматі, 8 біт у двійковому форматі або шістнадцятковому).")

def print_in_different_bases(value):
    """Виводить значення в різних системах числення."""
    print(f"Двійкове: {bin(value)[2:].zfill(8)}")   # Двійковий формат
    print(f"Десяткове: {value}")                    # Десятковий формат
    print(f"Шістнадцяткове: {hex(value)[2:].upper()}")  # Шістнадцятковий формат

def test_s_block(cipher):
    """
    Тестує S-блок, перевіряючи, чи коректно відбувається шифрування та дешифрування.
    """
    print("\nПочинаємо тестування S-блоку:")
    all_passed = True  # Змінна для відстеження результату тестування
    
    for input_value in range(16):  # Тестуємо всі значення від 0 до 15
        # Шифруємо значення
        substituted_value = cipher.constant_substitution(input_value)
        # Дешифруємо значення
        reversed_value = cipher.inverse_constant_substitution(substituted_value)

        # Виводимо результати тесту
        print(f"Тест для вхідного значення {input_value}: зашифроване {substituted_value}, дешифроване {reversed_value}.")

        # Перевірка, чи результати повертають до початкового значення
        if reversed_value != input_value:
            print(f"Тест не пройшов для вхідного значення {input_value}: зашифроване {substituted_value}, дешифроване {reversed_value}.")
            all_passed = False

    if all_passed:
        print("Тестування S-блоку пройшло успішно! Всі значення були правильно зашифровані та дешифровані.")
    else:
        print("Деякі тести не пройшли. Перевірте алгоритм S-блоку.")

def test_p_block(cipher):
    """
    Тестує P-блок, перевіряючи, чи коректно відбувається шифрування та дешифрування.
    """
    print("\nПочинаємо тестування P-блоку:")
    all_passed = True  # Змінна для відстеження результату тестування
    
    for input_value in range(256):  # Тестуємо всі значення від 0 до 255
        # Шифруємо значення
        permuted_value = cipher.permutation(input_value)
        # Дешифруємо значення
        reversed_value = cipher.inverse_permutation(permuted_value)

        # Виводимо результати тесту
        print(f"Тест для вхідного значення {input_value}: зашифроване {permuted_value}, дешифроване {reversed_value}.")

        # Перевірка, чи результати повертають до початкового значення
        if reversed_value != input_value:
            print(f"Тест не пройшов для вхідного значення {input_value}: зашифроване {permuted_value}, дешифроване {reversed_value}.")
            all_passed = False

    if all_passed:
        print("Тестування P-блоку пройшло успішно! Всі значення були правильно зашифровані та дешифровані.")
    else:
        print("Деякі тести не пройшли. Перевірте алгоритм P-блоку.")

def test_both_blocks(cipher):
    """
    Тестує S-блок та P-блок, перевіряючи, чи коректно відбувається
    шифрування та дешифрування.
    """
    print("\nПочинаємо тестування обох блоків:")
    all_passed = True  # Змінна для відстеження результату тестування
    
    for input_value in range(256):  # Тестуємо всі значення від 0 до 255
        # Шифруємо з обома блоками
        encrypted = cipher.permutation(cipher.constant_substitution(input_value))  # Застосовуємо S-блок, а потім P-блок

        # Дешифруємо з обома блоками
        decrypted = cipher.inverse_constant_substitution(cipher.inverse_permutation(encrypted))  # Зворотній порядок

        # Виводимо результати тесту
        print(f"Тест для вхідного значення {input_value}: зашифроване {encrypted}, дешифроване {decrypted}.")

        # Перевірка, чи результати повертають до початкового значення
        if decrypted != input_value:
            print(f"Тест не пройшов для вхідного значення {input_value}: зашифроване {encrypted}, дешифроване {decrypted}.")
            all_passed = False

    if all_passed:
        print("Тестування обох блоків пройшло успішно! Всі значення були правильно зашифровані та дешифровані.")
    else:
        print("Деякі тести не пройшли. Перевірте алгоритми S-блоку та P-блоку.")

def main():
    """Головна функція програми, яка забезпечує взаємодію з користувачем."""
    cipher = SPBlockCipher()  # Ініціалізуємо екземпляр класу один раз

    while True:
        print("\nМеню:")  # Основне меню
        print("1 - Робота з таблицею констант")
        print("2 - Робота з формулою перестановки")
        print("3 - Шифрування та дешифрування")
        print("4 - Тестування")
        print("0 - Вихід")
        choice = input("Оберіть дію: ")  # Отримуємо вибір користувача

        if choice == '1':
            # Меню для роботи з таблицею констант
            while True:
                print("\nМеню таблиці констант:")
                print("1 - Перегляд таблиці констант")
                print("2 - Редагування таблиці констант")
                print("3 - Генерувати випадкову таблицю констант")
                print("4 - Скинути таблицю констант до початкових значень")
                print("5 - Зберегти таблицю констант у файл")
                print("6 - Завантажити таблицю констант з файлу")
                print("0 - Назад")
                s_choice = input("Оберіть дію: ")

                if s_choice == '1':
                    cipher.display_constant_table()  # Відображення таблиці констант
                elif s_choice == '2':
                    cipher.edit_constant_table()  # Редагування таблиці констант
                elif s_choice == '3':
                    cipher.constant_table.generate_random_constants()  # Генерація випадкової таблиці констант
                elif s_choice == '4':
                    cipher.reset_constant_table()  # Скидання до початкових значень
                elif s_choice == '5':
                    path = input("Введіть шлях для збереження таблиці констант (з ім'ям файлу і розширенням .json): ")
                    cipher.save_constant_table(path)  # Зберігання таблиці констант у файл
                elif s_choice == '6':
                    path = input("Введіть шлях для завантаження таблиці констант (з ім'ям файлу і розширенням .json): ")
                    cipher.load_constant_table(path)  # Завантаження таблиці констант з файлу
                elif s_choice == '0':
                    break  # Повертаємось в основне меню
                else:
                    print("Невірний вибір!")  # Помилка вибору

        elif choice == '2':
            # Меню для роботи з формулою перестановки
            while True:
                print("\nМеню формули перестановки:")
                print("1 - Перегляд формули перестановки")
                print("2 - Редагування формули перестановки")
                print("3 - Генерувати випадкову формулу перестановки")
                print("4 - Скинути формулу перестановки до початкових значень")
                print("5 - Зберегти формулу перестановки у файл")
                print("6 - Завантажити формулу перестановки з файлу")
                print("0 - Назад")
                p_choice = input("Оберіть дію: ")

                if p_choice == '1':
                    cipher.display_permutation_formula()  # Відображення формули перестановки
                elif p_choice == '2':
                    cipher.edit_permutation_formula()  # Редагування формули перестановки
                elif p_choice == '3':
                    cipher.permutation_formula.generate_random_permutation()  # Генерація випадкової формули перестановки
                elif p_choice == '4':
                    cipher.reset_permutation_formula()  # Скидання до початкових значень
                elif p_choice == '5':
                    path = input("Введіть шлях для збереження формули перестановки (з ім'ям файлу і розширенням .json): ")
                    cipher.save_permutation_formula(path)  # Зберігання формули перестановки у файл
                elif p_choice == '6':
                    path = input("Введіть шлях для завантаження формули перестановки (з ім'ям файлу і розширенням .json): ")
                    cipher.load_permutation_formula(path)  # Завантаження формули перестановки з файлу
                elif p_choice == '0':
                    break  # Повертаємось в основне меню
                else:
                    print("Невірний вибір!")  # Помилка вибору

        elif choice == '3':
            # Окреме меню для шифрування та дешифрування
            while True:
                input_byte = get_input_byte()  # Отримати байт на основі введеного формату
                
                print("\nОберіть дію:")  # Меню шифрування/дешифрування
                print("1 - Шифрування за таблицею констант")
                print("2 - Дешифрування за таблицею констант")
                print("3 - Шифрування за формулою перестановки")
                print("4 - Дешифрування за формулою перестановки")
                print("5 - Шифрування обома блоками")
                print("6 - Дешифрування обома блоками")
                print("0 - Назад")
                action_choice = input("Ваш вибір: ")

                if action_choice == '1':
                    # Шифруємо лише за таблицею констант
                    s_substituted = cipher.constant_substitution(input_byte)  # Застосування таблиці констант
                    print("Результат шифрування за таблицею констант (в двійковому форматі):")
                    print_in_different_bases(s_substituted)  # Виводимо в різних системах числення

                elif action_choice == '2':
                    # Дешифруємо лише за таблицею констант
                    s_reversed = cipher.inverse_constant_substitution(input_byte)  # Дешифрування таблицею констант
                    print("Результат дешифрування за таблицею констант (в двійковому форматі):")
                    print_in_different_bases(s_reversed)  # Виводимо в різних системах числення

                elif action_choice == '3':
                    # Шифруємо лише за формулою перестановки
                    p_permuted = cipher.permutation(input_byte)  # Застосування формули перестановки
                    print("Результат шифрування за формулою перестановки (в двійковому форматі):")
                    print_in_different_bases(p_permuted)  # Виводимо в різних системах числення

                elif action_choice == '4':
                    # Дешифруємо лише за формулою перестановки
                    p_reversed = cipher.inverse_permutation(input_byte)  # Дешифрування формулою перестановки
                    print("Результат дешифрування за формулою перестановки (в двійковому форматі):")
                    print_in_different_bases(p_reversed)  # Виводимо в різних системах числення

                elif action_choice == '5':
                    # Шифруємо з обома блоками
                    s_substituted = cipher.constant_substitution(input_byte)  # Спочатку шифруємо таблицею констант
                    p_permuted = cipher.permutation(s_substituted)  # Потім шифруємо формулою перестановки
                    print("Результат шифрування за таблицею констант, потім формулою перестановки (в двійковому форматі):")
                    print_in_different_bases(p_permuted)  # Виводимо в різних системах числення

                elif action_choice == '6':
                    # Дешифруємо з обома блоками
                    p_reversed = cipher.inverse_permutation(input_byte)  # Дешифрування формулою перестановки
                    s_reversed = cipher.inverse_constant_substitution(p_reversed)  # Потім дешифруємо таблицею констант
                    print("Результат дешифрування обома блоками (в двійковому форматі):")
                    print_in_different_bases(s_reversed)  # Виводимо в різних системах числення

                elif action_choice == '0':
                    break  # Повертаємось в основне меню
                else:
                    print("Невірний вибір!")  # Помилка вибору

        elif choice == '4':
            # Меню для тестування
            while True:
                print("\nМеню тестування:")
                print("1 - Тестування S-блоку")
                print("2 - Тестування P-блоку")
                print("3 - Тестування обох блоків")
                print("0 - Назад")
                test_choice = input("Оберіть дію: ")

                if test_choice == '1':
                    test_s_block(cipher)  # Виконуємо тестування S-блоку
                elif test_choice == '2':
                    test_p_block(cipher)  # Виконуємо тестування P-блоку
                elif test_choice == '3':
                    test_both_blocks(cipher)  # Виконуємо тестування обох блоків
                elif test_choice == '0':
                    break  # Повертаємось в основне меню
                else:
                    print("Невірний вибір!")  # Помилка вибору

        elif choice == '0':
            print("Вихід з програми.")  # Завершення програми
            break
        
        else:
            print("Невірний вибір!")  # Помилка вибору

if __name__ == "__main__":
    main()  # Виклик головної функції при запуску програми
