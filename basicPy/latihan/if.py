angka=int(input("Input angka == "))
hasil="positif" if angka>0 else "non-positif" #conditional_expression(if)
print("angka tersebut",hasil)   

print("Silahkan Login".upper())
usrname = input("Username: ")
sandi = input("Password: ")
if usrname == "admin123":
     if sandi == "12345678":
      print("Password benar")
      print("Login Berhasil")
if usrname=="admin123" and sandi == "12345678":
     hari=input("Input hari sekolah == ").lower()
     match hari:
      case "senin" | "selasa" | "rabu" | "kamis" |"jumat" : #contoh penggunaan match-case (if)
       print("Kamu Sekolah".upper())
      case "sabtu" | "minggu" :
       print("kamu libur".upper())
      case _:
       print("nama tidak valid".upper())
     umur=int(input("Input umur anda:) == "))
     if umur>17:
      print("Anda Sudah Dewasa")
     if umur<17:
      print("Anda Masih Bocil")
     if umur==17:
      print("Anda Belum 18 tahun")
     if umur>=18:
      nilai_mtk=int(input("Input nilai ujian anda:( == "))
     if nilai_mtk>90:
      print("Anda Lulus Ujian (Grade A)") #contoh penggunaan elif
     elif nilai_mtk>80:
      print("Anda Lulus Ujian (Grade B)")
     elif nilai_mtk>75:
      print("Anda Lulus Ujian (Grade C)")
     else:
      print("Anda Tidak Lulus Ujian","\nBelajar Goblok")
     umur2=int(input("Berapa umur anda == "))
     if umur2 <= 16:
      print("Anda belum punya ktp")
     else:
      punya_ktp=input("Punya KTP (yes/no) == ")
     if umur2 >= 17 and punya_ktp == "yes":
      print("Kerja bro, anda sudah dewasa")
     else:
      print("hahahaha masih bocil")
else:
    print("Password salah")
    print("Login Gagal")









