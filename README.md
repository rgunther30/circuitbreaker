# circuitbreaker
[![Build Status](https://travis-ci.org/rgunther30/circuitbreaker.svg?branch=master)](https://travis-ci.org/rgunther30/circuitbreaker)

Python implementation of circuit breaker to protect systems from failures

Inspired by a presentation at Boston Python User Group given by Dan Riti.

Circuit breakers allow for graceful degradation of services, while also protecting the ailing service from 
being overloaded further. Circuit breakers are finite state machines that check for successes and failures 
on the things they wrap around. Once a certain number of consecutive fails is reached, the circuit breaker 
pops open, preventing any further traffic (current) through. Once a predetermined retry time has passed, the
braker enters a half open state. In this half open state, a single request is allowed through to test the health
of the remote service. If the request fails, we return to the open state, but if the request succeeds, we transition
back to the closed (healthy) state. 

To use this, simply use this as a decorator on a function you would normally use to make requests with:
```python
@circuit_breaker(allowed_fails=3, retry_timer=30)
def request_something():
    # do something...
```

You may also pass a validator function that checks the result of the function and returns a boolean value 
to determine if the return value of our function was permissible or not. This is a contrived example and
terrible practice, but for the sake of demonstration:
```python
def validator(response):
    return response.status_code >= 300
    
@circuit_breaker(allowed_fails=3, retry_timer=30, validation_func=validator)
def request_something()
    # do something ...
    return response
```

In some applications, we may know what type of exceptions can be thrown during the execution of our function.
If the exceptions are expected, and not a cause of alarm, we can pass a list of allowed exceptions as a kwarg
to the initializer of the circuit breaker. These will not increment the failure counter and thus have no
effect on the state of the breaker. They are logged however, so they are not completely ignored. An example of
allowed exceptions:
```python
@circuit_breaker(allowed_fails=3, retry_timer=60, allowed_exceptions=[KeyError, ConnectTimeout])
def request_something():
    # do something...
```

In some cases, we might be fine with many exceptions, but only have a few failures we care about. In this case
we can pass a list of explicit failures to the initializer. In this case, only these exceptions will be 
considered failures. All other exceptions caught by the circuit breaker will be logged, however.
```python
@circuit_breaker(failure_exceptions=[KeyError, RequestException])
def request_something():
    # do something...
```
