from abc import abstractmethod, ABCMeta
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
        :param max_v: Maximal acceptable value
        :return: List of values matching cron expression.
        """
        pass


class SimpleIntHandler(ParseHandler):
    """
    Handles expressions like "0"
    """

    def can_handle(self, text: str):
        return text.isdigit()

    def handle(self, text: str, min_v: int, max_v: int) -> List[int]:
        value = int(text)
        return [value] if min_v <= value < max_v else []


class RangeHandler(ParseHandler):
    """
    Handles expressions like "1-5"
    """

    def can_handle(self, text: str):
        return '-' in text and text.replace('-', "").isdigit()

    def handle(self, text: str, min_v: int, max_v: int) -> List[int]:
        parts = text.split('-')
        start, end = int(parts[0]), int(parts[1]) + 1
        if min_v <= start <= end <= max_v:
            return list(range(start, end))
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
        if all(min_v <= p <= max_v for p in parts):
            return parts
        return []


class AsteriskHandler(ParseHandler):
    """
        Handles expression "*"
    """

    def can_handle(self, text: str):
        return text == '*'

    def handle(self, text: str, min_v: int, max_v: int) -> List[int]:
        return list(range(min_v, max_v))


class PartitionHandler(ParseHandler):
    """
        Handles expressions like "*/15"
    """

    def can_handle(self, text: str):
        return '*/' in text and text[2:].isdigit()

    def handle(self, text: str, min_v: int, max_v: int) -> List[int]:
        division = int(text.replace('*/', ""))
        items = list(range(min_v, max_v))
        return items[::division]


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
    AsteriskHandler(),
    PartitionHandler(),
    MalformedHandler(),
]


def handle(text: str, min_v: int, max_v: int):
    """ Handles passed expression.

    Iterates over available handlers.

    :param text: Element of cron expression.
    :param min_v: Minimal acceptable value.
    :param max_v: Maximal acceptable value
    :return:
    """
    for handler in handlers:
        if handler.can_handle(text):
            return handler.handle(text, min_v, max_v)
    return []
