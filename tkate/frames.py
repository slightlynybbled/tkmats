import logging
from tkinter.ttk import Frame, Button, Label

from ate import Test, TestSequence

_light_green = '#66ff66'
_light_red = '#ff6666'
_light_yellow = '#ffff99'


class TkAteFrame(Frame):
    def __init__(self, parent, sequence: TestSequence, loglevel=logging.INFO):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(loglevel)

        self._parent = parent
        super().__init__(self._parent)

        self._sequence = sequence

        row = 0
        col = 0

        Button(self, text='Start', command=sequence.start).grid(row=row, column=col)

        col += 1
        Label(self, text='\u27a4').grid(row=row, column=col)

        col += 1
        self._test_status_frames = []
        for test in self._sequence.tests:
            self._test_status_frames.append(
                TestStatusFrame(self, test)
            )

        for i, tf in enumerate(self._test_status_frames):
            col += 1
            tf.grid(row=row, column=col)
            col += 1
            Label(self, text='\u27a4').grid(row=row, column=col)

        col += 1
        self._complete_label = Label(self, text='-', anchor='center', justify='center')
        self._complete_label.grid(row=row, column=col, sticky='news')

        self._update()

    def _update(self):
        if self._sequence.in_progress:
            self._complete_label.config(text='in progress', background=_light_yellow)
        elif self._sequence.is_aborted:
            self._complete_label.config(text='aborted', background=_light_red)
        elif self._sequence.is_passing:
            self._complete_label.config(text='pass', background=_light_green)
        else:
            self._complete_label.config(text='fail', background=_light_red)

        self.after(100, self._update)


class TestStatusFrame(Frame):
    def __init__(self, parent, test: Test, loglevel=logging.INFO):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(loglevel)

        self._parent = parent
        super().__init__(self._parent)

        self._test = test

        label_text = self._test.moniker.replace(' ', '\n')
        self._label = Label(self, text=label_text, anchor='center', justify='center')
        self._label.grid()

        self._label_bg_color = self._label.cget('background')

        self._update()

    def _update(self):
        if self._test.status == 'waiting':
            self._label.config(background=self._label_bg_color)
        elif self._test.status == 'running':
            self._label.config(background=_light_yellow)
        elif self._test.status == 'aborted':
            self._label.config(background=_light_red)
        elif not self._test.test_is_passing:
            self._label.config(background=_light_red)
        elif self._test.test_is_passing:
            self._label.config(background=_light_green)

        self.after(100, self._update)
