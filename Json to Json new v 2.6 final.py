import json
from pprint import pprint
import sys

types_of_data = [dict, list, str]
filename = "1.json"
out_filename = "out.json"

print("Распарсинг JSON")

class FileS():
    def __init__(self):
        pass
    def open_file(self, file):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            if not content:
                print("Файл пуст.")
                sys.exit(1)
            return content
        except FileNotFoundError:
            print(f"Файл {file} не найден.")
            sys.exit(1)
        except Exception as e:
            print(f"Ошибка чтения файла: {e}")
            sys.exit(1)
    def write_file(self, file, data):  # ← добавили data
        try:
            with open(file, 'w', encoding='utf-8') as out:
                json.dump(data, out, ensure_ascii=False, indent=2)  # ← пишем data
            print(f"Результат сохранен в {file}")
        except Exception as e:
            print(f"Ошибка записи файла: {e}")
class Content_data():
    def __init__(self,content):
        self.content=content
        self.new_file = FileS()
        pass
    def decode(self):
        try:
            data_json = json.loads(self.content)
            print("Начальный тип данных:", type(data_json).__name__)
            return data_json
        except json.JSONDecodeError as e:
            print(f"Ошибка JSON: {e}")
            return None
        
    def process_data(self, data_json, depth=0):
        if not isinstance(data_json, tuple(types_of_data)):
            return data_json
        
        type_name = type(data_json).__name__
        print(f"[{depth}] {type_name}")
        
        if isinstance(data_json, str):
            return self.pars_str(data_json, depth)
        elif isinstance(data_json, dict):
            result = self.pars_dict(data_json, depth)
        elif isinstance(data_json, list):
            result = self.pars_list(data_json, depth)
        
        pprint(result)
        choice = input("Продолжить? (y/n/s): ").lower().strip()
        
        if choice == 'y':
            return self.process_data(result, depth + 1)
        if choice == 's':
            self.new_file.write_file(out_filename, result)
            return result
        return result
    
    def pars_str(self, data, depth):
        print("Строка:", repr(data[:100]) + "..." if len(data) > 100 else data)
        try:
            parsed_json = json.loads(data)
            print("Строка распарсена как JSON:", type(parsed_json).__name__)
            return parsed_json
        except json.JSONDecodeError:
            print("Невалидная JSON строка")
            return data
        
    def pars_dict(self, data, depth):
        data_keys = list(data.keys())
        print("Ключи словаря:")
        for piece in data_keys: 
            pprint(piece)  
        print("Количество ключей:", len(data_keys))
        
        if len(data) == 1:
            key = data_keys[0]
            print(f"Автоматически выбран ключ: {key}")
        else:     
            key = input("Выберите ключ: ").strip()
            if key not in data:
                print(f"Ключ '{key}' не найден. Доступны: {data_keys}")
                return data
        return data[key]

    def pars_list(self, data, depth):  # ✅ Добавлен self и используется
        print("Количество элементов списка:", len(data))
        print("Элементы списка:")
        for i, piece in enumerate(data): 
            print(f"[{i}] {type(piece).__name__}")
            pprint(piece)
            print('')
        
        if len(data) == 1:
            key = 0
            print("Автоматически выбран элемент 0")
        else:     
            try:
                key = int(input("Выберите номер элемента: "))
                if key < 0 or key >= len(data):
                    raise ValueError("Индекс вне диапазона")
            except ValueError as e:
                print(f"Ошибка ввода: {e}. Возвращаем первый элемент.")
                key = 0
        
        return data[key]    

# Основной код
new_file=FileS()
content=new_file.open_file(filename)
content_data=Content_data(content)
data_json = content_data.decode()
if data_json is not None:
    final_result = content_data.process_data(data_json)
