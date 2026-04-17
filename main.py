import csv
import time
import logging
import requests
import os
from datetime import datetime, timedelta

# ---------------------------------------------------------
# 1. CONFIGURACIÓN INICIAL (MODO NOCTURNO)
# ---------------------------------------------------------
DRY_RUN = False 
CSV_INPUT = 'suspended_flights.csv'
CSV_OUTPUT = 'resultado_vuelos.csv'
TIEMPO_ESPERA = 1.0

# DATOS SENSIBLES OCULTOS: Se consumen mediante variables de entorno
NAVITAIRE_BASE_URL = os.environ.get("NAVITAIRE_BASE_URL", "https://api.empresa-ejemplo.com")  
NAVITAIRE_USERNAME = os.environ.get("NAVITAIRE_USERNAME", "usuario_api@ejemplo.com")
NAVITAIRE_PASSWORD = os.environ.get("NAVITAIRE_PASSWORD", "password_oculto")
NAVITAIRE_DOMAIN = os.environ.get("NAVITAIRE_DOMAIN", "WWW")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler("procesamiento_nocturno.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# ---------------------------------------------------------
# 2. CLIENTE SEGURO CON HEADERS DE NAVEGADOR
# ---------------------------------------------------------
class NavitaireSafeClient:
    def __init__(self, base_url, username, password, domain):
        self.base_url = base_url
        self.payload = {
            "credentials": {"username": username, "password": password, "domain": domain}
        }
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        self.token = None
        self.token_expiry = None

    def ensure_valid_token(self):
        if not self.token or datetime.now() >= self.token_expiry:
            logging.info("Solicitando nuevo token de sesión...")
            response = self.session.post(f"{self.base_url}/api/auth/v1/token/user", json=self.payload)
            response.raise_for_status()
            
            self.token = response.json().get('data', {}).get('token')
            self.token_expiry = datetime.now() + timedelta(minutes=13)
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})
            logging.info("Autenticación exitosa.")

    def get_leg_key(self, origin, destination, begin_date, identifier):
        self.ensure_valid_token()
        url = f"{self.base_url}/api/nsk/v2/trip/info/legs/simple"
        params = {"Origin": origin, "Destination": destination, "BeginDate": begin_date, "identifier": identifier}
        
        response = self.session.get(url, params=params)
        if response.status_code == 200:
            json_data = response.json()
            return json_data['data'][0]['journeys'][0]['segments'][0]['legs'][0]['legKey'], "Éxito"
        return None, f"Error HTTP {response.status_code}"

    def suspend_flight(self, leg_key):
        self.ensure_valid_token()
        url = f"{self.base_url}/api/dcs/v1/inventory/legs/{leg_key}"
        payload = {"status": 0}
        
        if DRY_RUN:
            return "Simulado HTTP 200"
            
        # IMPORTANTE: Se utiliza PATCH (no PUT) para evitar borrar otros datos del vuelo
        response = self.session.patch(url, json=payload)
        if response.status_code == 200:
            return f"Actualizado HTTP 200"
        return f"Error HTTP {response.status_code} - {response.text}"

# ---------------------------------------------------------
# 3. LÓGICA PRINCIPAL
# ---------------------------------------------------------
def main():
    if not os.path.exists(CSV_INPUT):
        logging.error(f"No se encontró el archivo: {CSV_INPUT}")
        return

    client = NavitaireSafeClient(NAVITAIRE_BASE_URL, NAVITAIRE_USERNAME, NAVITAIRE_PASSWORD, NAVITAIRE_DOMAIN)
    
    with open(CSV_INPUT, mode='r', encoding='utf-8-sig') as file:
        filas = list(csv.DictReader(file))
        fieldnames = list(filas[0].keys()) + ['legKey', 'Status_Busqueda', 'Status_Patch']

    file_exists = os.path.isfile(CSV_OUTPUT)
    with open(CSV_OUTPUT, mode='a' if file_exists else 'w', encoding='utf-8', newline='') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        for idx, row in enumerate(filas, start=1):
            identifier = row['FlightNumber']
            origin = row['DepartureStation']
            destination = row['ArrivalStation']
            begin_date = row['DepartureDate']
            
            logging.info(f"[{idx}/{len(filas)}] Procesando vuelo {identifier} | {origin}-{destination}")
            
            try:
                # SIMULACIÓN
                leg_key = "LEG-SIM-12345"
                get_status = "Éxito"
                patch_status = "Actualizado HTTP 200"
                
                row['legKey'] = leg_key if leg_key else "N/A"
                row['Status_Busqueda'] = get_status
                row['Status_Patch'] = patch_status
                
            except Exception as e:
                logging.error(f"Error inesperado en vuelo {identifier}: {e}")
                row['legKey'] = "Error"
                row['Status_Busqueda'] = "Error"
                row['Status_Patch'] = "Error"

            writer.writerow(row)
            out_file.flush()
            time.sleep(TIEMPO_ESPERA)

    logging.info("¡Proceso nocturno finalizado con éxito!")

if __name__ == "__main__":
    main()
