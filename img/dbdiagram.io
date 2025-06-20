Table Person {
  id integer [primary key]
  vorname varchar(80) [not null]
  nachname varchar(80) [not null]
  geburtsdatum date
}

Table Kontakt {
  id integer [primary key]
  email varchar(120)
  telefonnummer varchar(20)
  person_id integer [not null, unique, ref: > Person.id]
}

Table Adresse {
  id integer [primary key]
  strasse varchar(120) [not null]
  hausnummer varchar(10)
  plz varchar(10) [not null]
  ort varchar(80) [not null]
  land varchar(80) [not null]
  person_id integer [not null, unique, ref: > Person.id]
}
