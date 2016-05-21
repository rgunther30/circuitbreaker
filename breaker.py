import time
import functools


CLOSED = 0
OPEN = 1


class CircuitBreaker(object):
    def __init__(self, allowed_fails=3, retry_time=30):
        '''
        Initializes Breaker object

        Args:
            allowed_fails(int): Maximum number of consecutive failures allowed before
                                opening circuit
            retry_time(int): Number of seconds during close period before allowing
                             test request to check if other end of circuit is responsive
        '''
        self.allowed_fails = allowed_fails
        self.retry_time = retry_time
        self.failure_count = 0
        self.state = CLOSED
        self.half_open_time = 0  # initialize to minimum seconds since epoch

    def on_failure(self):
        '''
        Increments failure counter and switches state if allowed_fails is reached
        '''

        self.failure_count += 1
        print "fail count %s" % self.failure_count
        if self.failure_count == self.allowed_fails:
            print "OPEN"
            self.state = OPEN
            open_time = time.time()
            self.half_open_time = open_time + self.retry_time

    def on_success(self):
        '''
        Resets failure counter and moves breaker to closed state
        '''
        self.failure_count = 0
        self.state = CLOSED
        print "CLOSED"
        print "fail count %s" % self.failure_count

    def __call__(self, func):
        '''
        Wraps decorated function and watches for successes and failures
        '''
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            if self.state == OPEN:
                now = time.time()
                if now < self.half_open_time:
                    print "gotta wait"
                    return
            try:
                func(*args, **kwargs)
            except Exception:
                self.on_failure()
                return

            self.on_success()

        return wrapped_func


if __name__ == "__main__":
    # test code for now
    @CircuitBreaker(allowed_fails=3, retry_time=4)
    def test_func(number):
        if number % 4 == 0:
            return True
        else:
            raise ValueError("Not divisible by 4 lolwut")

    for i in xrange(25):
        time.sleep(1)
        test_func(i)
