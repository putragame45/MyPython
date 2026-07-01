#=== FITUR TO DO LIST ===

# Tugas Aktif   : 5
# Tugas Selesai : 12

# Simbol prioritas deadline 
# [!] Mepet Deadline
# [~] Hampir Mepet Deadline
# [-] Lebih Cepat Lebih Baik
# nb: daftar tugas di sortir berdasarkan prioritas deadline bukan tanggal dibuat

    # 1. Tugas

        # 0. kembali

        # 1. Daftar Tugas Aktif

            # 0. kembali
                # [kembali ke menu awal]

            # 1. [x] Belajar Python [deadline] [prioritas: !]
            # 2. [x] Belajar Linux [deadline] [prioritas: ~]
            # 3. [x] Mengerjakan Tugas [deadline] [prioritas: -]

                # id tugas: 20260628-001 
                # Tanggal dibuat: 27-06-2026
                # ===
                # Judul   : Belajar Linux
                # Deskripsi: buat ppt tugas pak arif
                # Deadline: 
                # Status  : [Belum Selesai]
                # Tanggal Selesai: 
                # ===

                    # 1. Tandai Selesai
                        # [tugas akan di hapus setelah seminggu jika status selesai]
                        # konfirmasi [y/n]

                        # [diperbarui]            
                        # Status: Selesai
                        # Tanggal Selesai: 30-06-2026

                    # 2. Edit
                        # Judul:
                        # Deskripsi:
                        # Deadline: 
                        # konfirmasi [y/n]
                        # [edit sukses]

                    # 3. Kembali
                        # [kembali ke list tugas]
                
    # 2. Tambah Tugas

        # konfirmasi tambah tugas [y/n]
            # [y]
                # Judul: 
                # Deskripsi:
                # Deadline: [input tanggal]
                # Status: [selesai/belum selesai]

                # [tugas (id tugas) di tambahkan]

            # [n]
                # [kembali ke menu awal]

    # 3. Tugas Selesai

        # 0. kembali
            # [kembali ke menu awal]

        # Daftar Tugas Selesai

        # nb: tugas akan di hapus setelah seminggu jika status selesai

        # 1. [x] Belajar Python [tugas_selesai_30-06-2026]
        # 2. [x] Belajar Linux [tugas_selesai_30-06-2026]
        # 3. [x] Mengerjakan Tugas [tugas_selesai_30-06-2026]

    # 4. Exit
        # [keluar]

# UTILITAS
import json
from datetime import datetime

def waktu_sekarang():
    return datetime.now().strftime("%d-%m-%Y")

def baca_file():
    try:
        with open("basicPy/reccall/tugas.json", "r") as file:
            daftar_tugas = json.load(file)

        return daftar_tugas
    
    except:
        return []

def simpan_file(daftar_tugas):
    with open("basicPy/reccall/tugas.json", "w") as file:
        json.dump(daftar_tugas, file, indent=4)

def buat_tugas(judul, deskripsi, deadline):
    return{
    "id": buat_id(),
    "tanggal_dibuat": waktu_sekarang(),
    "judul": judul,
    "deskripsi": deskripsi,
    "deadline": deadline,
    "status": "[Belum Selesai]",
    "tanggal_selesai": ""
    }

def menu_edit(daftar_tugas, pilihan): 
    try:
        print("\n0. Kembali")
        print("1. Tandai Selesai")
        print("2. Edit")
        
        inputmenu1_b = int(input("\nPilih Opsi: "))

        if inputmenu1_b == 1:
            tandai_selesai(daftar_tugas, pilihan)
                                
        elif inputmenu1_b == 2:
            edit_tugas()
                                
        elif inputmenu1_b == 0:
            return lihat_tugas()

    except ValueError:
        print("[menu tidak tersedia]")
        
    
def pilih_tugas():
    while True:
        daftar_tugas = sorted(
            baca_file(),
            key=lambda tugas: datetime.strptime(
                tugas['deadline'],
                "%d-%m-%Y")
        )

        for nomor, tugas in enumerate(daftar_tugas, start=1):
            if tugas['status'] ==  "[Selesai]":
                print(f"{nomor}. {tugas['judul']} {tugas['status']}")

            elif tugas['status'] == '[Belum Selesai]':
                print(f"{nomor}. {tugas['judul']} [deadline: {tugas['deadline']} {hitung_prioritas(tugas['deadline'])} ]")
        
        try:
            inputmenu1_a = int(input("\nPilih Tugas: "))

            if inputmenu1_a == 0:
                return menu()
            
            elif 1 <= inputmenu1_a <= len(daftar_tugas):
               
                tugas = daftar_tugas[inputmenu1_a - 1]
                if tugas['status'] ==  "[Selesai]":
                    print("\n[tugas anda telah selesai]\n")
                    continue    

                tampilkan_tugas(daftar_tugas, inputmenu1_a)
                return daftar_tugas, inputmenu1_a

            else:
                print("\n[tugas tidak ada]\n")
            
        except ValueError:
            print("\n[input tidak valid]\n")

     
def tampilkan_tugas(daftar_tugas, inputmenu1_a):
    
    tugas = daftar_tugas[inputmenu1_a -1]
    tampilkan_detail(tugas)


def buat_id():
    hariini = datetime.now().strftime("%Y%m%d")
    daftar_tugas = baca_file()
    jumlah = 0
    for tugas in daftar_tugas:
        if tugas["id"].startswith(hariini):
            jumlah += 1
    nomor = jumlah+ 1

    return f"{hariini}-{nomor:03d}"


def hitung_prioritas(deadline):
    deadline = datetime.strptime(deadline,"%d-%m-%Y")
    hariini = datetime.now()
    selisih_hari = (deadline - hariini).days
    if selisih_hari <= 0:
        prioritas = "[⚠"

    elif selisih_hari <= 3:
        prioritas = "[!]"

    elif selisih_hari <= 6:
        prioritas = "[~]"

    else:
        prioritas = "[-]"

    return prioritas


def tampilkan_detail(tugas):
    print(f"""
    ID                : {tugas['id']}
    Tanggal dibuat    : {tugas['tanggal_dibuat']}

    Judul             : {tugas['judul']}
    Deskripsi         : {tugas['deskripsi']}
    Deadline          : {tugas['deadline']}
    Status            : {tugas['status']}
    Tanggal selesai   : {tugas['tanggal_selesai']}
    """)

def konfirmasi():
    pass


# LIHAT TUGAS
def lihat_tugas():
    
    while True:
    
        try:
            print("\n0. Kembali")
            daftar_tugas, pilihan = pilih_tugas()
            menu_edit(daftar_tugas, pilihan)
        
        except ValueError:
            print("[menu tidak tersedia]")


def tambah_tugas():
    while True:
        try:
            pilihantambahtugas = str(input("tambahkan tugas? [y/n] ")).lower()

            if pilihantambahtugas == "y":
                print("\n[tambah tugas anda]\n")
                judul = input("Judul: ")
                deskripsi = input("Deskripsi: ")
                deadline = input("Deadline (dd-mm-yyyy): ")

                tugas = buat_tugas(judul,deskripsi,deadline)

                daftar_tugas = baca_file()

                daftar_tugas.append(tugas)

                simpan_file(daftar_tugas)

                print(f"\n[{judul}] di simpan\n")

            elif pilihantambahtugas == "n":
                print("\n[kembali ke menu awal]\n")
                return menu()
                

        except ValueError:
            print("[menu tidak tersedia]")

def edit_tugas():
    try:
            pilihantambahtugas = str(input("edit tugas? [y/n] ")).lower()

            if pilihantambahtugas == "y":
                print("\n[edit tugas anda]\n")
                judul = input("Judul: ")
                deskripsi = input("Deskripsi: ")
                deadline = input("Deadline (dd-mm-yyyy): ")

                tugas = buat_tugas(judul,deskripsi,deadline)

                daftar_tugas = baca_file()

                daftar_tugas.append(tugas)

                simpan_file(daftar_tugas)

                print(f"\n[{judul}] di simpan\n")

            elif pilihantambahtugas == "n":
                print("\n[kembali ke menu awal]\n")
                return menu()
                

    except ValueError:
            
            print("[menu tidak tersedia]")




def tandai_selesai(daftar_tugas, pilihan):

    tugas = daftar_tugas[pilihan -1]

    if tugas["status"] == "[Selesai]":
        print("[Tugas sudah selesai]")
        return

    print("\n[tugas akan di hapus setelah seminggu jika status selesai]\n")
    inputselesai = input("Yakin sudah selesai [y/n] ").lower()

    if inputselesai == "y":

        tugas["status"] = "[Selesai]"
        tugas["tanggal_selesai"] = waktu_sekarang()
        simpan_file(daftar_tugas)
        print("[Tugas berhasil diselesaikan]")


    elif inputselesai == "n":
        return

def tampilkan_tugas_selesai():
    daftar_tugas = baca_file()
    nomor = 1
    for tugas in daftar_tugas:
        if tugas['status'] ==  "[Selesai]":
            print(f"{nomor}. {tugas['judul']} {tugas['status']} {tugas['tanggal_selesai']}")
            nomor +=1
  
# MENU
def jumlah_tugas_aktif():
    daftar = baca_file()
    return len(daftar) - jumlah_tugas_selesai()


def jumlah_tugas_selesai():
    daftar = baca_file()
    jumlah = 0

    for tugas in daftar:

        if tugas["status"] == "[Selesai]":
            jumlah += 1

    return jumlah

def menu():
 # Menu Awal
    print("\n=== TO DO LIST TUGAS ===\n")

    print(f"Tugas Aktif: {jumlah_tugas_aktif()}")
    print(f"Tugas selesai: {jumlah_tugas_selesai()}")

    print("\nSimbol Prioritas: ")
    print("[⚠] TERLAMBAT")
    print("[!] Mepet Deadline")
    print("[~] Hampir Mepet Deadline")
    print("[-] Lebih Cepat Lebih Baik")

    print("\n1. Lihat Tugas")
    print("2. Tambah Tugas")
    print("3. Tugas Selesai")
    print("4. Exit")

    while True:
        try:
            inputmenu = int(input("\nPilih menu: "))

            # 1. Tugas
            if inputmenu == 1:
                print("\n[daftar tugas aktif]\n")
                print("nb: daftar tugas di sortir berdasarkan prioritas deadline bukan tanggal dibuat")
                lihat_tugas()
                
            # 2. Tambah Tugas
            elif inputmenu == 2:
                print("\n[tambah tugas]\n")
                tambah_tugas()

            # 3. Tandai Selesai
            elif inputmenu == 3:
                print("\n[daftar tugas selesai]\n")
                tampilkan_tugas_selesai()

            # 4. Exit    
            elif inputmenu == 4:
                print("\n[anda keluar]\n")
                exit()

        except ValueError:
            print("\n[ulangi]")

menu()