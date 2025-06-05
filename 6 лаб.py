import timeit
import pandas as pd
import matplotlib.pyplot as plt
from math import factorial  


def rec_F(n):
    if n == 1:
        return 1
    
    sign = -1 if (n % 2 == 1) else 1
    return sign * (3 * rec_F(n - 1) - 3 * rec_G(n - 1))

def rec_G(n):
    if n == 1:
        return 1

    return (rec_F(n - 1) + 2 * rec_G(n - 1)) / factorial(2 * n)

def iter_F(n):
    F = [0] * (n + 1)
    G = [0] * (n + 1)
    F[1] = 1
    G[1] = 1


    accumulated_fact = factorial(2)  # = 2

    for k in range(2, n + 1):

        accumulated_fact *= (2 * k - 1) * (2 * k)


        sign = -1 if (k % 2 == 1) else 1

        F[k] = sign * (3 * F[k - 1] - 3 * G[k - 1])
        G[k] = (F[k - 1] + 2 * G[k - 1]) / accumulated_fact

    return F[n]

def iter_G(n):
    F = [0] * (n + 1)
    G = [0] * (n + 1)
    F[1] = 1
    G[1] = 1

    accumulated_fact = factorial(2)

    for k in range(2, n + 1):
        accumulated_fact *= (2 * k - 1) * (2 * k)
        sign = -1 if (k % 2 == 1) else 1

        F[k] = sign * (3 * F[k - 1] - 3 * G[k - 1])
        G[k] = (F[k - 1] + 2 * G[k - 1]) / accumulated_fact

    return G[n]

if __name__ == '__main__':
    ns = list(range(1, 18))
    results = []

    for n in ns:

        t_rec = timeit.timeit(lambda: rec_F(n), number=5)
        t_it  = timeit.timeit(lambda: iter_F(n), number=5)

        results.append((n, rec_F(n), iter_F(n), t_rec, t_it))

    df = pd.DataFrame(
        results,
        columns=['n', 'Rec_F(n)', 'Iter_F(n)', 'Rec_time (s)', 'Iter_time (s)']
    )
    print(df.to_string(index=False))

    plt.figure(figsize=(10, 6))
    plt.plot(df['n'], df['Rec_time (s)'], 'o--', label='Рекурсия F(n)')
    plt.plot(df['n'], df['Iter_time (s)'], 's-', label='Итерация F(n)')
    plt.xlabel('n')
    plt.ylabel('Время выполнения (сек)')
    plt.title('Сравнение времени вычисления F(n): рекурсия vs итерация')
    plt.legend()
    plt.grid(True)
    plt.show()
