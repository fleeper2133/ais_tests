from django.contrib import admin
from usercourse.models import UserCourse, TaskQuestion, UserQuestion, UserTicket, UserAnswer,\
      QuestionTicket, UserCheckSkills, UserCheckSkillsQuestion

#admin.site.register(Profile)
admin.site.register(UserCourse)
admin.site.register(TaskQuestion)
admin.site.register(UserQuestion)
admin.site.register(UserTicket)
admin.site.register(UserAnswer)
admin.site.register(QuestionTicket)
admin.site.register(UserCheckSkills)
admin.site.register(UserCheckSkillsQuestion)