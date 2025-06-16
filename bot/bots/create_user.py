from requests import post
from json import dumps
from config import DefaultConfig

config = DefaultConfig()
api = config.API_URL

headers = {
    "Content-Type": "application/json"
}


def create_user(vorname, nachname, geburtsdatum, email, telefonnummer, strasse, hausnummer, plz, ort, land):
    
    user_data = {
        "vorname": vorname,
        "nachname": nachname,
        "geburtsdatum": geburtsdatum,
        "email": email,
        "telefonnummer": telefonnummer,
        "strasse": strasse,
        "hausnummer": hausnummer,
        "plz": plz,
        "ort": ort,
        "land": land
    }

    try:
        response = post(f"{api}/api/user", headers=headers, data=dumps(user_data))
        print(response.text)
        return response.text
    except ConnectionError as e:
        return f"Verbindungsfehler: Konnte den Server unter {api} nicht erreichen."