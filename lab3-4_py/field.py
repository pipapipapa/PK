# Пример:
goods = [
    {'title': 'Ковер', 'price': 2000, 'color': 'green'},
    {'title': 'Диван для отдыха', 'price': 5300, 'color': 'black'}
]


# field(goods, 'title') должен выдавать 'Ковер', 'Диван для отдыха'
# field(goods, 'title', 'price') должен выдавать {'title': 'Ковер', 'price': 2000}, {'title': 'Диван для отдыха', 'price': 5300}

def field(items, *args):
    assert len(args) > 0

    result = []
    if len(args) == 1:
        for it in items:
            value = str(it.get(args[0]))
            if value:
                result.append(f"{value}")

    else:
        for it in items:
            value = {key: it.get(key) for key in args if it.get(key) is not None}
            if value:
                result.append(value)

    return result


if __name__ == '__main__':
    titles = field(goods, 'title')
    print(", ".join(f"'{title}'" for title in titles))
    titles = field(goods, 'title', 'price')
    print(", ".join(f"{title}" for title in titles))