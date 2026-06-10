import json

def data_prep():
    with open("banco.json", "r", encoding="utf-8") as banco:
        biblioteca = json.load(banco)
    return biblioteca


def save(biblioteca): 
    data_prep()
    with open("banco.json", "w", encoding="utf-8") as banco:
        json.dump(biblioteca, banco, indent=4, ensure_ascii=False)
    return