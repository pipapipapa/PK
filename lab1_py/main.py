import sys
import math


def get_coef(index, prompt):
    while True:
        try:
            if len(sys.argv) > index:
                coef_str = sys.argv[index]
            else:
                print(prompt)
                coef_str = input()
            coef = float(coef_str)
            return coef
        except:
            print("Ошибка ввода")


def solve_quadratic(a, b, c):
    result = []
    D = b * b - 4 * a * c

    if D == 0.0:
        root = -b / (2.0 * a)
        result.append(root)

    elif D > 0.0:
        sqD = math.sqrt(D)
        root1 = (-b + sqD) / (2.0 * a)
        root2 = (-b - sqD) / (2.0 * a)
        result.append(root1)
        result.append(root2)

    return result


def solve_biquadratic(a, b, c):
    quadratic_roots = solve_quadratic(a, b, c)
    all_roots = []

    for root_sq in quadratic_roots:
        if root_sq >= 0:
            roots = solve_quadratic(1, 0, -root_sq)
            all_roots.extend(roots)

    unique_roots = sorted(list(set(all_roots)))
    return unique_roots


def main():
    a = get_coef(1, 'Введите коэффициент А:')
    b = get_coef(2, 'Введите коэффициент B:')
    c = get_coef(3, 'Введите коэффициент C:')

    if a == 0:
        return

    roots = solve_biquadratic(a, b, c)

    len_roots = len(roots)

    if len_roots == 0:
        print('Нет корней')
    elif len_roots == 1:
        print('Один корень: ', *roots)
    elif len_roots == 2:
        print('Два корня: ', *roots)
    elif len_roots == 3:
        print('Три корня: ', *roots)
    elif len_roots == 4:
        print('Четыре корня: ', *roots)


if __name__ == "__main__":
    main()

# Пример запуска
# biquadratic_solver.py 1 -5 4
# biquadratic_solver.py 1 -13 36
