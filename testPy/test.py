listnama = [
    "nanas",
    "nasy",
    "wawa",
    "nasywa",
    "nana", 
]

def lsnama(listnama):
    for nama in listnama:
        print(nama)

print(lsnama(listnama))

namabaru  = listnama.append(input("tambahkan nama: "))
with open("testPy/test.py", "a") as file:
    file.write(namabaru) 
    
print(lsnama(listnama))