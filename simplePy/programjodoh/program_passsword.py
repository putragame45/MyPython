a="-"
print(a*25)
def halo(nama):
    print("Selamat datang", nama)
    print("SILAHKAN LOGIN DULU :)")

halo(input("Siapa nama anda = "))

passwordTrue= "87654321"
percobaan=0
percobaanmax=3

akun=""
while akun != "admin321":
 akun=input("Username = ")
 if akun != "admin321":
   print("Ulangi")


else:
    passwordTrue= "87654321"
    percobaan=0
    percobaanMax=3
    while percobaan<percobaanMax:
     password=input("Password = ")
     percobaan +=1
     if password==passwordTrue:
        print("Login berhasil")
     if password!=passwordTrue:   
        print("Username atau Password salah,", "(tersisa", percobaanMax-percobaan, "percobaan)")
     if password==passwordTrue:   
         enter=(input("Ketik (Enter) untuk melanjutkan (Exit) untuk keluar = "))
         if enter=="Exit":
          exit
         if enter=="Enter":
            print(a*25)
            print("SELAMAT DATANG DI TOKO KAMI")
            print(a*25)
            print("Ayam 100gr     == Rp6,000")
            print("Kopi Kapal Api == Rp8,000")
            print("Beras 5kg      == Rp50,000")
            print(a*25)
            print("input jumlah produk yang ingin di beli (dengan angka)".upper())
            print(a*25)
            unit_ayam =int(input("Ayam 100gr     == "))
            unit_kopi =int(input("Kopi Kapal Api == "))
            unit_beras=int(input("Beras 5kg      == "))
            harga_ayam=6000
            harga_kopi=8000
            harga_beras=50000
            print(a*25)
            total_ayam =f"Ayam 1oogrvv {unit_ayam}x    == Rp{unit_ayam*harga_ayam:,}"
            total_kopi =f"Kopi Kapal Api {unit_kopi}x  == Rp{unit_kopi*harga_kopi:,}"
            total_beras=f"Beras 5kg {unit_beras}x      == Rp{unit_beras*harga_beras:,}"
            total=f"TOTAL HARGA\n----------------\n{total_ayam}\n{total_kopi}\n{total_beras}"
            total_semua=unit_ayam*harga_ayam + unit_kopi*harga_kopi + unit_beras*harga_beras 
            totalRP=f"\nTotal == Rp{total_semua:,}"
            print(total,totalRP)
            print(a*25)
            print("Terimakasih Telah Berbelanja".upper())
            break
         else:
            print("Bye-bye")
            break
         
    else:
        print("Percobaan habis, bye-bye")