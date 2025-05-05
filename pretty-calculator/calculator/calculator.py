import math
import re

class Calculator:
    """Core calculator functionality for evaluating mathematical expressions."""
    
    def __init__(self):
        self.functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'sqrt': math.sqrt,
            'log': math.log10,
            'ln': math.log,
            'factorial': math.factorial,
            'pow': math.pow
        }
        self.history = []
        self.degrees_mode = False  # Default is radians
    
    def set_angle_mode(self, degrees=True):
        """Set angle mode to degrees or radians."""
        self.degrees_mode = degrees
    
    def _convert_angle_if_needed(self, angle, func_name):
        """Convert angle to radians if in degrees mode and function needs radians."""
        if self.degrees_mode and func_name in ['sin', 'cos', 'tan']:
            return math.radians(angle)
        return angle
    
    def _parse_function(self, expression):
        """Parse function calls in the expression."""
        pattern = r'([a-zA-Z]+)[(](.*?)[)]'
        match = re.search(pattern, expression)
        
        while match:
            func_name = match.group(1)
            args_str = match.group(2)
            
            if func_name not in self.functions:
                raise ValueError(f"Unknown function: {func_name}")
            
            # Recursively evaluate arguments
            args_value = self.evaluate(args_str)
            
            # Convert angle if needed
            args_value = self._convert_angle_if_needed(args_value, func_name)
            
            # Apply function
            result = self.functions[func_name](args_value)
            
            # Replace function call with result
            expression = expression.replace(f"{func_name}({args_str})", str(result))
            
            # Look for more functions
            match = re.search(pattern, expression)
        
        return expression
    
    def evaluate(self, expression):
        """Evaluate a mathematical expression."""
        # Remove spaces
        expression = expression.replace(' ', '')
        
        if not expression:
            return 0
        
        try:
            # Parse functions
            expression = self._parse_function(expression)
            
            # Replace ^ with **
            expression = expression.replace('^', '**')
            
            # Evaluate
            result = eval(expression, {"__builtins__": {}}, {
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "sqrt": math.sqrt,
                "log": math.log10,
                "ln": math.log,
                "factorial": math.factorial,
                "pow": math.pow,
                "pi": math.pi,
                "e": math.e
            })
            
            # Add to history
            self.history.append((expression, result))
            
            return result
        except Exception as e:
            raise ValueError(f"Error evaluating expression: {str(e)}")
    
    def get_history(self):
        """Return calculation history."""
        return self.history
    
    def clear_history(self):
        """Clear calculation history."""
        self.history = []