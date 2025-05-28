import re

digits = {'0': 'ноль', '1': 'один', '2': 'два', '3': 'три', '4': 'четыре', '5': 'пять', '6': 'шесть', '7': 'семь', '8': 'восемь', '9': 'девять'}

def main(file_path):
    numbers = []
    with open(file_path, 'r') as file:
        buffer = file.read()

        pattern = r'\b([0-3]?[0-7]?[0-7]?0[0246])\b'
        lexemes = re.findall(pattern, buffer)

        for oct_num in lexemes:
            trunc = oct_num[:-2] if len(oct_num) > 2 else '0'
            numbers.append(int(trunc, 8))
            print("Обрезанное число:", trunc)

    if numbers:
        avg = (min(numbers) + max(numbers)) // 2
        avg_words = [digits[d] for d in str(avg)]
        print("\nСреднее значение:", ' '.join(avg_words))
    else:
        print("\nПодходящие числа не найдены.")

main("1lab.txt")
