import timeit

# Алгоритм Кнута-Морріса-Пратта

def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(text, pattern):
    M = len(pattern)
    N = len(text)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено

# Алгоритм Боєра-Мура
    
def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
# Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
# Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
# Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0 # Ініціалізуємо початковий індекс для основного тексту

# Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1 # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1 # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1


# Алгоритм Рабіна-Карпа 
def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(text, pattern):
    # Довжини основного рядка та підрядка пошуку
    pattern_length = len(pattern)
    text_length = len(text)
    
    # Базове число для хешування та модуль
    base = 256 
    modulus = 101  
    
    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    pattern_hash = polynomial_hash(pattern, base, modulus)
    current_slice_hash = polynomial_hash(text[:pattern_length], base, modulus)
    
    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, pattern_length - 1) % modulus
    
    # Проходимо крізь основний рядок
    for i in range(text_length - pattern_length + 1):
        if pattern_hash == current_slice_hash:
            if text[i:i+pattern_length] == pattern:
                return i

        if i < text_length - pattern_length:
            current_slice_hash = (current_slice_hash - ord(text[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(text[i + pattern_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

# Функція для вимірювання часу
def measure_time(func, *args):
    start_time = timeit.default_timer()
    result = func(*args)
    end_time = timeit.default_timer()
    time = end_time - start_time
    return result, time

# Відкриття файлів
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        return file.read()

algorithms = [kmp_search, boyer_moore_search, rabin_karp_search]

# Підготовка файлів 
text_1 = read_file('data/article_1.txt')
text_2 = read_file('data/article_2.txt')

# Вибір шаблонів
pattern_1 = 'структура даних, у якій пошук елементу здійснюється на основі його ключа'
pattern_2 = 'щось чого не існує'
pattern_3 = 'Інтерполяційний пошук використовується для пошуку елементів у відсортованому масиві'


# Перевірка вимірювання часу 
for algorithm in algorithms:
    name = algorithm.__name__
    print(f'{name} шукає {pattern_1} у article_1: {measure_time(algorithm, text_1, pattern_1)}')
    print(f'{name} шукає {pattern_2} у article_1: {measure_time(algorithm, text_1, pattern_2)}')
    print(f'{name} шукає {pattern_3} у article_1: {measure_time(algorithm, text_1, pattern_3)}')
    print(f'{name} шукає {pattern_1} у article_2: {measure_time(algorithm, text_2, pattern_1)}')
    print(f'{name} шукає {pattern_2} у article_2: {measure_time(algorithm, text_2, pattern_2)}')
    print(f'{name} шукає {pattern_3} у article_2: {measure_time(algorithm, text_2, pattern_3)}')