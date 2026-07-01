print("FILE INPUT_OUTPUT SEDANG BERJALAN")
print("=== INPUT NAMA TEMAN BAIK ===")

file = open("namateman.txt", "w")

while True:
    nama = input("Nama teman: ").title()
    if nama == "":
        break

    umur = (input("Umur teman: ")) 
    noWa = (input("Nomor WA: "))

    file.write(f"{nama}, {umur}, {noWa}\n")
    print("====",nama,"berhasil di simpan","====")
file.close()
print("=== SELESAI ===")



print("=== MENAMPILKAN NAMA ===")

file = open("namateman.txt", "r")
for line in file:
    data = line.strip().split(",")
    print(data[0],data[1],data[2])
file.close()
print("SELESAI")
