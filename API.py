from datetime import datetime
from flask import Flask, jsonify
from SchoolSchedule import SchoolSchedule
from Teacher import Teacher

day = (datetime.now().weekday()+2)%7

schedule = SchoolSchedule(day, "https://herzogks.iscool.co.il")
schedule.fetch_data()

app = Flask(__name__)

@app.route("/teacher/<string:teacher_name>/<int:hour>",methods=["GET"])
def get_room_for_teacher_and_hour(teacher_name:str, hour:int):
    return jsonify({"room":schedule.get_teacher_room_for_hour(Teacher(teacher_name),hour)})

@app.route("/empty-rooms/<int:hour>",methods=["GET"])
def get_empty_rooms_for_hour(hour:int):
    return jsonify({"emptyRooms":schedule.get_empty_rooms_for_hour(hour)})






app.run()