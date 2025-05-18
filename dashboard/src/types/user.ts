export interface User {
  id: number;
  vorname: string;
  nachname: string;
  geburtsdatum: string;
  kontakt: {
    email: string;
    telefonnummer: string;
  };
  adresse: {
    strasse: string;
    hausnummer: string;
    plz: string;
    ort: string;
    land: string;
  };
}

export interface CreateUserI {
  id: number;
  vorname: string;
  nachname: string;
  geburtsdatum: string;
  email: string;
  telefonnummer: string;
  strasse: string;
  hausnummer: string;
  plz: string;
  ort: string;
  land: string;
}