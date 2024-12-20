from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
from SchoolSchedule import SchoolSchedule
from Teacher import Teacher

day = (datetime.now().weekday()+2)%7

schedule = SchoolSchedule(day, "https://herzogks.iscool.co.il")
schedule.fetch_data()

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "teacher-tracker.netlify.app"])

@app.route("/teacher/<string:teacher_name>/<int:hour>",methods=["GET"])
def get_room_for_teacher_and_hour(teacher_name:str, hour:int):
    return jsonify({"room":schedule.get_teacher_room_for_hour(Teacher(teacher_name),hour)})

@app.route("/empty-rooms/<int:hour>",methods=["GET"])
def get_empty_rooms_for_hour(hour:int):
    return jsonify({"empty-rooms":schedule.get_empty_rooms_for_hour(hour)})

@app.route("/teachers",methods=["GET"])
def get_teachers():
    return jsonify({"teachers":list(schedule.teacher_map.keys())})

app.run()
