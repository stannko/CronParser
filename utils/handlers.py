from abc import abstractmethod, ABCMeta
from collections import Counter
from typing import List


class ParseHandler(metaclass=ABCMeta):
    """
    Base handler of cron expressions.
    Uses Chain Of Responsibility pattern.
    """

    @abstractmethod
    def can_handle(self, text: str):
        """ Checks if can handle specific expression.

        :param text: Expression.
        :return: Whether can handle specific expression.
        """
        pass

    @abstractmethod
    def handle(self, text: str, min_v: int, max_v: int) -> List[int]:
        """ Parses an element of cron expression.

        :param text: Element of cron expression.
        :param min_v: Minimal acceptable value.
        :param max_v: Maximal acceptable value.
        :return: List of values matching cron expression.
        """
        pass


class SimpleIntHandler(ParseHandler):
    """
    Handles expressions like "0".
    """

    def can_handle(self, text: str):
        return text.isdigit()

    def handle(self, text: str, min_v: int, max_v: int) -> List[int]:
        value = int(text)
        return [value] if min_v <= value < max_v else []


class RangeHandler(ParseHandler):
    """
    Handles expressions like "1-5/2".
    Works exactly the same way as python's slicing. eg. [1:5:2]
    """

    @staticmethod
    def _is_valid_text(text):
        """ Checks if the expression is not malformed.

        :param text: Expression.
        :return: If expression is valid.
        """
        counter = Counter(text)
        if counter['-'] > 1:
            return False
        if counter['*'] > 1:
            return False
        if counter['/'] > 1:
            return False
        if '*' in text and text.index('*') != 0:
            return False
        if '-' in text and text.index('-') == 0:
            return False
        if text != "*" and not text.replace("*", "").replace("/", "").replace("-", "").isdigit():
            return False

        return True

    def can_handle(self, text: str):
        return ('-' in text or '*' in text) and self._is_valid_text(text)

    def handle(self, text: str, min_v: int, max_v: int) -> List[int]:
        step = 1
        start = min_v
        end = max_v

        # Step is present in expression
        if "/" in text:
            # Split range and step
            parts = text.split("/")
            if len(parts) != 2:
                return []

            text = parts[0]
            step = int(parts[1])

        if text != '*':
            # Range was passed
            parts = text.split('-')
            start, end = int(parts[0]), int(parts[1]) + 1

        if min_v <= start <= end <= max_v:
            return list(range(start, end, step))

        return []


class EnumerationHandler(ParseHandler):
    """
        Handles expressions like "1,15"
    """

    def can_handle(self, text: str):
        return ',' in text and text.replace(',', "").isdigit()

    def handle(self, text: str, min_v: int, max_v: int) -> List[int]:
        parts = text.split(',')
        parts = [int(p) for p in parts]
        if all(min_v <= p < max_v for p in parts):
            return parts
        return []


class MalformedHandler(ParseHandler):
    """
        Handles all other not supported expressions.
    """

    def can_handle(self, text: str):
        return True

    def handle(self, text: str, min_v: int, max_v: int) -> List[int]:
        return []


# Chain of responsibility handlers.
handlers = [
    SimpleIntHandler(),
    RangeHandler(),
    EnumerationHandler(),
    MalformedHandler(),
]


def handle(text: str, min_v: int, max_v: int) -> List[int]:
    """
    Handles passed expression.
    Iterates over available handlers.

    :param text: Element of cron expression.
    :param min_v: Minimal acceptable value.
    :param max_v: Maximal acceptable value.
    :return: A list of matching times represented as int.
    """
    for handler in handlers:
        if handler.can_handle(text):
            try:
                return handler.handle(text, min_v, max_v)
            except ValueError:
                return []
    return []
