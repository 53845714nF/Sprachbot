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
        
        # validate email date then ask for TELEPHONE_NUMBER
        elif flow.last_question_asked == Question.EMAIL:
            validate_result = self._validate_name(user_input)
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
            validate_result = self._validate_name(user_input)
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
            validate_result = self._validate_name(user_input)
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
            validate_result = self._validate_name(user_input)
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
            validate_result = self._validate_name(user_input)
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
            validate_result = self._validate_name(user_input)
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
            validate_result = self._validate_name(user_input)
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                profile.country = validate_result.value
                await turn_context.send_activity(
                    MessageFactory.text(f"Sie leben im Land {profile.country}.")
                )
                await turn_context.send_activity(
                    MessageFactory.text(f"Das war's!")
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
        # Attempt to convert the Recognizer result to an integer. This works for "a dozen", "twelve", "12", and so on.
        # The recognizer returns a list of potential recognition results, if any.
        results = recognize_number(user_input, Culture.English)
        for result in results:
            if "value" in result.resolution:
                age = int(result.resolution["value"])
                if 18 <= age <= 120:
                    return ValidationResult(is_valid=True, value=age)

        return ValidationResult(
            is_valid=False, message="Bitte geben Sie ein Alter zwischen 18 und 120 Jahren an."
        )

    def _validate_date(self, user_input: str) -> ValidationResult:
        try:
            # Try to recognize the input as a date-time. This works for responses such as "11/14/2018", "9pm",
            # "tomorrow", "Sunday at 5pm", and so on. The recognizer returns a list of potential recognition results,
            # if any.
            results = recognize_datetime(user_input, Culture.English)
            for result in results:
                for resolution in result.resolution["values"]:
                    if "value" in resolution:
                        now = datetime.now()

                        value = resolution["value"]
                        if resolution["type"] == "date":
                            candidate = datetime.strptime(value, "%Y-%m-%d")
                        elif resolution["type"] == "time":
                            candidate = datetime.strptime(value, "%H:%M:%S")
                            candidate = candidate.replace(
                                year=now.year, month=now.month, day=now.day
                            )
                        else:
                            candidate = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

                        # user response must be more than an hour out
                        diff = candidate - now
                        if diff.total_seconds() >= 3600:
                            return ValidationResult(
                                is_valid=True,
                                value=candidate.strftime("%m/%d/%y"),
                            )

            return ValidationResult(
                is_valid=False,
                message="Es tut mir leid, ich konnte das nicht als geeignetes Datum interpretieren.",
            )
        except ValueError:
            return ValidationResult(
                is_valid=False,
                message="Es tut mir leid, ich konnte das nicht als geeignetes Datum interpretieren.",
            )
