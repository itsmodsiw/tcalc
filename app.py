from flask import Flask, render_template, request
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

if __name__ == "__main__":
    app.run(debug=True)