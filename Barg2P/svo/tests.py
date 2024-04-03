from . import *


class PlayerBot(Bot):

    def play_round(self):
        yield Submission(Decision, timeout_happened=True)
        if Results in page_sequence:
            yield Results
