nama="Putra"
umur=18
note="nama ku "+nama+", umur "+str(umur)
print(note)
print(len(note)) #len digunakan untuk menghitung karakter

index="Putra"
print(index[0]) #index di mulai dari angka 0 
print(index[-1]) #negatif memulai dari belakang
print(index[2:5])
print(index[:3]) 

nama="  putra swargaloka nanda naruto  "
nama_a=nama.title()
nama_b=nama.upper()
nama_c=nama.lower()
nama_d=nama.capitalize()
nama_e=nama.strip()
nama_f=nama.replace("naruto","narotama")
nama_g=nama.count("a")
nama_h=nama.find("naruto")

print(nama_h)

text="Aku Putra anak DKV\numur 18" # \n untuk membuat paragraf baru
text2="Arga=\tumur 18\nkelas=\tDKV" # \t spasi tab
print(text2)

nama0="putra swargaloka nanda narotama"
umur0=18
kota0="Jombang"
profil=f"halo nama ku {nama0.title()}, umur ku {umur0} tahun, aku tinggal di {kota0}" # contoh penggunaan f-string
print(profil)

harga=10000
unit=4.5
total=f"Total Rp{harga*unit:,} aja"
print(total)