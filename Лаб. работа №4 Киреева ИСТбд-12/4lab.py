'''
7.Формируется матрица F следующим образом: скопировать в нее А и если в С количество нулевых элементов в нечетных столбцах,
чем количество нулевых  элементов в четных столбцах,
то поменять местами С и В симметрично, иначе С и Е поменять местами несимметрично.
При этом матрица А не меняется. После чего если определитель матрицы А больше суммы диагональных элементов матрицы F,
то вычисляется выражение: A*AT – K * FТ, иначе вычисляется выражение (AТ +G-F-1)*K, где G-нижняя треугольная матрица,
полученная из А. Выводятся по мере формирования А, F и все матричные операции последовательно.
'''

import numpy as np
import matplotlib.pyplot as plt

def get_matrix(N):
    while True:
        try:
            A = np.loadtxt("matrix_data.txt", dtype=int)
            if A.shape != (N, N):
                print("Размер матрицы не совпадает с N!")
                return None
            if np.linalg.det(A) == 0:
                print("Матрица вырождена! Загрузите другую матрицу.")
                return None
            return A
        except Exception as e:
            print("Ошибка чтения файла:", e)
            return None

def count_zeros_cols(A, cols):
    return np.sum(A[:, cols] == 0)

def swap_quarters_sym(F, h):
    for i in range(h):
        for j in range(h):
            F[i, j+h], F[j+h, i+h] = F[j+h, i+h], F[i, j+h]

def swap_quarters_nonsym(F, h):
    temp = F[:h, h:].copy()
    F[:h, h:] = F[h:, h:]
    F[h:, h:] = temp

def process_matrix(A):
    N = A.shape[0]
    h = N // 2
    F = A.copy()

    C = A[h:, h:]

    odd_cols = [j for j in range(C.shape[1]) if j % 2 == 1]
    even_cols = [j for j in range(C.shape[1]) if j % 2 == 0]
    zeros_odd = count_zeros_cols(C, odd_cols)
    zeros_even = count_zeros_cols(C, even_cols)

    print(f"\nНулей в нечётных столбцах C: {zeros_odd}")
    print(f"Нулей в чётных столбцах C: {zeros_even}")

    if zeros_odd > zeros_even:
        print("Меняем четверти B и C симметрично (главная диагональ)")
        swap_quarters_sym(F, h)
    else:
        print("Меняем четверти B и C несимметрично")
        swap_quarters_nonsym(F, h)
    return F

def plot_graphs(F):
    plt.figure(figsize=(15, 4))
    plt.subplot(1, 3, 1)
    plt.imshow(F, cmap='coolwarm')
    plt.title("Тепловая карта F")
    plt.colorbar()
    plt.subplot(1, 3, 2)
    plt.plot(F.mean(axis=0), '-o')
    plt.title("Среднее по столбцам F")
    plt.subplot(1, 3, 3)
    plt.hist(F.flatten(), bins=20, color='skyblue')
    plt.title("Гистограмма элементов F")
    plt.tight_layout()
    plt.show()

def main():
    K = int(input("Введите K: "))
    N = int(input("Введите N (чётное): "))
    if N % 2 != 0:
        raise ValueError("N должно быть чётным!")
    A = get_matrix(N)
    if A is None:
        print("Не удалось загрузить матрицу. Программа завершена.")
        return
    print("\nМатрица A:\n", A)
    F = process_matrix(A)
    print("\nМатрица F:\n", F)
    AT = A.T
    print("\nA^T:\n", AT)
    FT = F.T
    print("\nF^T:\n", FT)
    G = np.tril(A)
    print("\nG (нижнетреугольная A):\n", G)

    det_A = np.linalg.det(A)
    trace_F = np.trace(F)
    trace_F_rev = np.trace(np.fliplr(F))
    print(f"\ndet(A) = {det_A:.2f}")
    print(f"Сумма диагоналей F (главная + побочная): {trace_F + trace_F_rev:.2f}")

    if det_A > (trace_F + trace_F_rev):
        print("\ndet(A) больше суммы диагоналей F")
        left = AT @ F
        print("\nA^T * F:\n", left)
        right = K * FT
        print(f"\nK * F^T (K={K}):\n", right)
        result = left - right
        print("\nРезультат (A^T * F - K * F^T):\n", result)
    else:
        print("\ndet(A) не больше суммы диагоналей F")
        left = AT + G - F
        print("\nA^T + G - F:\n", left)
        result = left * K
        print(f"\nРезультат (A^T + G - F) * K (K={K}):\n", result)

    plot_graphs(F)

if __name__ == "__main__":
    main()

