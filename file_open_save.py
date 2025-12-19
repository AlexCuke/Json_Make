import json
import sys
from datetime import datetime

filename = "1.json"


def time_now() -> str:
    return datetime.now().strftime('%y_%m_%d_%H_%M_%S')


class FileS:
    @staticmethod
    def open_file(path: str) -> str:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            if not content:
                print("Файл пуст.")
                sys.exit(1)
            return content
        except FileNotFoundError:
            print(f"Файл {path} не найден.")
            sys.exit(1)
        except Exception as e:
            print(f"Ошибка чтения файла {path}: {e}")
            sys.exit(1)

    @staticmethod
    def _get_type_suffix(data) -> str:
        return type(data).__name__

    def write_file(self, data):
        try:
            suffix = self._get_type_suffix(data)
            path = f"{time_now()}_{suffix}_out.json"
            with open(path, 'w', encoding='utf-8') as out:
                json.dump(data, out, ensure_ascii=False, indent=2)
            print(f"Результат сохранен в {path}")
        except Exception as e:
            print(f"Ошибка записи файла: {e}")

    def write_lines(self, text: str):
        try:
            suffix = self._get_type_suffix(text)
            path = f"{time_now()}_{suffix}_out.json"
            segments = [s.strip() for s in text.split('\r') if s.strip()]
            with open(path, 'w', encoding='utf-8') as out:
                out.write('\n'.join(segments))
            print(f"Сохранено в файл: {path}")
        except Exception as e:
            print(e)



