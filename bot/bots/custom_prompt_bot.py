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


class CustomPromptBot(ActivityHandler):
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
                MessageFactory.text("Let's get started. What is your fore name?")
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
                    MessageFactory.text(f"Hi {profile.first_name}")
                )
                await turn_context.send_activity(
                    MessageFactory.text("Whats your last name?")
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
                    MessageFactory.text(f"Your last name is {profile.last_name}.")
                )
                await turn_context.send_activity(
                    MessageFactory.text("When was your born?")
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
                        f"Your born on {profile.date_of_birth}."
                    )
                )
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"Whats your E-Mail?"
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
                    MessageFactory.text(f"Your email is {profile.email}.")
                )
                await turn_context.send_activity(
                    MessageFactory.text(f"Whats your Telephone Number?")
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
                    MessageFactory.text(f"Your telephone number is {profile.telephone_number}.")
                )
                await turn_context.send_activity(
                    MessageFactory.text(f"Which street do you live in?")
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
                    MessageFactory.text(f"Your street is {profile.street}.")
                )
                await turn_context.send_activity(
                    MessageFactory.text(f"What is the number of your house?")
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
                    MessageFactory.text(f"Your house number is {profile.house_number}.")
                )
                await turn_context.send_activity(
                    MessageFactory.text(f"Which postal code are you in?")
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
                    MessageFactory.text(f"Your postal code is {profile.postal_code}.")
                )
                await turn_context.send_activity(
                    MessageFactory.text(f"What city do you live in?")
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
                    MessageFactory.text(f"Your city is {profile.city}.")
                )
                await turn_context.send_activity(
                    MessageFactory.text(f"What country do you live in?")
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
                    MessageFactory.text(f"Your country is {profile.country}.")
                )
                await turn_context.send_activity(
                    MessageFactory.text(f"I am done!")
                )
                flow.last_question_asked = Question.NONE

    def _validate_name(self, user_input: str) -> ValidationResult:
        if not user_input:
            return ValidationResult(
                is_valid=False,
                message="Please enter a name that contains at least one character.",
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
            is_valid=False, message="Please enter an age between 18 and 120."
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
                message="I'm sorry, please enter a date at least an hour out.",
            )
        except ValueError:
            return ValidationResult(
                is_valid=False,
                message="I'm sorry, I could not interpret that as an appropriate "
                "date. Please enter a date at least an hour out.",
            )
