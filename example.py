import logging
from time import sleep
import tkinter as tk

from ate import Test
from ate import TestSequence
from tkate import TkAteFrame


class CommunicationTest(Test):
    def __init__(self, loglevel=logging.INFO):
        super().__init__(moniker='communications test', loglevel=loglevel)

    def execute(self, aborted=False):
        if aborted:
            return None

        sleep(0.5)

        # should return a (key, value) which are the results of the test
        self.test_is_passing = True
        return 'dual comm', False


class PumpTest(Test):
    def __init__(self, loglevel=logging.INFO):
        super().__init__(moniker='pump test', loglevel=loglevel)

    def setup(self, aborted=False):
        sleep(0.5)
        return None

    def execute(self, aborted=False):
        if aborted:
            return None

        sleep(0.5)  # simulate long-running process

        # should return a (key, value) which are the results of the test
        self.test_is_passing = True
        return 'pump', False

    def teardown(self, aborted=False):
        sleep(0.5)
        return None


logging.basicConfig(level=logging.DEBUG)

# create the sequence of test objects
sequence = [CommunicationTest(), PumpTest()]
ts = TestSequence(sequence=sequence, auto_run=False, loglevel=logging.DEBUG)

window = tk.Tk()

tkate_frame = TkAteFrame(window, ts)
tkate_frame.grid()

window.mainloop()
