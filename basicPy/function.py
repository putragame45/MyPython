


def sapa(nama):
    print("Selamat pagi", nama)
    print("Senang bertemu dengan mu :) ")
sapa(input("Input nama = "))

def hitungluas(panjang, lebar):
    luas=panjang*lebar
    print("luas adalah ", luas)
hitungluas(int(input("panjang = ")),int(input("lebar = ")))

def penjumlahan(A, B):
    c=A+B
    print("Hasil =",c)
penjumlahan(int(input("hitung A = ")), int(input("Hitung B = ")))


def luasLingkaran(radius):
    pi=3.14159
    luas=pi*radius*radius
    return luas
luas1=luasLingkaran(5)
luas2=luasLingkaran(10)

print("luas lingkaran radius 5: ",luas1)
print("luas lingkaran radius 10: ",luas2)
print("Total luas: ", luas1+luas2)

def sapa(nama, sapaan="hello"):
    print(sapaan,nama)

sapa(input("Namamu: "),)
sapa("Budi", "HAIIIII")


def perkenalan(nama, umur, negara):
    print("nama saya ",nama)
    print("umur saya ", umur, "tahun")
    print("negara saya ",negara, "seumur hidup")
    if negara=="WNI":
     print("SABARR YA JADI WNI")

perkenalan(nama=input("Nama mu? ") ,umur=input("Umur? ") ,negara=input("WNI? ") )

def profil1(nama, umur, kota="Jombang", status="Kerja"):
    print(f"=== PROFIL {nama.upper()} ===")
    print(f"Umur: {umur} tahun")
    print(f"Kota: {kota}")
    print(f"Status: {status}")
    print("====================")
    print()

profil1("Budi", 25)
profil1("Siti", 30, kota="Surabaya")
profil1("Andi", 22, status="Mahasiswa")

def cetak_list(*args):
    for item in args:
        print(item)

cetak_list("apel", "pisang", "jeruk")