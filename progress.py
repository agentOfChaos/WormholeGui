from etaprogress.progress import ProgressBarBytes

from etaprogress.components.eta_conversions import eta_letters
from etaprogress.components.units import UnitByte

import locale


class CustomProgressIndicator(ProgressBarBytes):

    def __init__(self, denominator, max_width=None):
        super().__init__(denominator, max_width)

    @staticmethod
    def _generate_eta(seconds):
        """Returns a human readable ETA string."""
        return '' if seconds is None else eta_letters(seconds)

    @property
    def str_eta(self):
        """Returns a formatted ETA value for the progress bar."""
        eta = eta_letters(self._eta.elapsed) if self.done else self._eta_string
        if not eta:
            return ''
        if eta.count(' ') > 1:
            eta = ' '.join(eta.split(' ')[:2])  # Only show up to two units (h and m, no s for example).
        return (' in {0}' if self.done else 'ETA: {0}').format(eta)

    @property
    def str_rate(self):
        """Returns the rate with formatting. If done, returns the overall rate instead."""
        # Handle special cases.
        if not self._eta.started or self._eta.stalled or not self.rate:
            return '--.-KiB/s'

        unit_rate, unit = UnitByte(self._eta.rate_overall if self.done else self.rate).auto
        if unit_rate >= 100:
            formatter = '%d'
        elif unit_rate >= 10:
            formatter = '%.1f'
        else:
            formatter = '%.2f'
        return '{0}{1}/s'.format(locale.format_string(formatter, unit_rate, grouping=False), unit)

    @property
    def str_numerator(self):
        """Returns the numerator with formatting."""
        unit_numerator, unit = self._unit_class(self.numerator).auto
        formatter = '%d' if unit_numerator == self.numerator else '%0.2f'
        numerator = locale.format_string(formatter, unit_numerator, grouping=True)
        return '{0} {1}'.format(numerator, unit)
