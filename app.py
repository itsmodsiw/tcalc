from flask import Flask, render_template, request, jsonify
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        timezone = request.form.get('timezone')
        date = request.form.get('date')
        time = request.form.get('time')

        dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        dt = pytz.timezone(timezone).localize(dt)

        unix_time = int(dt.timestamp())

        return render_template('result.html', unix_time=unix_time)

    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()  # Get the JSON data sent from the frontend
    datetime_str = data['datetime']  # Extract the datetime string

    # Parse the datetime string and convert to Unix timestamp...
    dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M")
    unix_timestamp = int(dt.timestamp())

    # Send the Unix timestamp back to the frontend as JSON
    return jsonify({'timestamp': unix_timestamp})

if __name__ == "__main__":
    app.run(debug=True)
