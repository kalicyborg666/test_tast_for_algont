import time
from flask import Flask, render_template, jsonify
import psutil
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cpu_load.db'
db = SQLAlchemy(app)


class CpuLoad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer)
    load = db.Column(db.Float)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/load-data')
def get_load_data():
    cpu_loads = CpuLoad.query.all()
    data = [{'timestamp': load.timestamp * 1000, 'load': load.load} for load in
            cpu_loads]
    return jsonify(data)


@app.route('/update-data')
def update_data():
    load = psutil.cpu_percent(interval=1)
    timestamp = int(time.time())
    cpu_load = CpuLoad(timestamp=timestamp, load=load)
    db.session.add(cpu_load)
    db.session.commit()
    return "Data updated"


if __name__ == '__main__':
    app.run(port=8000)
