print("MATERI DASAR PYTHON\n")

print("1. VARIABEL")
print("2. STR TINGKAT LANJUT")
print("3. KONTROL ALUR")
print("4. LOOP")

while True:
    materi_dipilih = input("\nSilahkan pilih: ")

    if materi_dipilih == "1":
            print("\n1. VARIABEL\n")
            with open("variabel.txt", "r") as file:
                print(file.read())
        
    elif materi_dipilih == "2":
            print("\n2. STR TINGKAT LANJUT\n")
            with open("string_tingkatlanjut.txt", "r") as file:
                print(file.read())
    
    elif materi_dipilih == "3":
          print("\n3. KONTROL ALUR\n")
          with open("kontrolalurprogram.txt", "r") as file:
                print(file.read())
    
    elif materi_dipilih == "4":
          print("\n4. LOOP\n")
          with open("loop.txt", "r") as file:
                print(file.read())

    elif materi_dipilih == "exit":
          print("EXIT")
          break
    
    else:
          print("pilihan tidak tersedia")

                

