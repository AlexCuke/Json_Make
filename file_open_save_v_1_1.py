import json
import sys
from datetime import datetime



# определение времени сохранения файла
def time_now() -> str:
    return datetime.now().strftime('%y_%m_%d_%H_%M_%S')

#Класс, отвечающий за обработку файлов
class FileS:
    
    
    #открытие файла
    @staticmethod
    def open_file():
        filename = input("Введите имя файла без расширения (.json): ")
        filename= filename+ '.json' 

        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    print("Файл пуст.")
                    sys.exit(1)
                return content
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
            sys.exit(1)
        except Exception as e:
            print(f"Ошибка чтения файла {filename}: {e}")
            sys.exit(1)
    #определение типа данных (под воопросом. Переработать)
    @staticmethod
    def _get_type_suffix(data) -> str:  # ← УБРАЛ self
        if isinstance(data, dict):
            return "dict"
        elif isinstance(data, list):
            return "list"
        elif isinstance(data, str):
            return "str"
        else:
            return type(data).__name__
    # запись файла
    def write_file(self, data):
        try:
            suffix = FileS._get_type_suffix(data)  # ← Правильный вызов
            path = f"{time_now()}_{suffix}_out.json"  # ← Правильная конкатенация
            with open(path, 'w', encoding='utf-8') as out:
                json.dump(data, out, ensure_ascii=False, indent=2)
            print(f"Результат сохранен в {path}")
        except Exception as e:
            print(f"Ошибка записи файла: {e}")



