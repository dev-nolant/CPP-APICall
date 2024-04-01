from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sbac.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model for detections
class Detection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    recorded_time = db.Column(db.DateTime, default=datetime.utcnow)
    game_id = db.Column(db.String, nullable=False)

def initialize_database():
    with app.app_context():
        db.create_all()


@app.route('/detections', methods=['GET', 'POST'])
def detections():
    query = request.args.get('search', '')  # For GET requests
    if request.method == 'POST':
        query = request.form.get('search', '')  # For POST requests
    else:
        detections = Detection.query.all()
        return jsonify([{"id": detection.id, "ip": detection.ip, "username": detection.username, "description": detection.description, "recorded_time": detection.recorded_time, "game_id": detection.game_id} for detection in detections])


    
if __name__ == "__main__":
    initialize_database()  # Initialize the database before the Flask app starts accepting requests
    app.run(debug=True)
