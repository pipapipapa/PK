class Unique(object):
    def __init__(self, items, **kwargs):
        self.items = iter(items)
        self.set = set()
        self.ignore_case = kwargs.get('ignore_case', False)

    def __next__(self):
        item = next(self.items)

        if self.ignore_case and isinstance(item, str):
            item_to_check = item.lower()
        else:
            item_to_check = item

        while item_to_check in self.set:
            item = next(self.items)

            if self.ignore_case and isinstance(item, str):
                item_to_check = item.lower()
            else:
                item_to_check = item

        self.set.add(item_to_check)
        return item

    def __iter__(self):
        return self


if __name__ == '__main__':
    data = ['a', 'A', 'b', 'b', 'c', 'C', 'd']
    unique_iterator = Unique(data, ignore_case=True)

    for item in unique_iterator:
        print(item)
