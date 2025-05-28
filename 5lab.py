import timeit
from itertools import combinations

def algorithmic_method(players, team_size):
    result = []
    team = []

    def backtrack(start):
        if len(team) == team_size:
            result.append(team.copy())
            return
        for i in range(start, len(players)):
            team.append(players[i])
            backtrack(i + 1)
            team.pop()

    backtrack(0)
    return result


def python_method(players, team_size):
    return list(combinations(players, team_size))

if __name__ == "__main__":
    professionals = [f'P{i}' for i in range(1, 6)]
    amateurs = [f'A{i}' for i in range(1, 6)]
    players = professionals + amateurs
    team_size = 4


    t_alg = timeit.timeit(lambda: algorithmic_method(players, team_size), number=2)
    alg_res = algorithmic_method(players, team_size)


    t_py = timeit.timeit(lambda: python_method(players, team_size), number=2)
    py_res = python_method(players, team_size)

    print(f"Алгоритмический метод: найдено {len(alg_res)} команд, время {t_alg:.6f} сек")
    print("Первые 5 команд:")
    for team in alg_res[:5]:
        print(team)

    print(f"\nМетод с использованием itertools: найдено {len(py_res)} команд, время {t_py:.6f} сек")
    print("Первые 5 команд:")
    for team in py_res[:5]:
        print(team)
