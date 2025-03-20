import os
import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

# Banner
banner = """
 ███████╗██╗  ██╗██╗   ██╗███████╗███████╗    ███████╗███████╗
██╔════╝██║ ██╔╝╚██╗ ██╔╝╚══███╔╝╚══███╔╝    ██╔════╝██╔════╝
███████╗█████╔╝  ╚████╔╝   ███╔╝   ███╔╝     ███████╗█████╗  
╚════██║██╔═██╗   ╚██╔╝   ███╔╝   ███╔╝      ╚════██║██╔══╝  
███████║██║  ██╗   ██║   ███████╗███████╗    ███████║██║     
╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚══════╝    ╚══════╝╚═╝     
                                                             
                                            
     SHELL FINDER  BY SKYZZXPLOIT |   
"""
print(Fore.LIGHTRED_EX + banner)

# Disable SSL warnings and initialize Colorama
urllib3.disable_warnings()
init(autoreset=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Keywords to identify shells and backdoors
KEYWORDS = [
    b'{Ninja-Shell}', b'drwxr-xr-x', b'drwxrwxrwx', b'-rw-r--r--',
    b'Backdoor Destroyer', b'Gel4y Mini Shell', b'Tiny File Manager',
    b'File manager', b'#0x2525', b'{Ninja-Shell}', b'./AlfaTeam',
    b'Mr.Combet', b'%PDF-0-1', b'nopebee7 [@] skullxploit',
    b'X0MB13', b'https://github.com/fluidicon.png',
    b'Madstore.sk! - Priv8 Sh3ll!', b'base64_decode', b'cmd=', b'phpinfo();',
    b'@eval', b'@system', b'@exec', b'@shell_exec', b'@passthru',
    b'<?php', b'?>', b'c99madshell', b'system(', b'proc_open', b'shell', 
    b'webshell', b'cmd.php', b'upload.php', b'admin.php', b'config.php',
    b'login.php', b'wp-config.php', b'select * from', b'drop table',
    b'insert into', b'php://input', b'php://filter', b'php://output',
    b'php://memory', b'php://temp', b'wp-admin', b'wp-content', 
    b'wp-includes', b'wp-login.php', b'xmlrpc.php'
]

# Paths to check for vulnerabilities
PATHS = [
    '/index.php'
]

# Fungsi untuk memeriksa kerentanan suatu domain
def check_domain_vulnerability(domain, paths):
    for path in paths:
        url = f"{domain}{path}"
        try:
            response = requests.get(url, headers=HEADERS, verify=False, timeout=10)
            content = response.content

            # Cek status code
            if response.status_code != 200:
                print(f" - {domain} - {Fore.LIGHTYELLOW_EX}URL Tidak Dapat Diakses ({response.status_code}){Style.RESET_ALL}")
                continue

            # Cek apakah ada keyword dalam konten
            if any(keyword in content for keyword in KEYWORDS):
                print(f" - {domain} - {Fore.LIGHTGREEN_EX}{Style.BRIGHT}Rentan (Shell Ditemukan){Style.RESET_ALL}")
                save_vulnerable_url(url)
                return

            # Cek pola kode berbahaya lainnya
            if b'"eval("' in content or b'"stat"' in content or b'"rrer","name"' in content or b"'eval'" in content:
                print(f" - {domain} - {Fore.LIGHTGREEN_EX}{Style.BRIGHT}Rentan (Pola Kode Berbahaya Ditemukan){Style.RESET_ALL}")
                save_vulnerable_url(url)
                return

            print(f" - {domain} - {Fore.LIGHTRED_EX}Tidak Rentan{Style.RESET_ALL}")
        except requests.RequestException:
            print(f" - {domain} - {Fore.LIGHTRED_EX}Tidak Dapat Diakses{Style.RESET_ALL}")

# Fungsi untuk menyimpan URL yang rentan
def save_vulnerable_url(url):
    # Pastikan direktori 'logs' ada untuk menyimpan log jika diperlukan
    os.makedirs("logs", exist_ok=True)
    with open("Shells.txt", "a", encoding="latin-1") as file:
        file.write(f"{url}\n")

# Fungsi untuk memuat daftar domain dari file
def load_domains(file_path):
    try:
        with open(file_path, "r", encoding="latin-1") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.LIGHTRED_EX}File tidak ditemukan: {file_path}{Style.RESET_ALL}")
        return []

# Fungsi untuk menampilkan laporan kerentanan
def display_vulnerability_report():
    try:
        with open("Shells.txt", "r", encoding="latin-1") as file:
            lines = file.readlines()
            if lines:
                print(f"\n{Fore.LIGHTGREEN_EX}Laporan:{Style.RESET_ALL}")
                print(f"{Fore.LIGHTWHITE_EX}Jumlah Shell Ditemukan: {len(lines)}{Style.RESET_ALL}")
                print("\n".join(line.strip() for line in lines))
            else:
                print(f"{Fore.LIGHTRED_EX}Tidak ada shell yang ditemukan.{Style.RESET_ALL}")
    except FileNotFoundError:
        print(f"{Fore.LIGHTRED_EX}Shells.txt tidak ditemukan. Belum ada shell yang tercatat.{Style.RESET_ALL}")

# Fungsi utama
def main():
    file_path = input(f"{Fore.LIGHTMAGENTA_EX}Masukkan path file yang berisi daftar domain:{Style.RESET_ALL} ")
    domain_list = load_domains(file_path)

    if not domain_list:
        print(f"{Fore.LIGHTRED_EX}Tidak ada domain untuk dipindai.{Style.RESET_ALL}")
        return

    print(f"{Fore.LIGHTBLUE_EX}Memulai pemindaian pada {len(domain_list)} domain...{Style.RESET_ALL}")

    # Gunakan ThreadPoolExecutor untuk pemindaian paralel
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(lambda domain: check_domain_vulnerability(domain, PATHS), domain_list)

    display_vulnerability_report()

# Jalankan program
if __name__ == "__main__":
    main()
