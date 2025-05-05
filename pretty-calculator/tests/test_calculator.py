import pytest
import math
from calculator.calculator import Calculator

@pytest.fixture
def calculator():
    return Calculator()

class TestCalculator:
    def test_addition(self, calculator):
        assert calculator.evaluate("2+3") == 5
    
    def test_subtraction(self, calculator):
        assert calculator.evaluate("5-3") == 2
    
    def test_multiplication(self, calculator):
        assert calculator.evaluate("4*5") == 20
    
    def test_division(self, calculator):
        assert calculator.evaluate("10/2") == 5
    
    def test_power(self, calculator):
        assert calculator.evaluate("2^3") == 8
    
    def test_multiple_operations(self, calculator):
        assert calculator.evaluate("2+3*4") == 14
        assert calculator.evaluate("(2+3)*4") == 20
    
    def test_sine_function_radians(self, calculator):
        calculator.set_angle_mode(False)  # Radians mode
        # Test sin(pi/2) which should be 1
        result = calculator.evaluate("sin(pi/2)")
        assert abs(result - 1) < 0.0001
    
    def test_sine_function_degrees(self, calculator):
        calculator.set_angle_mode(True)  # Degrees mode
        # Test sin(90) which should be 1
        result = calculator.evaluate("sin(90)")
        assert abs(result - 1) < 0.0001
    
    def test_cosine_function(self, calculator):
        calculator.set_angle_mode(False)  # Radians mode
        # Test cos(0) which should be 1
        result = calculator.evaluate("cos(0)")
        assert abs(result - 1) < 0.0001
    
    def test_tangent_function(self, calculator):
        calculator.set_angle_mode(False)  # Radians mode
        # Test tan(pi/4) which should be 1
        result = calculator.evaluate("tan(pi/4)")
        assert abs(result - 1) < 0.0001
    
    def test_sqrt_function(self, calculator):
        assert calculator.evaluate("sqrt(16)") == 4
    
    def test_log_function(self, calculator):
        assert calculator.evaluate("log(100)") == 2
    
    def test_ln_function(self, calculator):
        result = calculator.evaluate("ln(2.718281828459045)")
        assert abs(result - 1) < 0.0001
    
    def test_factorial_function(self, calculator):
        assert calculator.evaluate("factorial(5)") == 120
    
    def test_nested_functions(self, calculator):
        result = calculator.evaluate("sin(sqrt(9))")
        expected = math.sin(3)
        assert abs(result - expected) < 0.0001
    
    def test_error_handling(self, calculator):
        with pytest.raises(ValueError):
            calculator.evaluate("1/0")
        
        with pytest.raises(ValueError):
            calculator.evaluate("invalid_expression")
    
    def test_history(self, calculator):
        calculator.evaluate("2+3")
        calculator.evaluate("5*4")
        history = calculator.get_history()
        assert len(history) == 2
        assert history[0][0] == "2+3"
        assert history[0][1] == 5
        assert history[1][0] == "5*4"
        assert history[1][1] == 20
    
    def test_clear_history(self, calculator):
        calculator.evaluate("2+3")
        calculator.clear_history()
        assert len(calculator.get_history()) == 0