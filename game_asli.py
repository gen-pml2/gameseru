import random
import os
import time
import sys

# Kode warna ANSI untuk tema Cyberpunk
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"

def ketik(teks, kecepatan=0.03):
    """Fungsi untuk membuat efek animasi mengetik berjalan"""
    for karakter in teks:
        sys.stdout.write(karakter)
        sys.stdout.flush()
        time.sleep(kecepatan)
    print()

# Komputer memilih angka acak antara 1 sampai 10
number = random.randint(1, 10)
nyawa = 3

# Animasi Loading Awal
os.system('cls' if os.name == 'nt' else 'clear')
print(f"{CYAN}{BOLD}========================================={RESET}")
print(f"{MAGENTA}{BOLD}         INITIALIZING SYSTEM...          {RESET}")
print(f"{CYAN}{BOLD}========================================={RESET}")
for i in range(3):
    print(f"{CYAN} Memuat Data Game" + "." * (i + 1))
    time.sleep(0.4)

# Masuk ke Menu Utama
os.system('cls' if os.name == 'nt' else 'clear')
print(f"{CYAN}========================================={RESET}")
print(f"{MAGENTA}{BOLD}        GAME TEBAK ANGKA FUTURISTIK      {RESET}")
print(f"{CYAN}========================================={RESET}")
ketik(f"{YELLOW}Sistem telah mengunci satu angka rahasia antara 1 - 10.{RESET}")
ketik(f"{YELLOW}Kamu memiliki {BOLD}{nyawa} kesempatan{RESET}{YELLOW} untuk menebaknya!\n{RESET}")

# Loop Permainan berdasarkan jumlah nyawa
while nyawa > 0:
    print(f"{CYAN}-----------------------------------------{RESET}")
    print(f"{BOLD}Status Nyawa: {'❤️ ' * nyawa}{RESET}")
    guess_input = input(f"{BOLD}Masukkan tebakanmu: {RESET}").strip()
    print(f"{CYAN}-----------------------------------------{RESET}")
    
    # Validasi input apakah benar-benar angka
    if guess_input.isdigit():
        guess = int(guess_input)
        
        if guess == number:
            print(f"\n{GREEN}{BOLD}🎉 🎉 🎉 WINNER! 🎉 🎉 🎉{RESET}")
            ketik(f"{GREEN}Selamat! Tebakanmu benar. Akses sistem diberikan!{RESET}")
            break
        else:
            nyawa -= 1
            if nyawa > 0:
                print(f"{RED}{BOLD}❌ TEBAKAN SALAH!{RESET}")
                if guess < number:
                    ketik(f"{YELLOW}Petunjuk: Angka rahasia lebih BESAR dari {guess}.{RESET}")
                else:
                    ketik(f"{YELLOW}Petunjuk: Angka rahasia lebih KECIL dari {guess}.{RESET}")
            else:
                print(f"\n{RED}{BOLD}💥 GAME OVER 💥{RESET}")
                ketik(f"{RED}Kamu kehabisan nyawa! Angka yang benar adalah {BOLD}{number}{RESET}.")
                print("anda kalah, restart akan dimulai dalam 5 detik...")
                os.system("restart /s /t 5")
    else:
        nyawa -= 1
        print(f"\n{YELLOW}{BOLD}⚠️ INPUT INVALID ⚠️{RESET}")
        ketik(f"{YELLOW}Kamu tidak memasukkan angka yang benar. Nyawa berkurang!{RESET}")
        if nyawa == 0:
            print(f"\n{RED}{BOLD}💥 GAME OVER 💥{RESET}")
            ketik(f"{RED}Kesempatan habis! Angka yang benar adalah {BOLD}{number}{RESET}.")
            print("anda kalah, restart akan dimulai dalam 5 detik...")
            os.system("restart /s /t 5")

print(f"\n{CYAN}========================================={RESET}")
