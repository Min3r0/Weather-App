import argparse
import json
import urllib.request
import urllib.error
from datetime import datetime
from typing import List, Dict, Any
from collections import defaultdict


def fetch_weather(url) -> dict:
    """Appelle l'API Open-Meteo pour récupérer la météo actuelle et retourne le JSON."""
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            if resp.status != 200:
                raise urllib.error.HTTPError(url, resp.status, resp.reason, resp.headers, None)
            data = json.load(resp)
            return data
    except Exception as e:
        raise RuntimeError(f"Erreur lors de l'appel API: {e}")


def extract_readings(data: Any) -> List[Dict[str, Any]]:
    """Normalise différentes structures JSON en une liste de 'readings' contenant les clés attendues."""
    readings: List[Dict[str, Any]] = []

    if isinstance(data, list):
        readings = data
    elif isinstance(data, dict):
        if "records" in data and isinstance(data["records"], list):
            for rec in data["records"]:
                if isinstance(rec, dict) and "fields" in rec and isinstance(rec["fields"], dict):
                    readings.append(rec["fields"])
                else:
                    readings.append(rec)
        elif "results" in data and isinstance(data["results"], list):
            readings = data["results"]
        elif "data" in data and isinstance(data["data"], list):
            readings = data["data"]
        elif "items" in data and isinstance(data["items"], list):
            readings = data["items"]
        else:
            readings = [data]

    return readings


def parse_datetime(iso_str: str) -> datetime:
    """Parse une chaîne ISO en objet datetime."""
    try:
        return datetime.fromisoformat(iso_str)
    except Exception:
        return None


def normalize_pressure(p: Any) -> str:
    """Normalise la pression : si grande valeur (ex 99600) on suppose Pa et on convertit en hPa."""
    try:
        val = float(p)
        if val > 2000:
            return f"{val / 100:.1f}"
        return f"{val:.1f}"
    except Exception:
        return str(p)


def is_missing_value(key: str, value: Any) -> bool:
    """Retourne True si la valeur correspond à un marqueur 'non fourni' selon la clé."""
    if value is None:
        return True
    try:
        if key in ("humidite", "humidity", "hum"):
            v = int(value)
            return v == 0 or not (0 <= v <= 100)
        if key in ("temperature_en_degre_c", "temperature", "temp_c", "temp"):
            v = float(value)
            return v <= -50 or v < -100 or v > 60
        if key in ("pression", "pressure", "press"):
            v = float(value)
            return v <= 0
    except Exception:
        return False
    return False


def format_value(key: str, value: Any) -> str:
    """Formate une valeur pour l'affichage."""
    if is_missing_value(key, value):
        return "N/A"

    try:
        if "temp" in key.lower():
            return f"{float(value):.1f}°C"
        elif "hum" in key.lower():
            return f"{int(value)}%"
        elif "press" in key.lower():
            return f"{normalize_pressure(value)}hPa"
    except Exception:
        pass
    return str(value)


def print_readings_horizontal(data: Any, limit: int = 10) -> None:
    """Affiche les lectures de manière horizontale, regroupées par jour."""
    if isinstance(data, dict) and "total_count" in data:
        try:
            print(f"Total count: {int(data['total_count'])}\n")
        except Exception:
            print(f"Total count: {data['total_count']}\n")

    readings = extract_readings(data)
    if not readings:
        print("Aucune lecture trouvée dans la réponse. Réponse brute :")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return

    # Regrouper par jour
    by_day = defaultdict(list)

    for r in readings[:limit]:
        time_raw = r.get("heure_de_paris") or r.get("time") or r.get("date") or r.get("datetime") or r.get("timestamp")
        if time_raw:
            dt = parse_datetime(time_raw)
            if dt:
                day_key = dt.strftime("%Y-%m-%d")
                by_day[day_key].append({
                    "datetime": dt,
                    "temp": r.get("temperature_en_degre_c") or r.get("temperature") or r.get("temp_c") or r.get("temp"),
                    "humid": r.get("humidite") or r.get("humidity") or r.get("hum"),
                    "pres": r.get("pression") or r.get("pressure") or r.get("press")
                })

    # Afficher par jour
    for day in sorted(by_day.keys(), reverse=True):
        entries = sorted(by_day[day], key=lambda x: x["datetime"])  # Tri croissant par heure

        # Formater la date en dd/mm/yyyy
        date_obj = datetime.strptime(day, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d/%m/%Y")

        print(f"{'=' * 80}")
        print(f"DATE: {formatted_date}")
        print(f"{'=' * 80}")

        # Ligne des heures
        hours = [e["datetime"].strftime("%H:%M") for e in entries]
        print(f"{'Heure':<15} " + " ".join(f"{h:>12}" for h in hours))

        # Ligne des températures
        temps = [format_value("temperature", e["temp"]) for e in entries]
        print(f"{'Température':<15} " + " ".join(f"{t:>12}" for t in temps))

        # Ligne des pressions
        press = [format_value("pression", e["pres"]) for e in entries]
        print(f"{'Pression':<15} " + " ".join(f"{p:>12}" for p in press))

        # Ligne des humidités
        hums = [format_value("humidite", e["humid"]) for e in entries]
        print(f"{'Humidité':<15} " + " ".join(f"{h:>12}" for h in hums))

        print()


def main(url, limit: int = 10):
    try:
        data = fetch_weather(url)
        print_readings_horizontal(data, limit=limit)
    except RuntimeError as e:
        print(e)


url = "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/42-station-meteo-toulouse-parc-compans-cafarelli/records?select=heure_de_paris%2C%20humidite%2C%20temperature_en_degre_c%2C%20pression&order_by=heure_de_paris%20DESC&limit=100"
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Récupère et affiche des lectures météo.")
    parser.add_argument("--url", "-u", default=url, help="URL de l'API")
    parser.add_argument("--limit", "-n", type=int, default=1000, help="Nombre d'entrées à afficher")
    args = parser.parse_args()
    main(args.url, limit=args.limit)