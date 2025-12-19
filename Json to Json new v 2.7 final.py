import json
from pprint import pprint

from file_open_save import FileS, filename

ALLOWED_TYPES = (dict, list, str)

print("Распарсинг JSON")


class ContentData:
    def __init__(self, content: str):
        self.content = content
        self.fs = FileS()

    def decode(self):
        try:
            data_json = json.loads(self.content)
            print("Начальный тип данных:", type(data_json).__name__)
            return data_json
        except json.JSONDecodeError as e:
            print(f"Ошибка JSON: {e}")
            return None

    def process_data(self, data, depth: int = 0):
        if not isinstance(data, ALLOWED_TYPES):
            return data

        print(f"[{depth}] {type(data).__name__}")

        if isinstance(data, str):
            result = self.parse_str(data, depth)
        elif isinstance(data, dict):
            result = self.parse_dict(data, depth)
        else:  # list
            result = self.parse_list(data, depth)

        pprint(result)
        choice = input("Продолжить? (y/n/s/sy): ").lower().strip()

        save = 's' in choice
        cont = 'y' in choice
        save_cont = 'sy' in choice

        if save:
            text = result if isinstance(result, str) else str(result)
            self.fs.write_lines(text)

        if cont:
            return self.process_data(result, depth + 1)
        if save_cont:
            text = result if isinstance(result, str) else str(result)
            self.fs.write_lines(text)
            return self.process_data(result, depth + 1)

        return result

    def parse_str(self, data: str, depth: int):
        preview = repr(data[:100]) + "..." if len(data) > 100 else data
        print("Строка:", preview)
        try:
            parsed_json = json.loads(data)
            print("Строка распарсена как JSON:", type(parsed_json).__name__)
            return parsed_json
        except json.JSONDecodeError:
            print("Невалидная JSON строка")
            return data

    def parse_dict(self, data: dict, depth: int):
        keys = list(data.keys())
        print("Ключи словаря:")
        for key in keys:
            pprint(key)
        print("Количество ключей:", len(keys))

        if len(keys) == 1:
            key = keys[0]
            print(f"Автоматически выбран ключ: {key}")
        else:
            key = input("Выберите ключ: ").strip()
            if key not in data:
                print(f"Ключ '{key}' не найден. Доступны: {keys}")
                return data

        return data[key]

    def parse_list(self, data: list, depth: int):
        print("Количество элементов списка:", len(data))
        print("Элементы списка:")

        for i, piece in enumerate(data):
            print(f"[{i}] {type(piece).__name__}")
            pprint(piece)
            print('')

        if len(data) == 1:
            index = 0
            print("Автоматически выбран элемент 0")
        else:
            try:
                index = int(input("Выберите номер элемента: "))
                if index < 0 or index >= len(data):
                    raise ValueError("Индекс вне диапазона")
            except ValueError as e:
                print(f"Ошибка ввода: {e}. Возвращаем первый элемент.")
                index = 0

        return data[index]


def main():
    fs = FileS()
    content = fs.open_file(filename)
    cd = ContentData(content)
    data = cd.decode()
    if data is not None:
        cd.process_data(data)


if __name__ == "__main__":
    main()
