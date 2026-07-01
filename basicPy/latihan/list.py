contohlist = ["Apel", "Semangka", "Durian"]
print(contohlist[0],contohlist[1],contohlist[2])

warna=["Merah", "Kuning", "Hijau"]
warna[0]="Biru"
warna.append("Ungu")
warna.insert(1, "Hitam")
warna.remove("Biru")
warna.pop()
del warna[0]
indexA= [1,2,3,4,5]
indexB= [6,7,8,9,10]
print(indexA+indexB)
print(len(warna))
print(warna)

totalwarna=["hijau","merah","kuning","hitam"]
for warna in totalwarna:
    print(warna.title())

for i in range(0, len(totalwarna)):
    print(totalwarna[i].title())