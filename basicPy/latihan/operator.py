a=5
b=10

print(a+b)
print(a-b)
print(a/b)
print(a*b)

print(a//b) #pembagian bulat(hasil tanpa desimal)
print(a%b)  #modulo (sisa pembagian)

print(10%2)
print(11%2)

print(a**b) #perpangkatan
print(5**2)
print(3**4)

x=25
print(x)
x+=10
print(x)
x-=10
print(x)
x*=2
print(x)
x/=2
print(x)

c=7
d=3
e="x = "
print(c,"",d)
print(e, c>d)  #apakah c lebih besar dari d
print(e, c<d)  #apakah c lebih kecil dari d
print(e, c>=d) #apakah c lebih besar/sama dari d
print(e, c<=d) #apakah c lebih kecil/sama dari d
print(e, a==d) #apakah c sama dengan d
print(e, a!=b) #apakah c tidak sama dengan d

n1="Putra"
n2="Arga"
n3="Nana"
print(n1==n2) #apakah n1 sama dengan n2
print(n2==n3)
print(n1!=n2) #apakah n1 tidak sama dengan n2

umur=18
print(umur>17 and umur<22)  #jika salah satu False maka False

nama="Putra"
print(nama=="Putra" or nama=="Nana") #jika salah satu True maka True

aktif= True
print(not aktif) #kebalikan nilai

n_depan="Putra "
n_belakang="Swargaloka "
n_lengkap=n_depan+n_belakang
print(n_lengkap)
print(n_lengkap*2)
print("Putra" in n_depan)
print("Nana" in n_lengkap)
print("Swargaloka" in n_lengkap) #mencari kalimat dalam variabel dengan True/False