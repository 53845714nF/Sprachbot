title User Profile Registration Flow

participant User
participant Bot
participant ML Service

note over Bot: Start Profile Registration
User-> Bot: "Hallo"
Bot->User: "Dann fangen wir mal an. Wie lautet Ihr Vorname?"

User->Bot: [Vorname eingeben]
Bot->ML Service: analyze_query(user_input, "vorname_entity")
ML Service->Bot: ml_result
Bot->Bot: _validate_name(ml_result)

alt Validation erfolgreich
    Bot->User: "Hallo [Vorname]"
    Bot->User: "Wie lautet Ihr Nachname?"
else Validation fehlgeschlagen
    Bot->User: [Fehlermeldung]
end

User->Bot: [Nachname eingeben]
Bot->ML Service: analyze_query(user_input, "nachname_entity")
ML Service->Bot: ml_result
Bot->Bot: _validate_name(ml_result)

alt Validation erfolgreich
    Bot->User: "Dein Nachname ist [Nachname]."
    Bot->User: "Wann wurden Sie geboren?"
else Validation fehlgeschlagen
    Bot->User: [Fehlermeldung]
end

User->Bot: [Geburtsdatum eingeben]
Bot->ML Service: analyze_query(user_input, "geburtstag_entity")
ML Service->Bot: ml_result
Bot->Bot: _validate_date(ml_result)

alt Validation erfolgreich
    Bot->User: "Dein Geburstag ist der [Datum]."
    Bot->User: "Wie lautet Ihre E-Mail-Adresse?"
else Validation fehlgeschlagen
    Bot->User: [Fehlermeldung]
end

User->Bot: [E-Mail eingeben]
Bot->ML Service: analyze_query(user_input, "e-mail_entity")
ML Service->Bot: ml_result
Bot->Bot: _validate_email(ml_result)

alt Validation erfolgreich
    Bot->User: "Deine E-Mail-Adresse ist [Email]."
    Bot->User: "Wie lautet Ihre Telefonnummer?"
else Validation fehlgeschlagen
    Bot->User: [Fehlermeldung]
end

User->Bot: [Telefonnummer eingeben]
Bot->ML Service: analyze_query(user_input, "telefonnummer_entity")
ML Service->Bot: ml_result
Bot->Bot: _validate_tel(ml_result)

alt Validation erfolgreich
    Bot->User: "Diene Telefonnummer ist [Telefon]."
    Bot->User: "In welcher Straße wohnen Sie?"
else Validation fehlgeschlagen
    Bot->User: [Fehlermeldung]
end

User->Bot: [Straße eingeben]
Bot->ML Service: analyze_query(user_input, "straße_entity")
ML Service->Bot: ml_result
Bot->Bot: _validate_street(ml_result)

alt Validation erfolgreich
    Bot->User: "Sie leben in der Straße [Straße]."
    Bot->User: "Wie lautet die Nummer Ihres Hauses?"
else Validation fehlgeschlagen
    Bot->User: [Fehlermeldung]
end

User->Bot: [Hausnummer eingeben]
Bot->ML Service: analyze_query(user_input, "hausnummer_entity")
ML Service->Bot: ml_result
Bot->Bot: _validate_house_number(ml_result)

alt Validation erfolgreich
    Bot->User: "ihre Haus Nummer lautet [Hausnummer]."
    Bot->User: "In welcher Postleitzahl wohnen Sie?"
else Validation fehlgeschlagen
    Bot->User: [Fehlermeldung]
end

User->Bot: [PLZ eingeben]
Bot->ML Service: analyze_query(user_input, "plz_entity")
ML Service->Bot: ml_result
Bot->Bot: _validate_postal_code(ml_result)

alt Validation erfolgreich
    Bot->User: "Ihre Postleitzahl ist die [PLZ]."
    Bot->User: "In welcher Stadt leben Sie?"
else Validation fehlgeschlagen
    Bot->User: [Fehlermeldung]
end

User->Bot: [Stadt eingeben]
Bot->ML Service: analyze_query(user_input, "ort_entity")
ML Service->Bot: ml_result
Bot->Bot: _validate_city(ml_result)

alt Validation erfolgreich
    Bot->User: "Ihre Stadt heißt [Stadt]."
    Bot->User: "In welchem Land leben Sie?"
else Validation fehlgeschlagen
    Bot->User: [Fehlermeldung]
end

User->Bot: [Land eingeben]
Bot->ML Service: analyze_query(user_input, "land_entity")
ML Service->Bot: ml_result
Bot->Bot: _validate_country(ml_result)

alt Validation erfolgreich
    Bot->User: "Sie leben im Land [Land]."
    Bot->Bot: create_user() - Nutzer erstellen
    Bot->User: "Der Nutzer wurde erfolgreich erstellt. Das war's!"
else Validation fehlgeschlagen
    Bot->User: [Fehlermeldung]
end
