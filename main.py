from flask import Flask, request, render_template
from sweater import SetInSleeveSweater
from cardigan import Cardigan

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_instructions():
    pattern_type = request.form.get('patternType')
    chest_circumference = float(request.form.get('chestCircumference'))
    gaugeStitches = float(request.form.get('gaugeS'))
    gaugeRows = float(request.form.get('gaugeR'))
    
    instructions = []

    if pattern_type == 'sweater':
        set_in_sleeve = SetInSleeveSweater(gaugeStitches, gaugeRows)
        set_in_sleeve.setup(chest_circumference)
        set_in_sleeve.printInstructions(instructions)

    elif pattern_type == 'cardigan':
        cardigan = Cardigan(gaugeStitches, gaugeRows)
        cardigan.setup(chest_circumference)
        cardigan.printInstructions(instructions)

    return render_template('result.html', instructions=instructions)

if __name__ == '__main__':
    app.run(debug=True)
