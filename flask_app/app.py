from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Check if the request is JSON (for AJAX)
        if request.is_json:
            data = request.get_json()
            name = data.get('name')
            if name:
                return jsonify({'greeting': f"Hello, {name}!"})
            return jsonify({'greeting': ''})

        # Fallback for standard form submission
        name = request.form.get('name')
        greeting = ""
        if name:
            greeting = f"Hello, {name}!"
        return render_template('index.html', greeting=greeting)

    return render_template('index.html', greeting="")

@app.route('/bolt')
def bolt():
    return render_template('bolt.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
