from pyfiglet import Figlet
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from difflib import SequenceMatcher
from rich.spinner import Spinner
from time import sleep
import random
import os
import pygame
import sys

def resource_path(filename):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, filename)



try:
    pygame.mixer.init()
except Exception as e:
    print("Audio tidak dapat dijalankan:", e)

console = Console()

os.system("cls" if os.name == "nt" else "clear")
os.system("color 0A")
f = Figlet(font="slant")




pygame.mixer.music.load(
    resource_path("A Little Piece Of Heaven.mp3")
)
pygame.mixer.music.play()

benar_sound = pygame.mixer.Sound(
    resource_path("The  winner Takes It All.mp3")
)

salah_sound = pygame.mixer.Sound(
    resource_path("FahhhNew.mp3")
)


textA = Text("TEBAK JODOH GWEH", style="bold green")
console.print(
    Panel.fit(
        textA,
        border_style="green"
    )
)




f = Figlet(font="big")
with console.status(("[bold green]memutar lagu"),spinner="aesthetic"):
    sleep(5)
with console.status(f.renderText("ALAY  BGT  JIR"),spinner="aesthetic"):
    sleep(2)
with console.status(f.renderText("maaf kan gwehh"),spinner="aesthetic"): #aesthetic
    sleep(2)



while True:
    inputjodoh = console.input("\n[bold green]Tebak nama jodoh gwehh > [/bold green]").lower()

    jodoh_benar = [
        "nasywa",
        "nasywaa", 
        "nasywa meida rachmalia", 
        "nasywa meida"
        ]
    hampir_mirip = max(
        SequenceMatcher(None, inputjodoh, i).ratio()
        for i in jodoh_benar
        )
    
    limaCm = [
        "nopi",
        "novi",
        "bella",
        "bela",
        "jajas",
        "piyek"
        ]
        
    mirip5cm = max(
        SequenceMatcher(None,inputjodoh,j).ratio()
        for j in limaCm
    )
    
    if inputjodoh in jodoh_benar:
        pygame.mixer.music.set_volume(0.0)
        benar_sound.set_volume(0.3)
        benar_sound.stop()
        benar_sound.play()
        console.print(random.choice([
            "\n[bold blue]ANDA ADALAH JODOH😭❤️",
            "\n[bold blue]YAHHH KITA JODOHH🥰🥰",
            "\n[bold blue]ANDA BENARR😘🤩",
            "\n[bold blue]TAUU AJAH KITA JODOH🥰"
        ]))
        console.print(f"[grey70]Kemiripan: {hampir_mirip:.2f}[/grey70]")

    elif inputjodoh == "help":
        console.print("\n[bold white]- ketik (exit) untuk keluar")
        console.print("[bold white]- ketik (bebas) untuk menebak jodoh")

    elif inputjodoh == "exit":
        console.print("\n[bold white]ANDA KELUAR\n")
        break

    elif len(inputjodoh) >= 3 and mirip5cm > 0.6:
        pygame.mixer.music.set_volume(0.3)
        benar_sound.stop()
        salah_sound.stop()
        salah_sound.play()
        console.print(random.choice([
          "\n[bold purple]MASA IYA 5cm, gak mungkin",
          "\n[bold purple]MASA IYA SAMAA NOPII😔",
          "\n[bold purple]MASA IYA SAMA BELLA😭",
          "\n[bold purple]MASA IYAA sama DIAA :)"
        ]))
        console.print(f"[grey70]Kemiripan: {hampir_mirip:.2f}[/grey70]")
        
    elif len(inputjodoh) >= 3 and hampir_mirip > 0.5:
        pygame.mixer.music.set_volume(0.3)
        benar_sound.stop()
        salah_sound.stop()
        salah_sound.play()
        console.print(random.choice([
            "\n[bold yellow]hmmmmmm, ada N nya sih :v",
            "\n[bold yellow]okelahh, hampir mirip jodoh gwehh",
            "\n[bold yellow]hampirrr guysss semangat",
            "\n[bold yellow]kurang dikiiiitttt lagi pliss"
        ]))
        console.print(f"[grey70]Kemiripan: {hampir_mirip:.2f}[/grey70]")    
     
    else:
        pygame.mixer.music.set_volume(0.3)
        benar_sound.stop()
        salah_sound.stop()
        salah_sound.play()
        console.print(random.choice([
            "\n[bold red]SIAPA INI? gk kenal jir",
            "\n[bold red]BUKAN, BUKAN, BUKAN inii",
            "\n[bold red]APAA SIHH gajelas",
            "\n[bold red]MASA IYAA INI"
        ]))
        console.print(f"[grey70]Kemiripan: {hampir_mirip:.2f}[/grey70]")
