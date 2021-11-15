from collections import namedtuple

from utils.handlers import handle

malformed_message = "Malformed CRON expression"

Bound = namedtuple('Bound', ['Min', 'Max'])


class Bounds(object):
    """ Min and max values for every element.
    """
    Minute = Bound(0, 60)
    Hour = Bound(0, 24)
    DayOfMonth = Bound(1, 32)
    Month = Bound(1, 13)
    DayOfWeek = Bound(0, 7)


# Labels to display.
labels = [
    "minute",
    "hour",
    "day_of_month",
    "month",
    "day of week",
    "command",
]

# Labels must be exactly 14 chars long.
labels = ["{0:<14}".format(label) for label in labels]


class CronExpression(object):

    def __init__(self, minute: str, hour: str, day_of_month: str, month: str, day_of_week: str, command: str):
        self.minute = minute
        self.hour = hour
        self.day_of_month = day_of_month
        self.month = month
        self.day_of_week = day_of_week
        self.command = command

        self.lines = self._build()
        self.correct = all(self.lines)

    def _build(self):
        return [
            handle(self.minute, min_v=Bounds.Minute.Min, max_v=Bounds.Minute.Max),
            handle(self.hour, min_v=Bounds.Hour.Min, max_v=Bounds.Hour.Max),
            handle(self.day_of_month, min_v=Bounds.DayOfMonth.Min, max_v=Bounds.DayOfMonth.Max),
            handle(self.month, min_v=Bounds.Month.Min, max_v=Bounds.Month.Max),
            handle(self.day_of_week, min_v=Bounds.DayOfWeek.Min, max_v=Bounds.DayOfWeek.Max),
            [self.command]
        ]

    def __repr__(self):
        lines = [" ".join(str(item) for item in line) for line in self.lines]
        lines = [label + line for label, line in zip(labels, lines)]
        return "\n".join(lines)


def explain(expression: str) -> str:
    parts = expression.split(' ')

    # Support of exactly 6 elements.
    if len(parts) != 6:
        return malformed_message

    cron_expression = CronExpression(*parts)

    # Incorrect expression found.
    if not cron_expression.correct:
        return malformed_message

    return str(cron_expression)
