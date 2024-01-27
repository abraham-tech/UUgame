### Language
All code and comments should be in English.

### Comments
All functions should be documented.

### Indentation rules
Tab length: 4 spaces

### Python naming
function_number_one()  
variable_number_one  
ClassNumberOne

### Pull requests
Each pull request should only complete one task  
The name of each pull request should contain the ID of the task in Trello

### Python code examples
```python
def complex(real=0.0, imag=0.0):
    """
    Form a complex number
    
    Keyword arguments:
    real -- the real part (default 0.0)
    imag -- the imaginary part (default 0.0)
    
    Returns:
    counter – counter from loop
    """
    
    if imag == 0.0 and real == 0.0: 
        return complex_zero
```  
  
```python
import abc

class Payable(metaclass=abc.ABCMeta):
    """
    Defines the interface of payable objects.
    """
    
    @abc.abstractsmethod
    def get_payment_amount(self):
    pass

class Employee(Payable):
    """
    Defines an employee as a payable object.
    """
    
    def __init__(self, first_name, last_name, social_security_number):
        self._first_name = first_name
        self._last_name = last_name
        self._social_security_number = social_security_number
        
    def get_payment_amount(self):
        pass
```

```python
class Singleton(type):
    """
    Define an Instance operation that lets clients access its instance.
    """
    
    def __init__(cls, name, bases, attrs, **kwargs):
      super().__init__(name, bases, attrs)
      cls._instance = None
    
    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

class Board(metaclass=Singleton)
    """
    Example class.
    """
    
    pass
```
