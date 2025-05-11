from datetime import date

# Own Modules
from database import db

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(80), nullable=False)
    nachname = db.Column(db.String(80), nullable=False)
    geburtsdatum = db.Column(db.Date)
    kontakt = db.relationship('Kontakt', backref='person', uselist=False)
    adresse = db.relationship('Adresse', backref='person', uselist=False)

    def __repr__(self):
        return f'<Person {self.vorname} {self.nachname}>'

class Kontakt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    telefonnummer = db.Column(db.String(20))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False, unique=True)

    def __repr__(self):
        return f'<Kontakt {self.email}>'

class Adresse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strasse = db.Column(db.String(120), nullable=False)
    hausnummer = db.Column(db.String(10))
    plz = db.Column(db.String(10), nullable=False)
    ort = db.Column(db.String(80), nullable=False)
    land = db.Column(db.String(80), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False, unique=True)

    def __repr__(self):
        return f'<Adresse {self.ort}, {self.land}>'