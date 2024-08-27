from users.views import LoginAPIView, LogoutAPIView, RegistrationAPIView, SendMail, CreateUserAPIView
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include
from rest_framework import routers
from .views import QualificationViewSet, BlockViewSet, NormativeDocumentViewSet, CourseViewSet, TestingViewSet, TicketViewSet, QuestionViewSet, VarientViewSet, QuestionListViewSet, LearningMaterialViewSet
from .views import UserCourseViewSet, TaskQuestionViewSet, UserQuestionViewSet, UserTicketViewSet, UserAnswerViewSet, UserAnswerItemViewSet, QuestionTicketViewSet, UserCheckSkillsViewSet, UserCheckSkillsQuestionViewSet
from .views import UserDaysViewSet

router = routers.DefaultRouter()

router.register(r'user-days', UserDaysViewSet)
router.register(r'qualifications', QualificationViewSet)
router.register(r'blocks', BlockViewSet)
router.register(r'normative-documents', NormativeDocumentViewSet)
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'testings', TestingViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'varients', VarientViewSet)
router.register(r'question-lists', QuestionListViewSet)
router.register(r'learning-materials', LearningMaterialViewSet)
# --------------------------------------------------------------------
router.register(r'user-courses', UserCourseViewSet)
router.register(r'task-questions', TaskQuestionViewSet)
router.register(r'user-questions', UserQuestionViewSet)
router.register(r'user-tickets', UserTicketViewSet)
router.register(r'user-answers', UserAnswerViewSet)
router.register(r'user-answer-items', UserAnswerItemViewSet)
router.register(r'question-tickets', QuestionTicketViewSet)
router.register(r'user-check-skills', UserCheckSkillsViewSet)
router.register(r'user-check-skills-questions', UserCheckSkillsQuestionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("registration/", RegistrationAPIView.as_view(), name="registration"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('send-mail/', SendMail.as_view(), name="send_mail"),
    path('create-user/', CreateUserAPIView.as_view(), name="create_user")
]