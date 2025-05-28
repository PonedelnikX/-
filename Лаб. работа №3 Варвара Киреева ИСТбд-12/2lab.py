def read_matrix_from_file(file_path):
    matrix = []
    with open(file_path, 'r') as file:
        for line in file:
            row = list(map(int, line.strip().split()))
            if row:
                matrix.append(row)
    return matrix

def print_matrix(matrix, title="Matrix"):
    print(f"{title}:")
    for row in matrix:
        print(" ".join(f"{num:4}" for num in row))
    print()

def count_zeros_in_area(matrix, area, N):
    count = 0
    for i in range(N):
        for j in range(N):
            # Область 1: верхний левый треугольник (включая главную диагональ и выше, но выше побочной)
            if area == 1 and j <= i and i + j < N - 1:
                if matrix[i][j] == 0:
                    count += 1
            # Область 3: нижний левый треугольник (ниже главной диагонали и ниже побочной)
            elif area == 3 and j >= i and i + j >= N:
                if matrix[i][j] == 0:
                    count += 1
    return count

def swap_areas_1_2_symmetrically(F, N):
    # Меняем области 1 и 2 по главной диагонали
    for i in range(N):
        for j in range(i):
            if i + j < N - 1:
                F[i][j], F[j][i] = F[j][i], F[i][j]

def swap_areas_1_2_non_symmetrically(F, N):
    # Меняем области 1 и 2 по побочной диагонали
    for i in range(N):
        for j in range(i):
            if i + j < N - 1:
                ni, nj = N - 1 - j, N - 1 - i
                if ni > nj and ni + nj < N - 1:
                    F[i][j], F[ni][nj] = F[ni][nj], F[i][j]

def matrix_transpose(matrix, N):
    return [[matrix[j][i] for j in range(N)] for i in range(N)]

def matrix_multiply(A, B, N):
    result = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            for k in range(N):
                result[i][j] += A[i][k] * B[k][j]
    return result

def scalar_multiply(matrix, scalar, N):
    return [[matrix[i][j] * scalar for j in range(N)] for i in range(N)]

def matrix_subtract(A, B, N):
    return [[A[i][j] - B[i][j] for j in range(N)] for i in range(N)]

def main():
    file_path = "1lab.txt"
    A = read_matrix_from_file(file_path)
    N = len(A)
    if any(len(row) != N for row in A):
        print("Ошибка: матрица не квадратная или некорректный файл!")
        return

    K = int(input("Введите число K: "))

    print_matrix(A, "Исходная матрица A")

    F = [row[:] for row in A]  # Глубокая копия

    zeros_area1 = count_zeros_in_area(F, 1, N)
    zeros_area3 = count_zeros_in_area(F, 3, N)
    print(f"Количество нулей в области 1 (треугольной): {zeros_area1}")
    print(f"Количество нулей в области 3 (треугольной): {zeros_area3}")

    if zeros_area1 > zeros_area3:
        print("Меняем области 1 и 2 симметрично (главная диагональ)")
        swap_areas_1_2_symmetrically(F, N)
    else:
        print("Меняем области 1 и 2 несимметрично (побочная диагональ)")
        swap_areas_1_2_non_symmetrically(F, N)

    print_matrix(F, "Матрица F после преобразований")

    AT = matrix_transpose(A, N)
    print_matrix(AT, "Транспонированная матрица A^T")

    AAT = matrix_multiply(A, AT, N)
    print_matrix(AAT, "Результат умножения A*A^T")

    KF = scalar_multiply(F, K, N)
    print_matrix(KF, "Результат умножения K*F")

    result = matrix_subtract(AAT, KF, N)
    print_matrix(result, "Итоговый результат A*A^T - K*F")

if __name__ == "__main__":
    main()
