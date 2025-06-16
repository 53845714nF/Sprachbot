# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datetime import datetime

from recognizers_number import recognize_number, Culture
from recognizers_date_time import recognize_datetime

from botbuilder.core import (
    ActivityHandler,
    ConversationState,
    TurnContext,
    UserState,
    MessageFactory,
)

from data_models import ConversationFlow, Question, UserProfile
from .create_user import create_user

class ValidationResult:
    def __init__(
        self, is_valid: bool = False, value: object = None, message: str = None
    ):
        self.is_valid = is_valid
        self.value = value
        self.message = message


class UserPromptBot(ActivityHandler):
    def __init__(self, conversation_state: ConversationState, user_state: UserState):
        if conversation_state is None:
            raise TypeError(
                "[CustomPromptBot]: Missing parameter. conversation_state is required but None was given"
            )
        if user_state is None:
            raise TypeError(
                "[CustomPromptBot]: Missing parameter. user_state is required but None was given"
            )

        self.conversation_state = conversation_state
        self.user_state = user_state

        self.flow_accessor = self.conversation_state.create_property("ConversationFlow")
        self.profile_accessor = self.user_state.create_property("UserProfile")

    async def on_message_activity(self, turn_context: TurnContext):
        # Get the state properties from the turn context.
        profile = await self.profile_accessor.get(turn_context, UserProfile)
        flow = await self.flow_accessor.get(turn_context, ConversationFlow)

        await self._fill_out_user_profile(flow, profile, turn_context)

        # Save changes to UserState and ConversationState
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def _fill_out_user_profile(
        self, flow: ConversationFlow, profile: UserProfile, turn_context: TurnContext
    ):
        user_input = turn_context.activity.text.strip()

        # ask for name
        if flow.last_question_asked == Question.NONE:
            await turn_context.send_activity(
                MessageFactory.text("Dann fangen wir mal an. Wie lautet Ihr Vorname?")
            )
            flow.last_question_asked = Question.FIRST_NAME

        # validate first name then ask for lastname
        elif flow.last_question_asked == Question.FIRST_NAME:
            validate_result = self._validate_name(user_input)
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                profile.first_name = validate_result.value
                await turn_context.send_activity(
                    MessageFactory.text(f"Hallo {profile.first_name}")
                )
                await turn_context.send_activity(
                    MessageFactory.text("Wie lautet Ihr Nachname?")
                )
                flow.last_question_asked = Question.LAST_NAME

        # validate last name then ask for birth date
        elif flow.last_question_asked == Question.LAST_NAME:
            validate_result = self._validate_name(user_input)
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                profile.last_name = validate_result.value
                await turn_context.send_activity(
                    MessageFactory.text(f"Dein Nachname ist {profile.last_name}.")
                )
                await turn_context.send_activity(
                    MessageFactory.text("Wann wurden Sie geboren?")
                )
                flow.last_question_asked = Question.DATE_OF_BIRTH

        # validate birth date then ask for email
        elif flow.last_question_asked == Question.DATE_OF_BIRTH:
            validate_result = self._validate_date(user_input)
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                profile.date_of_birth = validate_result.value
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"Dein Geburstag ist der {profile.date_of_birth}."
                    )
                )
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"Wie lautet Ihre E-Mail-Adresse?"
                    )
                )
                flow.last_question_asked = Question.EMAIL

                # Konvertiere das Datum in YYYY-MM-DD Format
                try:
                    date_obj = datetime.strptime(profile.date_of_birth, '%d.%m.%Y')
                    profile.date_of_birth = date_obj.strftime('%Y-%m-%d')
                except ValueError:
                    print("Fehler bei der Datumsumwandlung")
        
        # validate email date then ask for TELEPHONE_NUMBER
        elif flow.last_question_asked == Question.EMAIL:
            validate_result = self._validate_email(user_input)
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                profile.email = validate_result.value
                await turn_context.send_activity(
                    MessageFactory.text(f"Deine E-Mail-Adresse ist {profile.email}.")
                )
                await turn_context.send_activity(
                    MessageFactory.text(f"Wie lautet Ihre Telefonnummer?")
                )
                flow.last_question_asked = Question.TELEPHONE_NUMBER

        # validate tele then ask for street
        elif flow.last_question_asked == Question.TELEPHONE_NUMBER:
            validate_result = self._validate_tel(user_input)
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                profile.telephone_number = validate_result.value
                await turn_context.send_activity(
                    MessageFactory.text(f"Diene Telefonnummer ist {profile.telephone_number}.")
                )
                await turn_context.send_activity(
                    MessageFactory.text(f"In welcher Straße wohnen Sie?")
                )
                flow.last_question_asked = Question.STREET

        # validate stree then ask for house number
        elif flow.last_question_asked == Question.STREET:
            validate_result = self._validate_street(user_input)
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                profile.street = validate_result.value
                await turn_context.send_activity(
                    MessageFactory.text(f"Sie leben in der Straße {profile.street}.")
                )
                await turn_context.send_activity(
                    MessageFactory.text(f"Wie lautet die Nummer Ihres Hauses?")
                )
                flow.last_question_asked = Question.HOUSE_NUMBER
        
        # validate housenumber then ask for postal code
        elif flow.last_question_asked == Question.HOUSE_NUMBER:
            validate_result = self._validate_house_number(user_input)
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                profile.house_number = validate_result.value
                await turn_context.send_activity(
                    MessageFactory.text(f"ihre Haus Nummer lautet {profile.house_number}.")
                )
                await turn_context.send_activity(
                    MessageFactory.text(f"In welcher Postleitzahl wohnen Sie?")
                )
                flow.last_question_asked = Question.POSTAL_CODE

        # validate postal_code then ask for city
        elif flow.last_question_asked == Question.POSTAL_CODE:
            validate_result = self._validate_postal_code(user_input)
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                profile.postal_code = validate_result.value
                await turn_context.send_activity(
                    MessageFactory.text(f"Ihre Postleitzahl ist die {profile.postal_code}.")
                )
                await turn_context.send_activity(
                    MessageFactory.text(f"In welcher Stadt leben Sie?")
                )
                flow.last_question_asked = Question.CITY

        # validate city then ask for country
        elif flow.last_question_asked == Question.CITY:
            validate_result = self._validate_city(user_input)
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                profile.city = validate_result.value
                await turn_context.send_activity(
                    MessageFactory.text(f"Ihre Stadt heißt {profile.city}.")
                )
                await turn_context.send_activity(
                    MessageFactory.text(f"In welchem Land leben Sie?")
                )
                flow.last_question_asked = Question.COUNTRY
        
        # validate country then ask for noting
        elif flow.last_question_asked == Question.COUNTRY:
            validate_result = self._validate_country(user_input)
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                profile.country = validate_result.value
                await turn_context.send_activity(
                    MessageFactory.text(f"Sie leben im Land {profile.country}.")
                )
                create_user(profile.first_name,
                        profile.last_name,
                        profile.date_of_birth,
                        profile.email,
                        profile.telephone_number,
                        profile.street,
                        profile.house_number,
                        profile.postal_code,
                        profile.city,
                        profile.country)
                
                await turn_context.send_activity(
                    MessageFactory.text(f"Der Nutzer wurde erfolgreich erstellt. Das war's!")
                )
                flow.last_question_asked = Question.NONE

    def _validate_name(self, user_input: str) -> ValidationResult:
        if not user_input:
            return ValidationResult(
                is_valid=False,
                message="Bitte geben Sie einen Namen ein, der mindestens einen Buchstaben enthält.",
            )

        return ValidationResult(is_valid=True, value=user_input)

    def _validate_age(self, user_input: str) -> ValidationResult:
        results = recognize_number(user_input, Culture.English)
        for result in results:
            if "value" in result.resolution:
                age = int(result.resolution["value"])
                if 18 <= age <= 120:
                    return ValidationResult(is_valid=True, value=age)

        return ValidationResult(
            is_valid=False, message="Bitte geben Sie ein Alter zwischen 18 und 120 Jahren an."
        )

    def _validate_email(self, user_input: str) -> ValidationResult:
        if not user_input:
            return ValidationResult(
                is_valid=False,
                message="Bitte geben Sie eine E-Mail-Adresse ein.",
            )
        
        if '@' not in user_input or '.' not in user_input[user_input.find('@'):]:
            return ValidationResult(
                is_valid=False,
                message="Bitte geben Sie eine gültige E-Mail-Adresse ein (muss @ und einen Punkt nach dem @ enthalten).",
            )
            
        return ValidationResult(is_valid=True, value=user_input)

    def _validate_date(self, user_input: str) -> ValidationResult:
        try:
            # Versuche das Datum im Format DD.MM.YYYY zu parsen
            date_parts = user_input.split('.')
            if len(date_parts) != 3:
                return ValidationResult(
                    is_valid=False,
                    message="Bitte geben Sie das Datum im Format TT.MM.JJJJ ein (z.B. 19.02.2001)"
                )
            
            day = int(date_parts[0])
            month = int(date_parts[1])
            year = int(date_parts[2])
            
            # Überprüfe die Gültigkeit des Datums
            if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2100):
                return ValidationResult(
                    is_valid=False,
                    message="Bitte geben Sie ein gültiges Datum ein (z.B. 19.02.2001)"
                )
            
            # Formatiere das Datum zurück in das gewünschte Format
            formatted_date = f"{day:02d}.{month:02d}.{year}"
            return ValidationResult(is_valid=True, value=formatted_date)
            
        except ValueError:
            return ValidationResult(
                is_valid=False,
                message="Bitte geben Sie das Datum im Format TT.MM.JJJJ ein (z.B. 19.02.2001)"
            )

    def _validate_tel(self, user_input: str) -> ValidationResult:
        if not user_input:
            return ValidationResult(
                is_valid=False,
                message="Bitte geben Sie eine Telefonnummer ein.",
            )
        
        # Entferne Leerzeichen für die Validierung
        tel = user_input.replace(" ", "")
        
        # Prüfe ob die Nummer mit + beginnt
        if tel.startswith('+'):
            tel = tel[1:]
        
        # Prüfe ob nur Zahlen enthalten sind
        if not tel.isdigit():
            return ValidationResult(
                is_valid=False,
                message="Die Telefonnummer darf nur Zahlen und optional ein + am Anfang enthalten.",
            )
        
        # Prüfe die Länge (internationale Nummern haben zwischen 7 und 15 Ziffern)
        if len(tel) < 7 or len(tel) > 15:
            return ValidationResult(
                is_valid=False,
                message="Die Telefonnummer muss zwischen 7 und 15 Ziffern lang sein.",
            )
            
        return ValidationResult(is_valid=True, value=user_input)

    def _validate_street(self, user_input: str) -> ValidationResult:
        if not user_input:
            return ValidationResult(
                is_valid=False,
                message="Bitte geben Sie eine Straße ein.",
            )
        
        # Es gibt Straßen mit 1 Zeichen, darum nicht die Länge prüfen
        return ValidationResult(is_valid=True, value=user_input)

    def _validate_house_number(self, user_input: str) -> ValidationResult:
        if not user_input:
            return ValidationResult(
                is_valid=False,
                message="Bitte geben Sie eine Hausnummer ein.",
            )
        
        number = user_input.replace(" ", "")
        
        # Prüfe ob die Hausnummer mit einer Zahl beginnt
        # Es gibt Hausnummern mit Buchstaben wie 2a
        if not number[0].isdigit():
            return ValidationResult(
                is_valid=False,
                message="Die Hausnummer muss mit einer Zahl beginnen.",
            )
            
        return ValidationResult(is_valid=True, value=user_input)

    def _validate_postal_code(self, user_input: str) -> ValidationResult:
        if not user_input:
            return ValidationResult(
                is_valid=False,
                message="Bitte geben Sie eine Postleitzahl ein.",
            )
        
        postal_code = user_input.replace(" ", "")
        
        # Prüfe ob die Postleitzahl nur aus Zahlen besteht
        if not postal_code.isdigit():
            return ValidationResult(
                is_valid=False,
                message="Die Postleitzahl darf nur aus Zahlen bestehen.",
            )
        
        # Prüfe ob die Postleitzahl 5 Ziffern hat
        if len(postal_code) != 5:
            return ValidationResult(
                is_valid=False,
                message="Die Postleitzahl muss genau 5 Ziffern lang sein.",
            )
            
        return ValidationResult(is_valid=True, value=user_input)

    def _validate_city(self, user_input: str) -> ValidationResult:
        if not user_input:
            return ValidationResult(
                is_valid=False,
                message="Bitte geben Sie eine Stadt ein.",
            )
        # Es gibt Städte mit 1 Zeichen, darum nicht die Länge prüfen        
        return ValidationResult(is_valid=True, value=user_input)

    def _validate_country(self, user_input: str) -> ValidationResult:
        if not user_input:
            return ValidationResult(
                is_valid=False,
                message="Bitte geben Sie ein Land ein.",
            )
        
        # Chad, Peru, Mali, Iran haben 4 Zeichen 
        # Prüfe ob das Land mindestens 4 Zeichen lang ist
        if len(user_input) < 4:
            return ValidationResult(
                is_valid=False,
                message="Der Ländername muss mindestens 4 Zeichen lang sein.",
            )
            
        return ValidationResult(is_valid=True, value=user_input)
