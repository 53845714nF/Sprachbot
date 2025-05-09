from enum import Enum

class Question(Enum):
    FIRST_NAME = 1
    LAST_NAME = 2
    DATE_OF_BIRTH = 3
    EMAIL = 4
    TELEPHONE_NUMBER = 5
    STREET = 6
    HOUSE_NUMBER = 7
    POSTAL_CODE = 8
    CITY = 9
    COUNTRY = 10
    NONE = 11


class ConversationFlow:
    def __init__(
        self, last_question_asked: Question = Question.NONE,
    ):
        self.last_question_asked = last_question_asked
