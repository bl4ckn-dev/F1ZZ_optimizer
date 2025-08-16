import os
import subprocess
import psutil
import requests
import ctypes
import pyfiglet
import json
import webbrowser
from colorama import Fore, init

init(autoreset=True)

# ============================
# Banner estilizado
# ============================
def banner():
    ascii_banner = pyfiglet.figlet_format("F1ZZ")
    print(Fore.CYAN + ascii_banner)

# ============================
# Monitoramento de performance
# ============================
def monitorar_performance():
    print(Fore.YELLOW + "\n[ Monitoramento de Performance em Tempo Real ]")
    print(f"CPU: {psutil.cpu_percent()}%")
    print(f"RAM: {psutil.virtual_memory().percent}%")
    print(f"Disco: {psutil.disk_usage('/').percent}%")

# ============================
# Limpeza inteligente de cache
# ============================
def limpar_cache():
    print(Fore.YELLOW + "\n[✔] Limpando caches temporários...")

    pastas = [
        os.environ.get("TEMP"),
        os.path.expanduser("~\\AppData\\Local\\Temp")
    ]

    total_arquivos = 0
    for pasta in pastas:
        if pasta and os.path.exists(pasta):
            for root, dirs, files in os.walk(pasta):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                        total_arquivos += 1
                    except:
                        pass
    print(Fore.GREEN + f"[✔] {total_arquivos} arquivos de cache removidos com sucesso.")

# ============================
# Otimizar inicialização
# ============================
def otimizar_inicializacao():
    print(Fore.YELLOW + "\n[✔] Desativando programas de inicialização desnecessários...")
    subprocess.run("wmic startup where 'not name like \"%Windows%\"' call disable", shell=True)
    print(Fore.GREEN + "[✔] Programas de inicialização desnecessários desativados!")

# ============================
# Serviços guiados com backup
# ============================
SERVICOS = {
    "Cortana": {"reg": r'HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search', "valor": "AllowCortana", "tipo": "REG_DWORD", "desativar": 0},
    "Telemetria": {"sc": "DiagTrack"},
    "dmwappushservice": {"sc": "dmwappushservice"},
    "Windows Search": {"sc": "WSearch"},
    "Print Spooler": {"sc": "Spooler"}
}
BACKUP_FILE = "servicos_backup.json"

def backup_servicos():
    backup = {}
    for nome, dados in SERVICOS.items():
        if "reg" in dados:
            try:
                resultado = subprocess.check_output(f'reg query "{dados["reg"]}" /v {dados["valor"]}', shell=True).decode()
                valor_atual = int(resultado.strip().split()[-1], 16)
                backup[nome] = {"valor": valor_atual}
            except:
                backup[nome] = {"valor": None}
        elif "sc" in dados:
            try:
                resultado = subprocess.check_output(f'sc query {dados["sc"]}', shell=True).decode()
                status = "RUNNING" if "RUNNING" in resultado else "STOPPED"
                backup[nome] = {"status": status}
            except:
                backup[nome] = {"status": None}
    with open(BACKUP_FILE, "w") as f:
        json.dump(backup, f, indent=4)
    print(Fore.GREEN + "[✔] Backup dos serviços concluído!")

def restaurar_servicos():
    if not os.path.exists(BACKUP_FILE):
        print(Fore.RED + "[x] Nenhum backup encontrado!")
        return
    with open(BACKUP_FILE, "r") as f:
        backup = json.load(f)
    for nome, dados in SERVICOS.items():
        if "reg" in dados:
            valor_antigo = backup.get(nome, {}).get("valor")
            if valor_antigo is not None:
                subprocess.run(f'reg add "{dados["reg"]}" /v {dados["valor"]} /t {dados["tipo"]} /d {valor_antigo} /f', shell=True)
        elif "sc" in dados:
            status_antigo = backup.get(nome, {}).get("status")
            if status_antigo == "RUNNING":
                subprocess.run(f'sc start {dados["sc"]}', shell=True)
            elif status_antigo == "STOPPED":
                subprocess.run(f'sc stop {dados["sc"]}', shell=True)
    print(Fore.GREEN + "[✔] Serviços restaurados a partir do backup!")

def otimizar_servicos_guiado():
    print(Fore.YELLOW + "\n[ Otimização Guiada de Serviços ]")
    backup_servicos()
    print(Fore.CYAN + "\nSelecione os serviços que deseja desativar:")
    for i, nome in enumerate(SERVICOS.keys(), start=1):
        print(f"{i} - {nome}")
    selecionados = input("\nDigite os números separados por vírgula (ex: 1,3): ")
    selecionados = [int(x.strip()) for x in selecionados.split(",") if x.strip().isdigit()]
    for i in selecionados:
        nome = list(SERVICOS.keys())[i-1]
        dados = SERVICOS[nome]
        if "reg" in dados:
            subprocess.run(f'reg add "{dados["reg"]}" /v {dados["valor"]} /t {dados["tipo"]} /d {dados["desativar"]} /f', shell=True)
        elif "sc" in dados:
            subprocess.run(f'sc stop {dados["sc"]}', shell=True)
    print(Fore.GREEN + "[✔] Serviços selecionados desativados com sucesso!")

# ============================
# Otimização automática completa
# ============================
def otimizar_servicos_automatico_completo():
    print(Fore.YELLOW + "\n[✔] Iniciando Otimização Automática Completa...")

    # Backup dos serviços
    backup_servicos()

    # Desativar serviços opcionais
    print(Fore.YELLOW + "\n[✔] Desativando serviços opcionais...")
    comandos_servicos = [
        r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search" /v AllowCortana /t REG_DWORD /d 0 /f',
        r'sc stop DiagTrack',
        r'sc config DiagTrack start=disabled',
        r'sc stop dmwappushservice',
        r'sc config dmwappushservice start=disabled'
    ]
    for cmd in comandos_servicos:
        subprocess.run(cmd, shell=True)
    print(Fore.GREEN + "[✔] Serviços opcionais desativados.")

    # Desativar efeitos visuais
    print(Fore.YELLOW + "\n[✔] Desativando efeitos visuais para melhor desempenho...")
    try:
        subprocess.run(
            r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f',
            shell=True
        )
        tweaks = [
            r'reg add "HKCU\Control Panel\Desktop" /v UserPreferencesMask /t REG_BINARY /d 9012008010000000 /f',
            r'reg add "HKCU\Control Panel\Desktop\WindowMetrics" /v MinAnimate /t REG_SZ /d 0 /f'
        ]
        for t in tweaks:
            subprocess.run(t, shell=True)
        print(Fore.GREEN + "[✔] Efeitos visuais desativados.")
    except Exception as e:
        print(Fore.RED + f"[x] Erro ao desativar efeitos visuais: {e}")

    # Perguntar sobre reinício
    resposta = ctypes.windll.user32.MessageBoxW(
        0,
        "Otimização completa realizada.\n\nDeseja reiniciar agora para aplicar as mudanças?",
        "F1ZZ Optimizer",
        1
    )
    if resposta == 1:
        print(Fore.RED + "[!] Reiniciando o computador em 10 segundos...")
        subprocess.run("shutdown /r /t 10", shell=True)
    else:
        print(Fore.YELLOW + "[!] Reinício cancelado. Mudanças serão aplicadas na próxima reinicialização.")

# ============================
# Download de apps
# ============================
def baixar_app(nome, url):
    try:
        print(Fore.YELLOW + f"\n[*] Baixando {nome}...")
        r = requests.get(url, stream=True)
        file_path = os.path.join(os.getcwd(), f"{nome}.exe")
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        print(Fore.GREEN + f"[✔] {nome} baixado com sucesso em {file_path}")
    except Exception as e:
        print(Fore.RED + f"[x] Erro ao baixar {nome}: {e}")

# ============================
# Menu principal
# ============================
def menu():
    while True:
        os.system("cls")
        banner()
        titulo = "=== MENU F1ZZ OPTIMIZER ==="
        print(Fore.CYAN + titulo.center(70))
        print(Fore.BLUE + "="*70)

        col_esquerda = [
            "1 - Monitorar Performance",
            "2 - Limpeza Inteligente de Cache",
            "3 - Otimizar Inicialização",
            "4 - Otimização Automática Completa",
            "5 - Otimizar Serviços (Guiado)"
        ]
        col_direita = [
            "6 - Baixar Brave",
            "7 - Baixar Firefox",
            "8 - Baixar Opera",
            "9 - Baixar 7-Zip",
            "10 - Baixar Spotify",
            "11 - Baixar Discord"
        ]

        max_linhas = max(len(col_esquerda), len(col_direita))
        for i in range(max_linhas):
            esquerda = col_esquerda[i] if i < len(col_esquerda) else ""
            direita = col_direita[i] if i < len(col_direita) else ""
            print(f"{Fore.BLUE}{esquerda.ljust(40)}{Fore.BLUE}{direita}")

        print(Fore.RED + "0 - Sair".center(70))
        print(Fore.BLUE + "="*70)

        opc = input(Fore.CYAN + "\nEscolha uma opção: ")

        if opc == "1":
            monitorar_performance()
        elif opc == "2":
            limpar_cache()
        elif opc == "3":
            otimizar_inicializacao()
        elif opc == "4":
            otimizar_servicos_automatico_completo()
        elif opc == "5":
            while True:
                print(Fore.YELLOW + "\n[ Serviços Guiados ]")
                print("1 - Desativar serviços selecionados")
                print("2 - Restaurar serviços do backup")
                print("0 - Voltar ao menu")
                sub = input("\nEscolha uma opção: ")
                if sub == "1":
                    otimizar_servicos_guiado()
                elif sub == "2":
                    restaurar_servicos()
                elif sub == "0":
                    break
                else:
                    print(Fore.RED + "[!] Opção inválida!")
        elif opc == "6":
            baixar_app("Brave", "https://laptop-updates.brave.com/latest/winx64")
        elif opc == "7":
            baixar_app("Firefox", "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=pt-BR")
        elif opc == "8":
            baixar_app("Opera", "https://net.geo.opera.com/opera/stable/windows")
        elif opc == "9":
            baixar_app("7-Zip", "https://www.7-zip.org/a/7z1900-x64.exe")
        elif opc == "10":
            baixar_app("Spotify", "https://download.scdn.co/SpotifySetup.exe")
        elif opc == "11":
            baixar_app("Discord", "https://discord.com/api/download?platform=win")
        elif opc == "0":
            print(Fore.RED + "\nSaindo do F1ZZ Optimizer...")

            # Pop-up informativo
            ctypes.windll.user32.MessageBoxW(
                0,
                "Obrigado por usar o F1ZZ Optimizer!\n\n"
                "Você será redirecionado para nosso servidor do Discord para atualizações\n"
                "e acesso a pacotes de otimização para PC e jogos.",
                "F1ZZ Optimizer",
                0
            )

            # Abrir o Discord no navegador
            webbrowser.open("https://discord.gg/YVM3PXuz")
            break
        else:
            print(Fore.RED + "\n[!] Opção inválida!")

        input(Fore.CYAN + "\nPressione ENTER para voltar ao menu...")

# ============================
# Início do programa
# ============================
if __name__ == "__main__":
    menu()
