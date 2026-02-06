import json
import hl7parser
import hl7
import re
from pprint import pprint

from file_open_save_v_1_1 import FileS #Импортируем данные из функций и класса импорта файлов

ALLOWED_TYPES = (dict, list, str) # Типы данных

print("Распарсинг JSON")           # Приветствие

#Класс контент
class ContentData:
    def __init__(self, content: str):      
        self.content = content
        self.fs = FileS()
        self.result = None  # Добавлено
        self.depth = 0      # Добавлено
    #декодирует сырой тип данных(строка) в верный тип данных
    def decode(self):
        try:
            data_json = json.loads(self.content)
            print("Начальный тип данных:", type(data_json).__name__)
            return data_json
        except json.JSONDecodeError as e:
            print(f"Ошибка JSON: {e}")
            return None       

    #ОСНОВНАЯ ФУНКЦИЯ
    def process_data(self, data, depth: int = 0):
        # Data -  это текущий элемент JSON на данном уровне вложенности
        # Depth - отслеживает уровень вложенности
        #сравниваем данные для определенитя типа данных (вопрос на переработку)
        self.depth=depth
        
        # Парсим сначала
        result = self._parsing_type(data, depth)
        self.result = result
        
        # Показываем результат
        print("\nРезультат парсинга:")
        pprint(result)
        
        # Спрашиваем ПОСЛЕ парсинга
        self._menu(result, depth)
        return self.result   
       
    def _parsing_type(self,data,depth):
        result = data
        #выбор метода парсинша в зависимости от типа данных 
        if isinstance(data, str):
            result = self.parse_str(data, depth)     
        elif isinstance(data, dict):
            result = self.parse_dict(data, depth)
        else:  # list
            result = self.parse_list(data, depth)  
        return result    
    # Меню продолжения работы программы
    def _menu(self,result,depth):
        # стоит ли продолжать или сохранить
        choice = input("Продолжить? (y/n/s/sy): ").lower().strip()
        #нажимаем сохранить РАБОТАЕТ НЕКОРРЕКТНО
        if choice == 's':                       
            self.fs.write_file(result)
            print('Сохранено')
        # нажимаем продолжить
        if choice == 'y':
            self.process_data(result, depth + 1)   
        # нажимаем сохранить и продолжить 
        elif  choice == 'sy':
            self.fs.write_file(result)
            print('Сохранено')
            self.process_data(result, self.depth + 1)         
                
    # Парсинг словаря
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
    # Парсинг списка   
    def parse_list(self, data: list, depth: int):
        print("Количество элементов списка:", len(data))
        print("Элементы списка:")

        for i, piece in enumerate(data):
            print(f"Номер:{i} Тип: {type(piece).__name__} Количество элементов: {len(piece)}")
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
    # Парсинг строки  # валидация и парсинг h17
   
    def parse_str(self, data: str, depth: int):
        preview = repr(data[:100]) + "..." if len(data) > 100 else data
        print("Строка:", preview)
        
        data = data.strip().replace('\n', '\r')
        
        # Проверка стандартного HL7 (с MSH)
        if data.startswith('MSH|') and '\r' in data:
            return self._parse_standard_hl7(data)
        
        # Проверка вашего формата (PID без MSH)
        elif data.startswith('PID|') and '\r' in data:
            print("Обнаружено неполное HL7 (без MSH)")
            return self._parse_partial_hl7(data)
        
        # JSON
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return data

    def _parse_standard_hl7(self, data):
        try:
            h = hl7.parse(data)
            return {
                'is_hl7': True,
                'type': 'standard',
                'segments': len(h),
                'message_type': f"{h[0][8][0]}^{h[0][8][1]}" if len(h) > 0 else None,
                'parsed': h
            }
        except Exception as e:
            return {'is_hl7': False, 'reason': str(e)}

    def _parse_partial_hl7(self, data):
        """Парсинг вашего неполного HL7"""
        segments = data.split('\r')
        result = {
            'is_hl7': True,
            'type': 'partial',
            'segments': [],
            'patient_id': None
        }
        
        for i, seg in enumerate(segments):
            if seg.strip():
                fields = seg.split('|')
                seg_name = fields[0]
                result['segments'].append({
                    'name': seg_name,
                    'fields': fields,
                    'raw': seg
                })
                
                # Извлечение PID
                if seg_name == 'PID' and len(fields) > 3:
                    result['patient_id'] = fields[3]  # ID пациента
        
        print(f"Распарсено {len(result['segments'])} сегментов")
        return result
            





'''
def main():
    fs = FileS()                                            #создание обьекта класса FileS
    content = fs.open_file(filename)                        #сырая выгрузка данных из файла, 
    cd = ContentData(content)                               #создание обьекта класса cd и всегла строка так как "сырое содержимое"
    data = cd.decode()                                      #декодирует сырой тип данных(строка) в верный тип данных
    if data is not None:                                    #если данные не равны классу None работем
        cd.process_data(data)



if __name__ == "__main__":
    main()
'''
def _print(dataset):
    print(dataset)
    print(type(dataset))
def test():
    fs = FileS()                                                #создание обьекта класса FileS
    #print(fs)
    print('fs = FileS():', type(fs))
    content = fs.open_file()                            #сырая выгрузка данных из файла, 
    #print(content)
    print('content = fs.open_file(filename):', type(content))
    cd = ContentData(content)                                   #создание обьекта класса cd и всегла строка так как "сырое содержимое"                   
    #print(cd)
    print('cd = ContentData(content):', type(cd))
    data = cd.decode()                                          #декодирует сырой тип данных(строка) в верный тип данных
    #print(data)
    print(' data = cd.decode():', type(data)) 
    print('')   
    print('')  
    print('Начало основной функции')                 
    cd.process_data(data)



if __name__ == "__main__":
    test()
