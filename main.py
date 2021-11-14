import argparse

from utils.parser import explain


def _get_args():
    """ Returns command line arguments

    :return: Arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--expression', type=str, required=True)
    return parser.parse_args()


def main():
    """ Script entry point.

    :return: Explanation of a cron expression.
    """
    expression = _get_args().expression
    print(explain(expression))


if __name__ == '__main__':
    main()
