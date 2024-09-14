# Umbralix BlackOps

Umbralix BlackOps es una herramienta poderosa para la auditoría de redes y la seguridad. Incluye capacidades como escaneo de puertos, ataques de fuerza bruta, y explotación de vulnerabilidades con Metasploit.

## Características
- Escaneo de redes WiFi con `netdiscover` o en modo monitor.
- Escaneo de puertos abiertos con `nmap`.
- Ataques de fuerza bruta con `hydra` en servicios como SSH, HTTP y FTP.
- Explotación de vulnerabilidades con Metasploit.

## Instalación

### Requisitos:
Asegúrate de tener instaladas las siguientes herramientas:
- `nmap`
- `hydra`
- `netdiscover`
- `metasploit`
- `aircrack-ng`

### Instalación en sistemas Debian/Ubuntu:
```bash
sudo apt-get update
sudo apt-get install nmap hydra netdiscover aircrack-ng metasploit-framework
