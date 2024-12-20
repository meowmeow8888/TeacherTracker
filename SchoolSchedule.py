import time
from requests import Response
from Lesson import Lesson
from Teacher import Teacher
from bs4 import BeautifulSoup as bs
import requests as rs
from fake_useragent import UserAgent

class SchoolSchedule:

    def __init__(self, school_day: int, school_url: str):
        self.school_day = school_day - 1
        self.school_url = school_url + ("/" if school_url[-1] != "/" else "") + "default.aspx"
        self.hour_map: dict[int, list[Lesson]] = { }
        self.teacher_map: dict[str , list[Lesson]] = {}
        self.rooms_list = []
        self.session = rs.Session()
        self.ua = UserAgent()


    def __get_class_count(self):
        res = Response()
        while res.status_code !=200:
            res = self.session.post(
                self.school_url,
                headers={
                    "user-agent": self.ua.random

                },
                data="""------WebKitFormBoundary9Wiees6OIfqkMkFY\r\nContent-Disposition: form-data; name=\"__EVENTTARGET\"\r\n\r\ndnn$ctr16470$TimeTableView$btnTimeTable\r\n------WebKitFormBoundary9Wiees6OIfqkMkFY\r\nContent-Disposition: form-data; name=\"__EVENTARGUMENT\"\r\n\r\n\r\n------WebKitFormBoundary9Wiees6OIfqkMkFY\r\nContent-Disposition: form-data; name=\"__LASTFOCUS\"\r\n\r\n\r\n------WebKitFormBoundary9Wiees6OIfqkMkFY\r\nContent-Disposition: form-data; name=\"__VIEWSTATE\"\r\n\r\n/wEPDwUIMjU3MTQzOTcPZBYGZg8WAh4EVGV4dAU+PCFET0NUWVBFIEhUTUwgUFVCTElDICItLy9XM0MvL0RURCBIVE1MIDQuMCBUcmFuc2l0aW9uYWwvL0VOIj5kAgEPZBYMAgEPFgIeB1Zpc2libGVoZAICDxYCHgdjb250ZW50BRjXlNeo16bXldeSINeb16TXqCDXodeR15BkAgMPFgIfAgUn15TXqNem15XXkiDXm9ek16gg16HXkdeQLERvdE5ldE51a2UsRE5OZAIEDxYCHwIFINeb15wg15TXlteb15XXmdeV16og16nXnteV16jXldeqZAIFDxYCHwIFC0RvdE5ldE51a2UgZAIGDxYCHwIFGNeU16jXpteV15Ig15vXpNeoINeh15HXkGQCAg9kFgJmD2QWAgIED2QWAmYPZBYGAgIPZBYCZg8PFgYeCENzc0NsYXNzBQtza2luY29sdHJvbB4EXyFTQgICHwFoZGQCAw9kFgJmDw8WBh8DBQtza2luY29sdHJvbB8ABRfXm9eg15nXodeUINec157Xoteo15vXqh8EAgJkZAIKD2QWAgICD2QWCAIBDw8WAh8BaGRkAgMPDxYCHwFoZGQCBQ9kFgICAg8WAh8BaGQCBw9kFgICAQ9kFgICAQ9kFgwCBg9kFgJmD2QWDAICDxYCHgVjbGFzcwUKSGVhZGVyQ2VsbGQCBA8WAh8FBQpIZWFkZXJDZWxsZAIGDxYCHwUFCkhlYWRlckNlbGxkAggPFgIfBQUKSGVhZGVyQ2VsbGQCCg8WAh8FBQpIZWFkZXJDZWxsZAIMDxYCHwUFEEhlYWRlckNlbGxCdXR0b25kAgcPEGQQFQAVABQrAwBkZAIJDxYCHwFoZAILDxYCHwFoZAIMD2QWAmYPZBYcZg9kFgICAQ8QZBAVGwPXmTED15kyA9eZMwPXmTQD15k1A9eZNgPXmTcD15k4A9eZOQXXmdeQMQXXmdeQMgXXmdeQMwXXmdeQNAXXmdeQNQXXmdeQNgXXmdeQNwXXmdeQOAXXmdeQOQXXmdeRMQXXmdeRMgXXmdeRMwXXmdeRNAXXmdeRNQXXmdeRNgXXmdeRNwXXmdeROAXXmdeRORUbATEBMgEzATQBNQE2AjI2AjI4AjM1ATkCMTACMTECMTICMTMCMTQCMTUCMjkCMzYCMTYCMTcCMTgCMTkCMjACMjECMjICMzACMzQUKwMbZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnFgECDGQCAg8WBB8FBQpIZWFkZXJDZWxsHwFoZAIDDxYCHwFoZAIEDxYCHwUFCkhlYWRlckNlbGxkAgYPFgQfBQUKSGVhZGVyQ2VsbB8BaGQCBw8WAh8BaGQCCA8WAh8FBQpIZWFkZXJDZWxsZAIKDxYCHwUFCkhlYWRlckNlbGxkAgwPFgIfBQUKSGVhZGVyQ2VsbGQCDg8WAh8FBQpIZWFkZXJDZWxsZAIQDxYCHwUFCkhlYWRlckNlbGxkAhIPFgQfBQUKSGVhZGVyQ2VsbB8BaGQCEw8WAh8BaGQCFA8WBB8FBRBIZWFkZXJDZWxsQnV0dG9uHwFoZAIPDw8WAh8ABTvXntei15XXk9eb158g15w6IDIwLjEyLjIwMjQsINep16LXlDogMTI6MTcsINee16HXmjogQTExNjQ3MGRkZFvhyQkNvsVpy92B6ann4tPCYY4J\r\n------WebKitFormBoundary9Wiees6OIfqkMkFY\r\nContent-Disposition: form-data; name=\"__VIEWSTATEGENERATOR\"\r\n\r\nCA0B0334\r\n------WebKitFormBoundary9Wiees6OIfqkMkFY\r\nContent-Disposition: form-data; name=\"dnn$ctr16470$TimeTableView$ClassesList\"\r\n\r\n0\r\n------WebKitFormBoundary9Wiees6OIfqkMkFY\r\nContent-Disposition: form-data; name=\"dnn$ctr16470$TimeTableView$ControlId\"\r\n\r\n\r\n------WebKitFormBoundary9Wiees6OIfqkMkFY\r\nContent-Disposition: form-data; name=\"ScrollTop\"\r\n\r\n\r\n------WebKitFormBoundary9Wiees6OIfqkMkFY\r\nContent-Disposition: form-data; name=\"__dnnVariable\"\r\n\r\n\r\n------WebKitFormBoundary9Wiees6OIfqkMkFY--\r\n""",
            )
            if res.status_code == 200:
                print("googy")
                break
            print(self.school_url,res.status_code)
            time.sleep(0.5)

        soup = bs(res.content, "html.parser")
        classes = soup.find_all("option")
        return len(classes)

    def __parse_class_schedule(self, soup):
        all_lessons = [x for i,x in enumerate(soup.find_all("td", "TTCell")) if i%6==self.school_day]
        lesson_list = []
        for index, lessons in enumerate(all_lessons):
            subjects = [b.next_element for b in lessons.find_all('b')]
            classrooms = ["-1" if str(s.next_element)[3:6] == '/>' else str(s.next_element)[3:6] for s in subjects]
            for classroom in classrooms:
                if classroom[-1] == ')':
                    classroom = classroom[:2]
                if classroom not in self.rooms_list:
                    self.rooms_list.append(classroom)
            teachers = [Teacher(s.next_element.next_element) if str(s.next_element)[3:6] == '/>' else Teacher(str(s.next_element.next_element.next_element)) for s in subjects]
            for subject, room, teacher in zip(subjects, classrooms, teachers):
                lesson_list.append(Lesson(subject, room, teacher, index))
        return lesson_list

    def fetch_data(self):
        for i in range(1,self.__get_class_count()+1):
            res = Response()
            while res.status_code != 200:
                res = self.session.post(self.school_url,
                              headers={
                                  "user-agent": self.ua.random
                              },
                              data=f"------WebKitFormBoundary4yuhil16pTgADnUF\r\nContent-Disposition: form-data; name=\"__EVENTTARGET\"\r\n\r\ndnn$ctr16470$TimeTableView$btnTimeTable\r\n------WebKitFormBoundary4yuhil16pTgADnUF\r\nContent-Disposition: form-data; name=\"__EVENTARGUMENT\"\r\n\r\n\r\n------WebKitFormBoundary4yuhil16pTgADnUF\r\nContent-Disposition: form-data; name=\"__LASTFOCUS\"\r\n\r\n\r\n------WebKitFormBoundary4yuhil16pTgADnUF\r\nContent-Disposition: form-data; name=\"__VIEWSTATE\"\r\n\r\n/wEPDwUIMjU3MTQzOTcPZBYGZg8WAh4EVGV4dAU+PCFET0NUWVBFIEhUTUwgUFVCTElDICItLy9XM0MvL0RURCBIVE1MIDQuMCBUcmFuc2l0aW9uYWwvL0VOIj5kAgEPZBYMAgEPFgIeB1Zpc2libGVoZAICDxYCHgdjb250ZW50BRjXlNeo16bXldeSINeb16TXqCDXodeR15BkAgMPFgIfAgUn15TXqNem15XXkiDXm9ek16gg16HXkdeQLERvdE5ldE51a2UsRE5OZAIEDxYCHwIFINeb15wg15TXlteb15XXmdeV16og16nXnteV16jXldeqZAIFDxYCHwIFC0RvdE5ldE51a2UgZAIGDxYCHwIFGNeU16jXpteV15Ig15vXpNeoINeh15HXkGQCAg9kFgJmD2QWAgIED2QWAmYPZBYGAgIPZBYCZg8PFgYeCENzc0NsYXNzBQtza2luY29sdHJvbB4EXyFTQgICHwFoZGQCAw9kFgJmDw8WBh8DBQtza2luY29sdHJvbB8ABRfXm9eg15nXodeUINec157Xoteo15vXqh8EAgJkZAIKD2QWAgICD2QWCAIBDw8WAh8BaGRkAgMPDxYCHwFoZGQCBQ9kFgICAg8WAh8BaGQCBw9kFgICAQ9kFgICAQ9kFgwCBg9kFgJmD2QWDAICDxYCHgVjbGFzcwUKSGVhZGVyQ2VsbGQCBA8WAh8FBQpIZWFkZXJDZWxsZAIGDxYCHwUFCkhlYWRlckNlbGxkAggPFgIfBQUKSGVhZGVyQ2VsbGQCCg8WAh8FBQpIZWFkZXJDZWxsZAIMDxYCHwUFEEhlYWRlckNlbGxCdXR0b25kAgcPEGQQFQAVABQrAwBkZAIJDxYCHwFoZAILDxYCHwFoZAIMD2QWAmYPZBYcZg9kFgICAQ8QZBAVGwPXmTED15kyA9eZMwPXmTQD15k1A9eZNgPXmTcD15k4A9eZOQXXmdeQMQXXmdeQMgXXmdeQMwXXmdeQNAXXmdeQNQXXmdeQNgXXmdeQNwXXmdeQOAXXmdeQOQXXmdeRMQXXmdeRMgXXmdeRMwXXmdeRNAXXmdeRNQXXmdeRNgXXmdeRNwXXmdeROAXXmdeRORUbATEBMgEzATQBNQE2AjI2AjI4AjM1ATkCMTACMTECMTICMTMCMTQCMTUCMjkCMzYCMTYCMTcCMTgCMTkCMjACMjECMjICMzACMzQUKwMbZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnFgECDWQCAg8WBB8FBQpIZWFkZXJDZWxsHwFoZAIDDxYCHwFoZAIEDxYCHwUFCkhlYWRlckNlbGxkAgYPFgQfBQUKSGVhZGVyQ2VsbB8BaGQCBw8WAh8BaGQCCA8WAh8FBQpIZWFkZXJDZWxsZAIKDxYCHwUFCkhlYWRlckNlbGxkAgwPFgIfBQUKSGVhZGVyQ2VsbGQCDg8WAh8FBQpIZWFkZXJDZWxsZAIQDxYCHwUFCkhlYWRlckNlbGxkAhIPFgQfBQUKSGVhZGVyQ2VsbB8BaGQCEw8WAh8BaGQCFA8WBB8FBRBIZWFkZXJDZWxsQnV0dG9uHwFoZAIPDw8WAh8ABTvXntei15XXk9eb158g15w6IDEwLjEwLjIwMjQsINep16LXlDogMDk6MzIsINee16HXmjogQTExNjQ3MGRkZHrlE4HhIFBwGyXo2EHZ4PS3Kirr\r\n------WebKitFormBoundary4yuhil16pTgADnUF\r\nContent-Disposition: form-data; name=\"__VIEWSTATEGENERATOR\"\r\n\r\nCA0B0334\r\n------WebKitFormBoundary4yuhil16pTgADnUF\r\nContent-Disposition: form-data; name=\"dnn$ctr16470$TimeTableView$ClassesList\"\r\n\r\n{i}\r\n------WebKitFormBoundary4yuhil16pTgADnUF\r\nContent-Disposition: form-data; name=\"dnn$ctr16470$TimeTableView$ControlId\"\r\n\r\n\r\n------WebKitFormBoundary4yuhil16pTgADnUF\r\nContent-Disposition: form-data; name=\"ScrollTop\"\r\n\r\n\r\n------WebKitFormBoundary4yuhil16pTgADnUF\r\nContent-Disposition: form-data; name=\"__dnnVariable\"\r\n\r\n\r\n------WebKitFormBoundary4yuhil16pTgADnUF--\r\n"
                              )
                if res.status_code == 200:
                    print("goog")
                    break
                print("notgoog")
                time.sleep(0.5)

            soup = bs(res.content, "html.parser")
            lesson_list = self.__parse_class_schedule(soup)
            for lesson in lesson_list:
                self.hour_map.setdefault(lesson.hour, [])
                if lesson not in self.hour_map[lesson.hour]:
                    self.hour_map[lesson.hour].append(lesson)
                self.teacher_map.setdefault(lesson.teacher.name, []).append(lesson)



    def get_lessons_for_hour(self, hour):
        if hour in self.hour_map.keys():
            return self.hour_map[hour]
        return None

    def get_teacher_room_for_hour(self, teacher: Teacher, hour: int):
        if teacher.name not in self.teacher_map:
            return 0
        for lesson in self.teacher_map[teacher.name]:
            if lesson.hour == hour:
                return lesson.room
        return None

    def get_empty_rooms_for_hour(self,hour):
        occupied_rooms = []
        for lesson in self.hour_map[hour]:
            if lesson.room not in occupied_rooms:
                occupied_rooms.append(lesson.room)
        empty_rooms = []
        for room in self.rooms_list:
            if room not in occupied_rooms:
                empty_rooms.append(room)
        return empty_rooms