from flask import render_template, request, jsonify
from calculator import app
from calculator.calculator import Calculator

calculator = Calculator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expression = data.get('expression', '')
    try:
        result = calculator.evaluate(expression)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400