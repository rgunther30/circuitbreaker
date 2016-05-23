import unittest
import time

import circuit_breaker


DEFAULT_FAILS = 3
DEFAULT_RETRY = 1


class TestBreaker(unittest.TestCase):
    def setUp(self):
        self.breaker = circuit_breaker.CircuitBreaker(
            allowed_fails=DEFAULT_FAILS,
            retry_time=DEFAULT_RETRY,
            validation_func=None
        )
        self.breaker_with_validation = circuit_breaker.CircuitBreaker(
            allowed_fails=DEFAULT_FAILS,
            retry_time=DEFAULT_RETRY
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


if __name__ == '__main__':
    unittest.main()
