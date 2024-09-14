import os
import subprocess
import time
import pyfiglet

# Definir los códigos de color ANSI
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Mostrar título en ASCII con tu apodo
def show_title():
    title = pyfiglet.figlet_format("Made by Umbralix UmbralixBlackOps", width=100, font="slant")
    print(f"{RED}{title}{RESET}")
    
# Disclaimer legal
def show_disclaimer():
    disclaimer_text = """
    ************************************************************
    *                                                          *
    *  AVISO LEGAL: Este programa está diseñado exclusivamente  *
    *  para fines educativos y de auditoría ética de seguridad. *
    *  El uso indebido de estas herramientas es ilegal y puede  *
    *  tener consecuencias graves. Solo debes utilizarlo en tus *
    *  propias redes o con permiso expreso del propietario.     *
    *                                                          *
    ************************************************************
    """
    print(f"{RED}{disclaimer_text}{RESET}")
    input("Presiona Enter para continuar...")

# Verificar si tenemos privilegios de root
def check_root_privileges():
    if os.geteuid() != 0:
        print(f"{RED}Este escaneo requiere privilegios de root. Por favor, ejecuta el script como root.{RESET}")
        exit(1)

# Verificar si una herramienta está instalada
def check_tool_installed(tool):
    result = subprocess.run(["which", tool], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"{RED}La herramienta '{tool}' no está instalada. Por favor, instálala antes de continuar.{RESET}")
        return False
    return True

# Escanear redes WiFi o usar netdiscover
def scan_wifi_networks():
    if not check_tool_installed("netdiscover"):
        return
    choice = input(f"{YELLOW}¿Quieres activar el modo monitor para escanear redes WiFi? (s/n): {RESET}").lower()
    if choice == 's':
        # Cambiar a modo monitor antes del escaneo
        print(f"{CYAN}Verificando si wlp3s0 está en modo monitor...{RESET}")
        result = subprocess.run(["iwconfig", "wlp3s0"], capture_output=True, text=True)
        
        if "Mode:Monitor" not in result.stdout:
            print(f"{YELLOW}La interfaz wlp3s0 no está en modo monitor. Habilitando modo monitor...{RESET}")
            subprocess.run(["airmon-ng", "start", "wlp3s0"], check=True)
        
        print(f"{CYAN}Escaneando redes WiFi...{RESET}")
        time.sleep(2)
        try:
            subprocess.run(["iwlist", "wlp3s0", "scan"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"{RED}Error al escanear redes: {e}{RESET}")
    else:
        # Usar netdiscover si no se activa el modo monitor
        print(f"{CYAN}Usando netdiscover para escanear la red...{RESET}")
        time.sleep(2)
        try:
            subprocess.run(["netdiscover", "-i", "wlp3s0", "-r", "192.168.1.0/24"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"{RED}Error al usar netdiscover: {e}{RESET}")

# Escanear puertos con Nmap
def scan_ports_nmap():
    if not check_tool_installed("nmap"):
        return
    target_ip = input(f"{YELLOW}Ingresa la IP del objetivo para escanear puertos: {RESET}")
    print(f"{GREEN}Escaneando puertos en {target_ip}...{RESET}")
    try:
        subprocess.run(["nmap", "-sV", target_ip], check=True)
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error al escanear puertos: {e}{RESET}")

# Enumerar servicios con Nmap
def enumerate_services_nmap():
    if not check_tool_installed("nmap"):
        return
    target_ip = input(f"{YELLOW}Ingresa la IP del objetivo para enumerar servicios: {RESET}")
    print(f"{GREEN}Enumerando servicios en {target_ip}...{RESET}")
    try:
        subprocess.run(["nmap", "-sC", "-sV", target_ip], check=True)
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error al enumerar servicios: {e}{RESET}")

# Ataques de fuerza bruta con Hydra
def brute_force_hydra():
    if not check_tool_installed("hydra"):
        return
    target_ip = input(f"{YELLOW}Ingresa la IP del objetivo para ataque de fuerza bruta: {RESET}")
    service = input(f"{YELLOW}Selecciona el servicio para el ataque (ssh/http/ftp): {RESET}")
    username = input(f"{YELLOW}Ingresa el nombre de usuario: {RESET}")
    wordlist = input(f"{YELLOW}Ingresa la ruta a la lista de contraseñas: {RESET}")
    
    if service == "ssh":
        print(f"{GREEN}Iniciando ataque de fuerza bruta SSH en {target_ip}...{RESET}")
        subprocess.run(["hydra", "-l", username, "-P", wordlist, f"ssh://{target_ip}"], check=True)
    elif service == "http":
        print(f"{GREEN}Iniciando ataque de fuerza bruta HTTP en {target_ip}...{RESET}")
        subprocess.run(["hydra", "-l", username, "-P", wordlist, f"http-get://{target_ip}"], check=True)
    elif service == "ftp":
        print(f"{GREEN}Iniciando ataque de fuerza bruta FTP en {target_ip}...{RESET}")
        subprocess.run(["hydra", "-l", username, "-P", wordlist, f"ftp://{target_ip}"], check=True)
    else:
        print(f"{RED}Servicio no válido. Por favor, selecciona ssh, http, o ftp.{RESET}")

# Menú de Metasploit
def metasploit_menu():
    while True:
        print(f"""
        {MAGENTA}***********************************************{RESET}
        {CYAN}Menú de Metasploit{RESET}
        {MAGENTA}***********************************************{RESET}
        1. {YELLOW}Buscar exploits por servicio{RESET}
        2. {YELLOW}Ejecutar un exploit específico{RESET}
        3. {YELLOW}Listar todos los exploits{RESET}
        4. {YELLOW}Regresar al menú principal{RESET}
        """)
        metasploit_choice = input(f"{BLUE}Elige una opción: {RESET}")
        
        if metasploit_choice == '1':
            search_exploits_metasploit()
        elif metasploit_choice == '2':
            run_specific_exploit_metasploit()
        elif metasploit_choice == '3':
            list_all_exploits_metasploit()
        elif metasploit_choice == '4':
            break
        else:
            print(f"{RED}Opción no válida. Por favor, elige una opción correcta.{RESET}")

# Buscar exploits por servicio
def search_exploits_metasploit():
    if not check_tool_installed("msfconsole"):
        return
    service_name = input(f"{YELLOW}Ingresa el nombre del servicio a buscar exploits: {RESET}")
    print(f"{GREEN}Buscando exploits para {service_name}...{RESET}")
    subprocess.run(["msfconsole", "-x", f"search {service_name}; exit"], check=True)

# Ejecutar un exploit específico
def run_specific_exploit_metasploit():
    if not check_tool_installed("msfconsole"):
        return
    target_ip = input(f"{YELLOW}Ingresa la IP del objetivo para explotación: {RESET}")
    exploit_module = input(f"{YELLOW}Ingresa el módulo de exploit que quieres usar (e.g., exploit/windows/smb/ms17_010_eternalblue): {RESET}")
    print(f"{GREEN}Iniciando exploit {exploit_module} contra {target_ip}...{RESET}")
    subprocess.run(["msfconsole", "-x", f"use {exploit_module}; set RHOST {target_ip}; run"], check=True)

# Listar todos los exploits
def list_all_exploits_metasploit():
    if not check_tool_installed("msfconsole"):
        return
    print(f"{GREEN}Listando todos los exploits disponibles en Metasploit...{RESET}")
    subprocess.run(["msfconsole", "-x", "show exploits; exit"], check=True)

# Habilitar modo monitor
def monitor_mode():
    if not check_tool_installed("airmon-ng"):
        return
    print(f"{CYAN}Habilitando modo monitor...{RESET}")
    subprocess.run(["airmon-ng", "start", "wlp3s0"], check=True)

# Deshabilitar modo monitor
def disable_monitor_mode():
    if not check_tool_installed("airmon-ng"):
        return
    print(f"{CYAN}Deshabilitando modo monitor...{RESET}")
    subprocess.run(["airmon-ng", "stop", "wlp3s0"], check=True)

# Guardar log de acciones
def log_action(action):
    with open("wifi_attack_log.txt", "a") as log_file:
        log_file.write(f"[{time.ctime()}] {action}\n")

# Función principal del menú
def main():
    show_disclaimer()
    check_root_privileges()
    show_title()
    while True:
        print(f"""
        {MAGENTA}***********************************************{RESET}
        {CYAN}Menú - Aplicación de Hacking WiFi{RESET}
        {MAGENTA}***********************************************{RESET}
        1. {YELLOW}Escanear redes WiFi / Usar netdiscover{RESET}
        2. {YELLOW}Escanear puertos con Nmap{RESET}
        3. {YELLOW}Enumerar servicios con Nmap{RESET}
        4. {YELLOW}Ataque de fuerza bruta con Hydra{RESET}
        5. {YELLOW}Explotación con Metasploit{RESET}
        6. {YELLOW}Habilitar modo monitor{RESET}
        7. {YELLOW}Deshabilitar modo monitor{RESET}
        8. {YELLOW}Salir{RESET}
        """)
        choice = input(f"{BLUE}Elige una opción: {RESET}")
        
        if choice == '1':
            scan_wifi_networks()
            log_action("Escaneo de redes WiFi o uso de netdiscover realizado")
        elif choice == '2':
            scan_ports_nmap()
            log_action("Escaneo de puertos realizado")
        elif choice == '3':
            enumerate_services_nmap()
            log_action("Enumeración de servicios realizada")
        elif choice == '4':
            brute_force_hydra()
            log_action("Ataque de fuerza bruta realizado")
        elif choice == '5':
            metasploit_menu()
            log_action("Se abrió el menú de Metasploit")
        elif choice == '6':
            monitor_mode()
            log_action("Modo monitor habilitado")
        elif choice == '7':
            disable_monitor_mode()
            log_action("Modo monitor deshabilitado")
        elif choice == '8':
            print(f"{GREEN}Saliendo del programa...{RESET}")
            log_action("Programa cerrado")
            break
        else:
            print(f"{RED}Opción no válida. Por favor, elige una opción correcta.{RESET}")

if __name__ == "__main__":
    main()
