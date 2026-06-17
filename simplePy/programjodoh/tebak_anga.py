angka_benar=4
while True:
    tebakan=int(input("Tebak Angka (1-10) == "))
    if tebakan == angka_benar:
        print("Anda Hoki")
        break
    if tebakan >10:
        print("(1-10) Goblog")
    else:
        print("Salah, Ulangi")
