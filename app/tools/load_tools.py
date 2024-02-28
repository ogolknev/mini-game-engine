import json

def loadJson(path: str) -> dict:
    '''
    Возвращает словарь соответствующий указанному json-объекту
    '''
    with open(path) as settings_file:
        return json.load(settings_file)
