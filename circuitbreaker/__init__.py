import logging

from circuitbreaker import circuit_breaker

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
