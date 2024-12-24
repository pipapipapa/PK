import json
from print_result import print_result
from unique import Unique
from gen_random import gen_random
from field import field
from cm_timer import cm_timer_1

path = './data_light.json'

with open(path, encoding='utf-8') as f:
    data = json.load(f)

# Необходимо в переменную path сохранить путь к файлу, который был передан при запуске сценария

# Далее необходимо реализовать все функции по заданию, заменив `raise NotImplemented`
# Предполагается, что функции f1, f2, f3 будут реализованы в одну строку
# В реализации функции f4 может быть до 3 строк

@print_result
def f1(arg):
    return list(Unique(field(arg, "job-name"), ignore_case=True))


@print_result
def f2(arg):
    return list(filter(lambda x: x.lower().startswith("программист"), arg))


@print_result
def f3(arg):
    return list(map(lambda x: f"{x} с опытом Python", arg))


@print_result
def f4(arg):
    salaries = gen_random(len(arg), 100000, 200000)
    return [f"{job}, зарплата {salary} руб." for job, salary in zip(arg, salaries)]


if __name__ == '__main__':
    with cm_timer_1():
        f4(f3(f2(f1(data))))
