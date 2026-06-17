a="-"
print(a*17)
opening="selamat datang di toko kami\n----------------"
print(opening.upper())
print("Ayam 100gr     == Rp6,000")
print("Kopi Kapal Api == Rp8,000")
print("Beras kg      == Rp50,000\n----------------")
print("input jumlah produk yang ingin di beli (dengan angka)\n----------------".upper())
unit_ayam =int(input("Ayam 100gr     == "))
unit_kopi =int(input("Kopi Kapal Api == "))
unit_beras=int(input("Beras 5kg      == "))
harga_ayam=6000
harga_kopi=8000
harga_beras=50000
print("----------------")
total_ayam =f"Ayam 1oogr {unit_ayam}x     == Rp{unit_ayam*harga_ayam:,}"
total_kopi =f"Kopi Kapal Api {unit_kopi}x == Rp{unit_kopi*harga_kopi:,}"
total_beras=f"Beras 5kg {unit_beras}x      == Rp{unit_beras*harga_beras:,}"
total=f"TOTAL HARGA\n----------------\n{total_ayam}\n{total_kopi}\n{total_beras}"
total_semua=unit_ayam*harga_ayam + unit_kopi*harga_kopi + unit_beras*harga_beras 
totalRP=f"\nTotal             == Rp{total_semua:,}"
print(total,totalRP)
print(a*17,"\nTerimakasih Telah Berbelanja".upper())
print(a*17)


