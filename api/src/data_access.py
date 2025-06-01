# Third-party modules
from sqlalchemy import or_

# Own modules
from database import db
from models import Person, Kontakt, Adresse

def create_user(vorname, nachname, geburtsdatum, email, telefonnummer, strasse, hausnummer, plz, ort, land):
    user = Person(vorname=vorname, nachname=nachname, geburtsdatum=geburtsdatum)
    kontakt = Kontakt(email=email, telefonnummer=telefonnummer, person=user)
    adresse = Adresse(strasse=strasse, hausnummer=hausnummer, plz=plz, ort=ort, land=land, person=user)
    db.session.add(user)
    db.session.commit()
    return user.id

def get_user(user_id):
    return db.session.get(Person, user_id)

def get_all_users():
    return Person.query.all()

def update_user(user_id, vorname=None, nachname=None, geburtsdatum=None, email=None, telefonnummer=None, strasse=None, hausnummer=None, plz=None, ort=None, land=None):
    user = get_user(user_id)
    if not user:
        return None

    if vorname is not None:
        user.vorname = vorname
    if nachname is not None:
        user.nachname = nachname
    if geburtsdatum is not None:
        user.geburtsdatum = geburtsdatum

    if user.kontakt:
        if email is not None:
            user.kontakt.email = email
        if telefonnummer is not None:
            user.kontakt.telefonnummer = telefonnummer
    else:
        user.kontakt = Kontakt(email=email, telefonnummer=telefonnummer, person=user)

    if user.adresse:
        if strasse is not None:
            user.adresse.strasse = strasse
        if hausnummer is not None:
            user.adresse.hausnummer = hausnummer
        if plz is not None:
            user.adresse.plz = plz
        if ort is not None:
            user.adresse.ort = ort
        if land is not None:
            user.adresse.land = land
    else:
        user.adresse = Adresse(strasse=strasse, hausnummer=hausnummer, plz=plz, ort=ort, land=land, person=user)

    db.session.commit()
    return user

def delete_user(user_id):
    user = get_user(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

def search_user(vorname=None, nachname=None, email=None, telefonnummer=None, strasse=None, ort=None, land=None, plz=None):
    filters = []

    if vorname:
        filters.append(Person.vorname.ilike(f"%{vorname}%"))
    if nachname:
        filters.append(Person.nachname.ilike(f"%{nachname}%"))

    if email or telefonnummer:
        kontakt_filters = []
        if email:
            kontakt_filters.append(Kontakt.email.ilike(f"%{email}%"))
        if telefonnummer:
            kontakt_filters.append(Kontakt.telefonnummer.ilike(f"%{telefonnummer}%"))
        filters.append(Person.kontakt.has(or_(*kontakt_filters)))

    if strasse or ort or land or plz:
        adresse_filters = []
        if strasse:
            adresse_filters.append(Adresse.strasse.ilike(f"%{strasse}%"))
        if ort:
            adresse_filters.append(Adresse.ort.ilike(f"%{ort}%"))
        if land:
            adresse_filters.append(Adresse.land.ilike(f"%{land}%"))
        if plz:
            adresse_filters.append(Adresse.plz.ilike(f"%{plz}%"))
        filters.append(Person.adresse.has(or_(*adresse_filters)))

    results = Person.query.filter(*filters).all()
    return results