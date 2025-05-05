document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const expressionEl = document.getElementById('expression');
    const resultEl = document.getElementById('result');
    const historyListEl = document.getElementById('historyList');
    const modeIndicatorEl = document.getElementById('modeIndicator');
    
    // State
    let currentExpression = '';
    let currentResult = null;
    let memory = 0;
    let inDegreesMode = false;
    
    // Function to update the display
    function updateDisplay() {
        expressionEl.textContent = currentExpression;
        resultEl.textContent = currentResult !== null ? currentResult : '0';
    }
    
    // Function to append to expression
    function appendToExpression(value) {
        if (currentResult !== null && !isOperator(value) && !isFunction(value)) {
            // Start a new expression if result is showing and not appending an operator
            currentExpression = value;
            currentResult = null;
        } else {
            currentExpression += value;
        }
        updateDisplay();
    }
    
    // Check if a value is an operator
    function isOperator(value) {
        return ['+', '-', '×', '÷', '^'].includes(value);
    }
    
    // Check if a value is a function
    function isFunction(value) {
        return ['sin(', 'cos(', 'tan(', 'log(', 'ln(', 'sqrt('].includes(value);
    }
    
    // Calculate expression
    function calculate() {
        if (!currentExpression) return;
        
        // Format the expression for the backend
        let expressionForEval = currentExpression
            .replace(/×/g, '*')
            .replace(/÷/g, '/')
            .replace(/π/g, 'pi')
            .replace(/\^/g, '**');
        
        // Send to backend
        fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ expression: expressionForEval, degrees: inDegreesMode }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                currentResult = 'Error';
                console.error(data.error);
            } else {
                currentResult = data.result;
                addToHistory(currentExpression, currentResult);
            }
            updateDisplay();
        })
        .catch(error => {
            currentResult = 'Error';
            console.error('Calculation error:', error);
            updateDisplay();
        });
    }
    
    // Add calculation to history
    function addToHistory(expression, result) {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        historyItem.innerHTML = `
            <span class="history-expression">${expression}</span>
            <span class="history-result">${result}</span>
        `;
        historyListEl.prepend(historyItem);
    }
    
    // Clear history
    function clearHistory() {
        historyListEl.innerHTML = '';
    }
    
    // Toggle between radians and degrees
    function toggleAngleMode() {
        inDegreesMode = !inDegreesMode;
        modeIndicatorEl.textContent = inDegreesMode ? 'DEG' : 'RAD';
    }
    
    // Set up button click handlers
    document.querySelectorAll('.number, .decimal').forEach(button => {
        button.addEventListener('click', function() {
            appendToExpression(this.textContent);
        });
    });
    
    document.querySelectorAll('.operator').forEach(button => {
        button.addEventListener('click', function() {
            const operatorMap = {
                '+': '+',
                '-': '-',
                '×': '×',
                '÷': '÷',
                'x^y': '^'
            };
            const operator = operatorMap[this.textContent] || this.id;
            appendToExpression(operator);
        });
    });
    
    document.querySelectorAll('.function').forEach(button => {
        button.addEventListener('click', function() {
            const functionMap = {
                'sin': 'sin(',
                'cos': 'cos(',
                'tan': 'tan(',
                'log': 'log(',
                'ln': 'ln(',
                '√': 'sqrt(',
                '!': 'factorial('
            };
            
            if (this.id in functionMap) {
                appendToExpression(functionMap[this.id]);
            }
        });
    });
    
    // Memory operations
    document.getElementById('mClear').addEventListener('click', function() {
        memory = 0;
    });
    
    document.getElementById('mRecall').addEventListener('click', function() {
        appendToExpression(memory.toString());
    });
    
    document.getElementById('mAdd').addEventListener('click', function() {
        if (currentResult !== null) {
            memory += parseFloat(currentResult);
        }
    });
    
    document.getElementById('mSubtract').addEventListener('click', function() {
        if (currentResult !== null) {
            memory -= parseFloat(currentResult);
        }
    });
    
    // Special buttons
    document.getElementById('equals').addEventListener('click', calculate);
    
    document.getElementById('clear').addEventListener('click', function() {
        currentExpression = '';
        updateDisplay();
    });
    
    document.getElementById('clearAll').addEventListener('click', function() {
        currentExpression = '';
        currentResult = null;
        updateDisplay();
    });
    
    document.getElementById('pi').addEventListener('click', function() {
        appendToExpression('π');
    });
    
    document.getElementById('toggleMode').addEventListener('click', toggleAngleMode);
    
    document.getElementById('clearHistory').addEventListener('click', clearHistory);
    
    // Keyboard support
    document.addEventListener('keydown', function(event) {
        const key = event.key;
        
        // Number keys
        if (/^[0-9]$/.test(key)) {
            appendToExpression(key);
        }
        // Operators
        else if (['+', '-', '*', '/'].includes(key)) {
            const operatorMap = {
                '*': '×',
                '/': '÷'
            };
            appendToExpression(operatorMap[key] || key);
        }
        // Decimal point
        else if (key === '.') {
            appendToExpression('.');
        }
        // Enter/Equal key
        else if (key === 'Enter') {
            calculate();
        }
        // Backspace
        else if (key === 'Backspace') {
            currentExpression = currentExpression.slice(0, -1);
            updateDisplay();
        }
        // Clear
        else if (key === 'Escape') {
            currentExpression = '';
            updateDisplay();
        }
        // Parentheses
        else if (key === '(' || key === ')') {
            appendToExpression(key);
        }
    });
    
    // Initialize display
    updateDisplay();
});