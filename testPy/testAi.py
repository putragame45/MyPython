def tambah(a, b):
    return a + b
def kurang(a, b):
    return a - b
def kali(a, b):
    return a * b
def bagi(a, b):
    if b == 0:
        return "Error: Pembagian dengan nol tidak diperbolehkan."
    return a / b

print("Kalkulator Sederhana")
print("Pilih operasi: ")
print("1. Tambah")
print("2. Kurang")
print("3. Kali")
print("4. Bagi")

while True:
 operasi = input("Masukkan pilihan operasi (1/2/3/4): ")
 if operasi == "1":
    print("Hasil tambah: ", tambah(int(input("Masukkan angka pertama: ")), int(input("Masukkan angka kedua: "))))
    break
 elif operasi == "2":
    print("Hasil kurang: ", kurang(int(input("Masukkan angka pertama: ")), int(input("Masukkan angka kedua: "))))
    break
 elif operasi == "3":
    print("Hasil kali: ", kali(int(input("Masukkan angka pertama: ")), int(input("Masukkan angka kedua: "))))
    break
 elif operasi == "4":
    print("Hasil bagi: ", bagi(int(input("Masukkan angka pertama: ")), int(input("Masukkan angka kedua: "))))     
    print("Hasil bagi dengan nol: ", bagi(int(input("Masukkan angka pertama: ")), int(input("Masukkan angka kedua: "))))
    break
 else:  print("error")