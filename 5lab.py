import timeit
from itertools import combinations

# Первая часть: алгоритмический перебор всех сочетаний
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

# Первая часть: использование itertools.combinations
def python_method(players, team_size):
    return list(combinations(players, team_size))

# Вторая часть: алгоритмический перебор с ограничением минимум 2 профессионала и отсечкой
def algorithmic_method_with_constraint(players, team_size, professionals, min_pros=2):
    result = []
    team = []

    def backtrack(start, pros_count):
        remaining = team_size - len(team)
        possible_pros_left = sum(1 for p in players[start:] if p in professionals)
        # Отсечка: если даже взяв всех оставшихся профи, не достигнем min_pros
        if pros_count + possible_pros_left < min_pros:
            return

        if len(team) == team_size:
            if pros_count >= min_pros:
                result.append(team.copy())
            return

        for i in range(start, len(players)):
            player = players[i]
            team.append(player)
            backtrack(i + 1, pros_count + (1 if player in professionals else 0))
            team.pop()

    backtrack(0, 0)
    return result

# Вторая часть: itertools с фильтрацией по ограничению
def python_method_with_constraint(players, team_size, professionals, min_pros=2):
    all_combs = combinations(players, team_size)
    filtered = [comb for comb in all_combs if sum(1 for p in comb if p in professionals) >= min_pros]
    return filtered

if __name__ == "__main__":
    professionals = [f'P{i}' for i in range(1, 6)]
    amateurs = [f'A{i}' for i in range(1, 6)]
    players = professionals + amateurs
    team_size = 4

    print("=== Первая часть: без ограничений ===")

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

    print("\n=== Вторая часть: минимум 2 профессионала в команде с отсечкой ===")

    t_alg_c = timeit.timeit(lambda: algorithmic_method_with_constraint(players, team_size, professionals), number=2)
    alg_res_c = algorithmic_method_with_constraint(players, team_size, professionals)

    t_py_c = timeit.timeit(lambda: python_method_with_constraint(players, team_size, professionals), number=2)
    py_res_c = python_method_with_constraint(players, team_size, professionals)

    print(f"Алгоритмический метод с ограничением: найдено {len(alg_res_c)} команд, время {t_alg_c:.6f} сек")
    print("Первые 5 команд:")
    for team in alg_res_c[:5]:
        print(team)

    print(f"\nМетод с использованием itertools с ограничением: найдено {len(py_res_c)} команд, время {t_py_c:.6f} сек")
    print("Первые 5 команд:")
    for team in py_res_c[:5]:
        print(team)
