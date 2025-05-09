class UserProfile:
    def __init__(self, first_name: str = None, last_name: str = None,
                 date_of_birth: str = None, email: str = None,
                 telephone_number: str = None, street: str = None,
                 house_number: int = 0, postal_code: int = 0,
                 city: str = None, country: str = None):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.email = email
        self.telephone_number = telephone_number
        self.street = street
        self.house_number = house_number
        self.postal_code = postal_code
        self.city = city
        self.country = country