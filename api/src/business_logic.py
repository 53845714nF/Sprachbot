from datetime import date

# Own Modules
from data_access import (
    create_user,
    get_user,
    get_all_users,
    update_user,
    delete_user,
    search_user
)

def bl_create_user(data):
    geburtsdatum = None
    if data.get('geburtsdatum'):
        try:
            geburtsdatum = date.fromisoformat(data['geburtsdatum'])
        except ValueError:
            raise ValueError("Ungültiges Datumsformat für Geburtsdatum (YYYY-MM-DD)")

    return create_user(
        vorname=data['vorname'],
        nachname=data['nachname'],
        geburtsdatum=geburtsdatum,
        email=data.get('email'),
        telefonnummer=data.get('telefonnummer'),
        strasse=data.get('strasse'),
        hausnummer=data.get('hausnummer'),
        plz=data.get('plz'),
        ort=data.get('ort'),
        land=data.get('land')
    )

def bl_get_user(person_id):
    return get_user(person_id)

def bl_get_all_users():
    return get_all_users()

def bl_update_user(person_id, data):
    geburtsdatum = None
    if data.get('geburtsdatum'):
        try:
            geburtsdatum = date.fromisoformat(data['geburtsdatum'])
        except ValueError:
            raise ValueError("Ungültiges Datumsformat für Geburtsdatum (YYYY-MM-DD)")

    return update_user(
        user_id=person_id,
        vorname=data.get('vorname'),
        nachname=data.get('nachname'),
        geburtsdatum=geburtsdatum,
        email=data.get('email'),
        telefonnummer=data.get('telefonnummer'),
        strasse=data.get('strasse'),
        hausnummer=data.get('hausnummer'),
        plz=data.get('plz'),
        ort=data.get('ort'),
        land=data.get('land')
    )

def bl_delete_user(person_id):
    return delete_user(person_id)


def bl_search_user(query):
    if query == None:
        raise ValueError("Leere Suche")
    
    return search_user(query)