
class MenuS:   
    def menu(self,result,depth):
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
    def firstmenu():
        name_file = input("Введите имя файла без расширения (.json): ")
        name_file= name_file+ '.json' 
        return name_file