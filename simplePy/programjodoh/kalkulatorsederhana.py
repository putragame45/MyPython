
def tambah(a, b):
    return a + b
def kurang(a, b):
    return a - b
def kali(a, b):
    return a * b
def bagi(a, b):
    if b == 0:
        return "Error: Pembagian dengan nol tidak diperbolehkan."
    return a / b


from pyfiglet import Figlet
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import time
import os


console = Console()


os.system("cls" if os.name == "nt" else "clear")


os.system("color 0A")


f = Figlet(font="slant")


title = f.renderText("KALKULATOR")


hacker_text = Text(title, style="bold green")


console.print(
    Panel.fit(
        hacker_text,
        border_style="green",
        title="[bold red]ACCESS TERMINAL[/bold red]",
        subtitle="[green]SYSTEM READY[/green]"
    )
)

console.print("\n[green]Menghubungkan ke hati mu", end="")

for i in range(6):
    console.print(".", style="green", end="")
    time.sleep(0.5)


console.print("\n\n[bold green][ ANJAY BANGET KAN ][/bold green]")

print("\nPilih operasi: ".upper())
console.print("\n[green]1.[/green] Penjumlahan")
console.print("[green]2.[/green] Pengurangan")
console.print("[green]3.[/green] Perkalian")
console.print("[green]4.[/green] Pembagian")
console.print("[green]0.[/green] Exit")


while True:
 operasi = console.input("\n[bold green]Pilih Operasi > [/bold green]")
 if operasi == "0":
    console.print("\n[bold green]ANDA KELUAR[/bold green]\n")
    break
 console.print(f"\n[bold green]Menu dipilih:[/bold green] {operasi}")
 if operasi == "1": 
    try:
       console.print("\n[bold green]=================================[/bold green]")
       print("Hasil tambah:", tambah(int(input("Masukkan angka pertama: ")),int(input("Masukkan angka kedua: "))))
       console.print("[bold green]=================================[/bold green]")
    except ValueError:
       print("angka tidak valid")
 elif operasi == "2":
    try:
       console.print("\n[bold green]=================================[/bold green]")
       print(f"Hasil kurang: ", kurang(int(input("Masukkan angka pertama: ")), int(input("Masukkan angka kedua: "))))
       console.print("[bold green]=================================[/bold green]")
    except ValueError:
       print("angka tidak valid")
 elif operasi == "3":
    try:
       console.print("\n[bold green]=================================[/bold green]")
       print("Hasil kali: ", kali(int(input("Masukkan angka pertama: ")), int(input("Masukkan angka kedua: "))))
       console.print("[bold green]=================================[/bold green]")
    except ValueError:
       print("angka tidak valid")   
 elif operasi == "4":
    try:
       console.print("\n[bold green]=================================[/bold green]")
       print("Hasil bagi: ", bagi(int(input("Masukkan angka pertama: ")), int(input("Masukkan angka kedua: "))))
       console.print("[bold green]=================================[/bold green]")    
    except ZeroDivisionError:
       print("tidak bisa di bagi 0")
    except ValueError:
       print("angka tidak valid")
 else: print("\nerror ulangi lagi")