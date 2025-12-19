
import json
import sys
import datetime
filename = "1.json"
out_filename = "out.json"


class Times():
    def __init__(self):
        pass
    def time_now(self):
        self.full_time=datetime.datetime.now()
        return self.full_time.strftime('%y_%m_%d_%H_%M_%S')
time=Times()
out_filename = time.time_now()+"out.json"

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
            
    def _get_type_suffix(self, data):
        if isinstance(data, dict):
            return "dict"
        elif isinstance(data, list):
            return "list"
        elif isinstance(data, str):
            return "str"
        else:
            return type(data).__name__

    def write_file(self, data):
        try:
            time = Times()
            type_suffix = self._get_type_suffix(data)
            file = f"{time.time_now()}_{type_suffix}_out.json"
            with open(file, 'w', encoding='utf-8') as out:
                json.dump(data, out, ensure_ascii=False, indent=2)
            print(f"Результат сохранен в {file}")
        except Exception as e:
            print(f"Ошибка записи файла: {e}")
            
    def write_lines(self, text: str):
        try:
            time = Times()
            file = time.time_now() + '_out.json'   # например, .hl7
            type_suffix = self._get_type_suffix(text)
            file = f"{time.time_now()}_{type_suffix}_out.json"
            # text: "PID|...|\rIN1|...|\rDG1|...|\rORC|...|\rOBR|...|"
            segments = [s for s in text.split('\r') if s.strip()]

            with open(file, 'w', encoding='utf-8') as out:
                for i, seg in enumerate(segments):
                    line = seg.strip()
                    out.write(line)
                    if i < len(segments) - 1:
                        out.write('\n')   # реальный перевод строки

            print(f'Сохранено в файл: {file}')
        except Exception as e:
            print(e)




