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
    # To simulate business logic, 
    # checks whether the date of birth is a real date in ISO format
    geburtsdatum = None
    if data.get("geburtsdatum"):
        try:
            geburtsdatum = date.fromisoformat(data["geburtsdatum"])
        except ValueError:
            raise ValueError("Ungültiges Datumsformat für Geburtsdatum (YYYY-MM-DD)")

    return create_user(
        vorname=data["vorname"],
        nachname=data["nachname"],
        geburtsdatum=geburtsdatum,
        email=data.get("email"),
        telefonnummer=data.get("telefonnummer"),
        strasse=data.get("strasse"),
        hausnummer=data.get("hausnummer"),
        plz=data.get("plz"),
        ort=data.get("ort"),
        land=data.get("land")
    )

def bl_get_user(person_id):
    # No real business logic as only get user
    return get_user(person_id)

def bl_get_all_users():
    # No real business logic as only get all users
    return get_all_users()

def bl_update_user(person_id, data):
    # To simulate business logic, 
    # checks whether the date of birth is a real date in ISO format
    geburtsdatum = None
    if data.get("geburtsdatum"):
        try:
            geburtsdatum = date.fromisoformat(data["geburtsdatum"])
        except ValueError:
            raise ValueError("Ungültiges Datumsformat für Geburtsdatum (YYYY-MM-DD)")

    return update_user(
        user_id=person_id,
        vorname=data.get("vorname"),
        nachname=data.get("nachname"),
        geburtsdatum=geburtsdatum,
        email=data.get("email"),
        telefonnummer=data.get("telefonnummer"),
        strasse=data.get("strasse"),
        hausnummer=data.get("hausnummer"),
        plz=data.get("plz"),
        ort=data.get("ort"),
        land=data.get("land")
    )

def bl_delete_user(person_id):
    # No real business logic as only user will be deleted
    return delete_user(person_id)


def bl_search_user(vorname=None, nachname=None, email=None, telefonnummer=None, strasse=None, ort=None, land=None, plz=None):
    # To simulate business logic, 
    # the system checks again whether at least one of the following criteria is filled
    if all(arg is None for arg in [vorname, nachname, email, telefonnummer, strasse, ort, land, plz]):
        raise ValueError("At least one search criterion must be specified.")
    
    return search_user(
        vorname=vorname,
        nachname=nachname,
        telefonnummer=telefonnummer,
        strasse=strasse,
        ort=ort,
        land=land,
        plz=plz
        )
