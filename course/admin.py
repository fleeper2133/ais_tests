from django.contrib import admin
from course.models import Course, Testing, Ticket, Question, QuestionList, Varient, LearningMaterial, \
                            Block, NormativeDocument, Qualification

admin.site.register(Course)
admin.site.register(Testing)
admin.site.register(Ticket) 
admin.site.register(Question)
admin.site.register(Varient)
admin.site.register(QuestionList)
admin.site.register(LearningMaterial)
admin.site.register(Block)
admin.site.register(NormativeDocument)
admin.site.register(Qualification) 