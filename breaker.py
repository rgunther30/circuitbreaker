import time
import functools


CLOSED = 0
OPEN = 1

state_map = {CLOSED: "CLOSED", OPEN: "OPEN"}


class CircuitBreaker(object):
    def __init__(self, allowed_fails=3, retry_time=30, validation_func=None):
        '''
        Initializes Breaker object

        Args:
            allowed_fails(int): Maximum number of consecutive failures allowed before
                                opening circuit
            retry_time(int): Number of seconds during close period before allowing
                             test request to check if other end of circuit is responsive
            validation_func(func): function to check if return value of wrapped function
                                   is permissible. Must return boolean value
        '''
        self.allowed_fails = allowed_fails
        self.retry_time = retry_time
        self.validation_func = validation_func
        self.failure_count = 0
        self.state = CLOSED
        self.half_open_time = 0  # initialize to minimum seconds since epoch

    def on_failure(self):
        '''
        Increments failure counter and switches state if allowed_fails is reached
        '''

        self.failure_count += 1
        if self.failure_count == self.allowed_fails:
            self.state = OPEN
            open_time = time.time()
            self.half_open_time = open_time + self.retry_time

    def on_success(self):
        '''
        Resets failure counter and moves breaker to closed state
        '''
        self.failure_count = 0
        self.state = CLOSED

    def parse_result(self, result):
        '''
        Determine if result of wrapped function is valid

        Args:
            result(object): return value of wrapped function
        '''
        if self.validation_func(result):
            self.on_success()
        else:
            self.on_failure()

    def __call__(self, func):
        '''
        Wraps decorated function and watches for successes and failures
        '''
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            if self.state == OPEN:
                now = time.time()
                if now < self.half_open_time:
                    return
            try:
                result = func(*args, **kwargs)
            except Exception:
                self.on_failure()
                return

            if self.validation_func is not None:
                self.parse_result(result)
            else:
                self.on_success()

        return wrapped_func


if __name__ == "__main__":

    def validator(number):
        return number > 14

    # test code for now
    @CircuitBreaker(allowed_fails=3, retry_time=4, validation_func=validator)
    def test_func(number):
        if number % 4 == 0:
            return number * 2
        else:
            raise ValueError("Not divisible by 4 lolwut")

    for i in xrange(25):
        time.sleep(1)
        test_func(i)
