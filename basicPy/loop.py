angka=1
while angka<=10:
    print(angka)
    angka+=1



for i in range(1):
    print("hidup jokowi".upper(),i)
for i in range(1, 5): #akan di print 1 sampai 5
    print(i)
for i in range(5,0,-1):
    print(i)


    

nama="swargaloka".upper()
for i in nama:
    print(i)
kata=input("input kata-kata == ")
for a in kata:
    print("-",a)


for i in range(15):
    if i % 2 == 0:
        continue
    print(i)


a=int(input("input == "))
for i in range(a):
    if i % 2 == 0:
        continue
    print(i)


kata=input("Input Kata (huruf kecil semua) == ")
dicari=input("Input huruf yang di cari == ")
for huruf in kata:
    if huruf == dicari:
        print(dicari, "ditemukan")
        break
else:
    print(dicari, "tidak ditemukan")


for i in range(1,11):
    for a in range(1,11):
        hasil=i*a
        print(i, "x", a, "=", hasil)
    print("------")

