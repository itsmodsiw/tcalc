from flask import Flask, render_template, request, jsonify
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        datetime_str = data['datetime']
        timezone_str = data['timezone']

        dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M")
        dt = pytz.timezone(timezone_str).localize(dt)
        unix_timestamp = int(dt.timestamp())

        return jsonify({'timestamp': unix_timestamp})
    except Exception as e:
        error_message = "An error occurred during the conversion: " + str(e)
        return jsonify({'error': error_message}), 500

if __name__ == "__main__":
    app.run(debug=True)
