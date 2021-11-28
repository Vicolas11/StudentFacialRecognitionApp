import time

class TimeoutVar:
    """Variable whose values time out."""

    def __init__(self, value, timeout):
        """Store the timeout and value."""
        self._value = value
        self._last_set = time.time()
        self.timeout = timeout

    @property
    def value(self):
        """Get the value if the value hasn't timed out."""
        if time.time() - self._last_set < self.timeout:
            return self._value

    @value.setter
    def value(self, value, timeout=None):
        """Set the value while resetting the timer."""
        self._value = value
        self._last_set = time.time()
        if timeout is not None:
            self.timeout = timeout