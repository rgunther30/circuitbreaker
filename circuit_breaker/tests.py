import unittest
import time

import circuit_breaker

DEFAULT_FAILS = 3
DEFAULT_RETRY = 1


def validation_stub(number):
    return number > 0


class TestBreaker(unittest.TestCase):
    def setUp(self):
        self.breaker = circuit_breaker.CircuitBreaker(
            allowed_fails=DEFAULT_FAILS,
            retry_time=DEFAULT_RETRY,
            validation_func=None
        )
        self.breaker_with_validation = circuit_breaker.CircuitBreaker(
            allowed_fails=DEFAULT_FAILS,
            retry_time=DEFAULT_RETRY,
            validation_func=validation_stub
        )
        self.breaker_with_allowed = circuit_breaker.CircuitBreaker(
            allowed_exceptions=[AttributeError]
        )
        self.breaker_with_fail_exc = circuit_breaker.CircuitBreaker(
            failure_exceptions=[KeyError]
        )

    def test_open_transition(self):
        breaker = self.breaker
        for i in range(DEFAULT_FAILS):
            breaker._on_failure()
        self.assertEqual(breaker._state, circuit_breaker.OPEN)
        self.assertEqual(breaker._failure_count, DEFAULT_FAILS)

    def test_success(self):
        breaker = self.breaker
        for i in range(DEFAULT_FAILS - 1):
            breaker._on_failure()
        self.assertEqual(breaker._state, circuit_breaker.CLOSED)
        self.assertEqual(breaker._failure_count, DEFAULT_FAILS - 1)

        breaker._on_success()
        self.assertEqual(breaker._state, circuit_breaker.CLOSED)
        self.assertEqual(breaker._failure_count, 0)

    def test_half_open(self):
        breaker = self.breaker
        for i in range(DEFAULT_FAILS):
            breaker._on_failure()
        self.assertEqual(breaker._state, circuit_breaker.OPEN)

        time.sleep(DEFAULT_RETRY)
        breaker._check_state()
        self.assertEqual(breaker._state, circuit_breaker.HALF_OPEN)

    def test_validation_func(self):
        breaker = self.breaker_with_validation
        fake_result = 0
        breaker._parse_result(fake_result)
        self.assertEqual(breaker._failure_count, 1)
        # breaker should reset count upon success
        fake_result = 1
        breaker._parse_result(fake_result)
        self.assertEqual(breaker._failure_count, 0)

    def test_parse_allowed_exc(self):
        breaker = self.breaker_with_allowed
        breaker._parse_exception(KeyError)
        self.assertEqual(breaker._failure_count, 1)
        breaker._parse_exception(AttributeError)
        # reset on success
        self.assertEqual(breaker._failure_count, 0)

    def test_parse_failure_exc(self):
        breaker = self.breaker_with_fail_exc
        breaker._parse_exception(KeyError)
        self.assertEqual(breaker._failure_count, 1)
        breaker._parse_exception(AttributeError)
        self.assertEqual(breaker._failure_count, 0)

    def test_handles_child_exc(self):
        class TestException(AttributeError):
            pass
        breaker = self.breaker_with_allowed
        breaker._parse_exception(TestException)
        self.assertEqual(breaker._failure_count, 0)

    def test_init_failure(self):
        args = []
        kwargs = {
            "allowed_fails": DEFAULT_FAILS,
            "retry_time": DEFAULT_RETRY,
            "allowed_exceptions": [ValueError, AttributeError],
            "failure_exceptions": [KeyError]
        }
        self.assertRaises(ValueError, circuit_breaker.CircuitBreaker, *args, **kwargs)


if __name__ == '__main__':
    unittest.main()
