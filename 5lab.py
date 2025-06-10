import itertools
import timeit


def alg_teams(lst):
    n = len(lst)
    res = []
    for i in range(n - 3):
        for j in range(i + 1, n - 2):
            for k in range(j + 1, n - 1):
                for l in range(k + 1, n):
                    res.append([lst[i], lst[j], lst[k], lst[l]])
    return res


def py_teams(lst):
    return list(itertools.combinations(lst, 4))


pros = [("P1", 93), ("P2", 81), ("P3", 80), ("P4", 88), ("P5", 85)]
ams = [("A1", 72), ("A2", 71), ("A3", 65), ("A4", 48), ("A5", 75)]
players = pros + ams

teams_alg = alg_teams(players)
teams_py = py_teams(players)


print("=== Первые 10 команд (алгоритмический способ) ===")
for t in teams_alg[:10]:
    print([p[0] for p in t])


print("\n=== Первые 10 команд (itertools.combinations) ===")
for t in teams_py[:10]:
    print([p[0] for p in t])

# Сколько всего команд
total_combinations = len(teams_alg)
print(f"\nВсего различных команд: {total_combinations}")

# Замер времени (каждый вариант запускаем 10 000 раз для усреднения)
alg_time = timeit.timeit(lambda: alg_teams(players), number=10_000)
py_time = timeit.timeit(lambda: py_teams(players), number=10_000)

print("\n Среднее время за один прогон (из 10 000 повторов) ")
print(f"Алгоритмический 4-цикла : {alg_time/10_000:.8f} сек")
print(f"itertools.combinations : {py_time/10_000:.8f} сек")

SKILL_CAP = 300
MAX_SAME_TYPE = 3


def feasible_teams(players):
    for combo in itertools.combinations(players, 4):
        pros_cnt = sum(1 for p in combo if p in pros)
        ams_cnt = 4 - pros_cnt
        total = sum(p[1] for p in combo)
        if pros_cnt <= MAX_SAME_TYPE and ams_cnt <= MAX_SAME_TYPE and total <= SKILL_CAP:
            yield combo, total, pros_cnt, ams_cnt

feasible = list(feasible_teams(players))

feasible_count = len(feasible)
eliminated = total_combinations - feasible_count
reduction_pct = eliminated / total_combinations * 100


print("\nПервые 10 команд, удовлетворяющих ограничениям ")
for combo, total, pc, ac in feasible[:10]:
    names = [p[0] for p in combo]
    print(f"{names} → суммарный скилл: {total}, профи: {pc}, любители: {ac}")


print(f"\nКоличество вариантов, удовлетворяющих ограничениям: {feasible_count}")
print(f"Исключено вариантов: {eliminated} из {total_combinations} "
      f"({reduction_pct:.1f}% сокращение)")


best_total = max(total for _, total, _, _ in feasible)

best_combo = next(rec for rec in feasible if rec[1] == best_total)[0]
best_names = [p[0] for p in best_combo]
print(f"\nСамый лучший вариант (суммарный скилл = {best_total}): {best_names}")





