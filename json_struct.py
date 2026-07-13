import json
from datetime import datetime, date

class JSonClass:
    def __init__(self):
        self.id = self.__search_id()
        
    def build_struct(self, title: str, finish: str, is_deleting=False):
        if self.is_datetime(finish) == False:
            return False
        
        if not is_deleting:
            self.id += 1
            
        struct = {
            "id": self.id,
            "title": title,
            "create_at": date.today().strftime("%Y-%m-%d"),
            "complete": finish,
        }
        
        return struct

    def operation(self, struct: dict, is_delete: bool):
        try:
            with open('habits.json', 'r') as f:
                data = json.load(f)
            
            if not is_delete:
                data.append(struct)
            else:
                data = [i for i in data if i.get("id") != struct.get("id")]
                
            with open('habits.json', 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            if not is_delete:
                data = [struct] 
            else:
                data = []
            with open('habits.json', 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return e
    
    def read(self):
        try:
            with open("habits.json", 'r') as f:
                return json.load(f)
        except:
            return []  
        
    def is_datetime(self, date: str) -> bool:
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False
        
    def __search_id(self) -> int:
        try:
            with open("habits.json", 'r') as f:
                data = json.load(f)[-1]
            return int(data.get("id"))
        except: 
            return 0
