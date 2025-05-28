
def is_valid_number(word):
    return all(ch in '01234567' for ch in word) and len(word) > 1 and '0' in word

def convert_to_decimal(oct_number):
    return int(oct_number, 8)

def process_file(file_path):
    numbers = []
    digits = {  '0': 'ноль','1': 'один','2': 'два', '3': 'три', '4': 'четыре', '5': 'пять', '6': 'шесть', '7': 'семь', '8': 'восемь', '9': 'девять'}
    with open(file_path, 'r') as file:
        for line in file:
            for word in line.split():
                if is_valid_number(word):
                    n = convert_to_decimal(word)
                    if n <= 2047 and n % 2 == 0:
                        truncated_n = convert_to_decimal(word[:-2]) if len(word) > 2 else 0
                        numbers.append(truncated_n)
                        print( word[:-2])
    if numbers:
        avg = (min(numbers) + max(numbers)) // 2
        avg_words = [digits[digit] for digit in str(avg)]
        print("Среднее значение:", ' '.join(avg_words))
    else:
        print("Подходящие числа не найдены.")

process_file("1lab.txt")
