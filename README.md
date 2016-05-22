# circuitbreaker
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
@CircuitBreaker(allowed_fails=3, retry_timer=30)
def request_something():
    # do something...
```

You may also pass a validator function that checks the result of the function and returns a boolean value 
to determine if the return value of our function was permissible or not. This is a contrived example and
terrible practice, but for the sake of demonstration:
```python
def validator(response):
    return response.status_code >= 300
    
@CircuitBreaker(allowed_fails=3, retry_timer=30, validation_func=validator)
def request_something()
    # do something ...
    return response

