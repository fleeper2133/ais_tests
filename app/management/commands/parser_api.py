import os
import json
import django
from django.core.management.base import BaseCommand
from course.models import Question, Varient, Course, Qualification, Block, NormativeDocument, Testing
import requests
import datetime
import logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
django.setup()
HOST = "https://bp-cok.webworx.ru/api-exams/"
URLS = {
    "questions": HOST + "questions/",
    "qualifications": HOST + "qualifications/",
    "blocks": HOST + "blocks/",
    "ndocuments": HOST + "ndocuments/",
}
TOKEN = "7ed52887f5c6447bbaf51242e96b4a4a78d4111a"
HEADERS = {"Authorization": f"Token {TOKEN}"}


class Command(BaseCommand):
    help = "Парсинг вопросов и вариантов из API"

    def handle(self, *args, **kwargs):
        self.parse_qualifications(URLS['qualifications']) # Сначала создаём квалификации + курсы (возможно вручную)
        self.parse_blocks(URLS['blocks']) # потом докидываем блоки и доки
        self.parse_ndocuments(URLS['ndocuments'])
        self.parse_questions_variants(URLS["questions"]) # в конце парсим вопросы и ответы
    
    def parse_questions_variants(self, url):
        #Обработка ошибок???
        response = requests.get(url, headers=HEADERS)
        data = response.json()

        while True:
            questions = data.get("results", [])
            for question in questions:
                block_id = question['block']
                try:
                    block = Block.objects.get(pk=block_id)
                    qualification = Qualification.objects.get(pk=block.qualification_id)
                    course, created = Course.objects.get_or_create(
                        qualification=qualification,
                        defaults={
                            'name': qualification.title,
                            'description': f"Курс для квалификации {qualification.title}",
                            'version': "1.0",
                            'question_count': 0,
                            'available_until': datetime.datetime.today() + datetime.timedelta(days=365), #Иначе курс не доступен)
                        }
                    )
                    if created:
                        Testing.objects.create(
                            course=course,
                            description=f"Testing for {course}",
                            price=0,
                        )
                    main_question, _ = Question.objects.update_or_create(
                        pk=int(question["id"]),
                        defaults={
                            'question_text': question["text"],
                            'difficulty': "medium",
                            'name': f'{question["id"]} вопрос',
                            'topic': block.title[:250],
                            'course': course,
                            'block': block,
                            'ndocument_id': question['normative'],
                            "normative_point": question['normative_point']
                        }
                    )

                    for count, variant in enumerate(question['variants'], start=1):
                        Varient.objects.update_or_create(
                            pk=int(variant['id']),
                            defaults={
                                'answer_text': variant['text'],
                                'correct': variant['correct'],
                                'question': main_question,
                                'answer_number': count
                            }
                        )
                except Exception as e:
                    print(f"Ошибка при обработке запроса: {e}")

            next_page = data.get("next")
            print(next_page)
            if not next_page:
                break
            data = requests.get(next_page, headers=HEADERS).json()
        courses = Course.objects.all()
        for course in courses:
            course.update_question_count()

    def parse_qualifications(self, url):
        #обработка ошибок?
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        
        while True:
            qualifications = data["results"]
            for qual in qualifications:

                qualification_defaults = {
                'title': qual['full_title'] if qual['title'] != 'удалена' else qual['title'],
                'code': qual["nark_code"] if qual['title'] != 'удалена' else qual['code'],
                'level': int(qual["level"]) if qual['title'] != 'удалена' else 6
                }
                qualification, created = Qualification.objects.update_or_create(
                    pk=int(qual["id"]),
                    defaults=qualification_defaults
                )


                if created:
                    course_defaults = {
                        'name': qualification.title,
                        'description': f"Курс для квалификации {qualification.title}",
                        'version': "1.0",
                        'question_count': 0,
                        'available_until': datetime.datetime.today() + datetime.timedelta(days=365),
                    }
                    course, created_c = Course.objects.get_or_create(
                        qualification=qualification,
                        defaults=course_defaults
                    )
                    if created_c:
                        Testing.objects.create(
                            course=course,
                            description=f"Testing for {course}",
                            price=0,
                        )

            next_page = data.get("next")
            print(next_page)
            if not next_page:
                break
            data = requests.get(next_page, headers=HEADERS).json()

    def parse_blocks(self, url):
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        while True:
            blocks = data["results"]
            for block in blocks:
                Block.objects.update_or_create(
                    pk=int(block["id"]),
                    defaults={
                    'title': block['title'],
                    'qualification_id': block['qualification'] #здесь qual_id или qualification?
                                                        #в моделях qualification
                    }
                    
                )
            next_page = data.get("next")
            print(next_page)
            if not next_page:
                break
            data = requests.get(next_page, headers=HEADERS).json()

    def parse_ndocuments(self, url):
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        while True:
            ndocuments = data["results"]
            for ndoc in ndocuments:
                NormativeDocument.objects.update_or_create(
                    pk=int(ndoc["id"]),
                    defaults={
                    'text': ndoc['text'],
                    'is_active': ndoc['is_active']
                    }
                    
                )
            next_page = data.get("next")
            print(next_page)
            if not next_page:
                break
            data = requests.get(next_page, headers=HEADERS).json()