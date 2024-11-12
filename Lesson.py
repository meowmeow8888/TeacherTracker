from Teacher import Teacher

class Lesson:

    def __init__(self, subject: str, room: str, teacher: Teacher, hour: int):
        self.subject = subject
        self.room = room
        self.teacher = teacher
        self.hour = hour
    
    def __str__(self):
        return f"{self.teacher.name} is teaching {self.subject}, in room {self.room}, on the {self.hour} hour"

    def __eq__(self, other):
        return self.hour == other.hour and self.room == other.room and self.teacher == other.teacher and self.subject == other.subject