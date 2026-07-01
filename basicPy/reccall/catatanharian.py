# TANGGAL
from datetime import datetime
def waktu_sekarang():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

# FUNGSI EDIT PADA MENU NO.1 CATATAN
    # BACA 
def bacacatatan():
        with open("basicPy/reccall/catatanharian.txt", "r") as file:
            catatan_list = file.read().split("===\n")
            return catatan_list
            
    # AMBIL JUDUL
def tampilkanjudul(catatan_list):
        print("0. kembali")
        for nomor, data_catatan in enumerate(catatan_list, start=1):
            for baris in data_catatan.splitlines():
                if baris.startswith("Judul: "):
                    print(f"{nomor}. {baris.replace('Judul:', '').strip()}")

    # PILIH JUDUL
def pilihcatatan(jumlahcatatan):
     while True:
        try:
            pilihan = int(input("\nPilih nomor catatan: "))
            if pilihan == 0:
                return 0
            elif 1 <= pilihan <= jumlahcatatan:
                return pilihan

        except ValueError:
            print("[error]")

    # PRINT JUDUL
def tampilkan_isi(catatan_list, pilihan):
     catatan_dipilih = catatan_list[pilihan - 1]
     print(catatan_dipilih)

    # SAVE JUDUL
def simpan_catatan(catatan_list):
        with open("basicPy/reccall/catatanharian.txt", "w") as file:
            for catatan in catatan_list:
                if catatan.strip():
                    file.write(catatan)
                    file.write("===\n")


# MENU NO. 1 EDIT DALAM MENU CATATAN
def edit_catatan(catatan_list, pilihan):
            judul_baru = input("\nJudul baru: \n")
            catatan_baru = input("\nCatatan baru: \n")
            catatan_list[pilihan - 1] = (
            f"\nTanggal: {waktu_sekarang()}\n"
            f"Judul: {judul_baru}\n"
            f"Catatan: {catatan_baru}\n"
            )
            simpan_catatan(catatan_list)        


# MENU NO.1 CATATAN
def catatan():
        catatan_list = bacacatatan()
        tampilkanjudul(catatan_list)
        pilihan = pilihcatatan(len(catatan_list))
        if pilihan == 0:
                print(f"[kembali]")
                return
        
        tampilkan_isi(catatan_list, pilihan)

        print("1. Edit")
        print("2. Hapus")
        print("3. Kembali")

        while True:
            try:
                aksi = int(input("\nPilih: "))

                if aksi == 1:
                    edit_catatan(catatan_list, pilihan)
                    print(f"[di edit]")

                # MENU NO.2 HAPUS DALAM MENU CATATAN                           
                elif aksi == 2:
                    catatan_list.pop(pilihan - 1)
                    simpan_catatan(catatan_list)
                    print(f"[di hapus]")
                                        
                elif aksi == 3:
                    print(f"[kembali]")
                    break

            except ValueError:
                 print("[error]")


# MENU NO.2 TAMBAH CATATAN
def tambahcatatan():
        judul = input("\nTulis Judul:\n")
        catatan = input("\nTulis Catatan:\n")
        with open("basicPy/reccall/catatanharian.txt", "a") as file:
            file.write(f"\nTanggal: {waktu_sekarang()}\n")
            file.write(f"Judul: {judul.title()}\n")
            file.write(f"Catatan: {catatan}\n")
            file.write(f"\n===\n")
        print(f"\n{judul.title() }[berhasil disimpan]")


# MENU UTAMA
while True:
        print("\n=== CATATAN HARIAN AKU ===")
        print("\n1. Catatan")
        print("2. Tambah Catatan")
        print("3. Exit")
        try:
            opsi = int(input("\nPilih Opsi Menu: "))
            if opsi == 1:
                    print("\n=== Membuka Catatan ===\n".upper())
                    catatan()
            
            elif opsi == 2:
                    print("\n=== Menambahkan Catatan ===".upper())
                    tambahcatatan()
            
            # MENU NO. 3 EXIT
            elif opsi == 3:
                    print("\n=== Keluar ===".upper())
                    break
            
        except ValueError:
             print("[error]")




