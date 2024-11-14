from django.urls import path, include
from .views import *
from .metaviews import *
from rest_framework.routers import DefaultRouter
from .singleviews import *
from .metaviews import *

# router for single request
router = DefaultRouter()
 
# single request for creating and get all user details by List
router.register(r'save-profile', SaveDataCreateListViewSet, basename='save-profile')

 # job posting
router.register(r'posting', JobProstingViewSet, basename='posting')
router.register(r'notifications', NotificationListView)

app_name = "common"
API_URL_PREFIX = "api/"


urlpatterns = [
    path(f"{API_URL_PREFIX}change-password/", ChangePasswordView.as_view()), # change password
    path(f"{API_URL_PREFIX}custom-token-auth/", CustomAuthToken.as_view()), # generate token

    # country
    path(f"{API_URL_PREFIX}countries/", CountryListCreateAPIView.as_view()), 
    path(f"{API_URL_PREFIX}countries/<int:id>/", CountryDetailAPIView.as_view()),

    # state
    path(f"{API_URL_PREFIX}states/", StateListCreateAPIView.as_view()),
    path(f"{API_URL_PREFIX}states/<int:id>/", StateDetailAPIView.as_view()), 
    path(f"{API_URL_PREFIX}cities/", CityListCreateAPIView.as_view()), 

    # city
    path(f"{API_URL_PREFIX}cities/", CityListCreateAPIView.as_view()),
    path(f"{API_URL_PREFIX}cities/<int:id>/", CityDetailAPIView.as_view()), 
    

    # personal detail
    path(f"{API_URL_PREFIX}user/", UserListCreateAPIView.as_view()), 
    path(f"{API_URL_PREFIX}user/<int:id>/", UserDetailAPIView.as_view()),

    # degree 
    path(f"{API_URL_PREFIX}degrees/", DegreeListCreateAPIView.as_view()), 
    path(f"{API_URL_PREFIX}degrees/<int:id>/", DegreeDetailAPIView.as_view()),

    # certificate
    path(f"{API_URL_PREFIX}certificates/", CertificationsListCreateAPIView.as_view()), 
    path(f"{API_URL_PREFIX}certificates/<int:id>/", CertificationDetailAPIView.as_view()), 

    # education and certificate
    path(f"{API_URL_PREFIX}educationsandcertificates/", EducationAndCertificationsListCreateAPIView.as_view()), 
    path(f"{API_URL_PREFIX}educationsandcertificates/<int:id>/", EducationAndCertificationsDetailAPIView.as_view()),
    
    # skills 
    path(f"{API_URL_PREFIX}skills/", SkillsListCreateAPIView.as_view()),
    path(f"{API_URL_PREFIX}skills/<int:id>/", SkillsDetailAPIView.as_view()),

    # work details
    path(f"{API_URL_PREFIX}workdetails/", WorkDetailsListCreateAPIView.as_view()),
    path(f"{API_URL_PREFIX}workdetails/<int:id>/", WorkDetailsDetailAPIView.as_view()),

    # employement history
    path(f"{API_URL_PREFIX}employmenthistory/", EmploymentHistoryListCreateAPIView.as_view()),
    path(f"{API_URL_PREFIX}employmenthistory/<int:id>/", EmploymentHistoryDetailAPIView.as_view()), 

    # awards 
    path(f"{API_URL_PREFIX}awards/", AwardsListCreateAPIView.as_view()),
    path(f"{API_URL_PREFIX}awards/<int:id>/", AwardDetailAPIView.as_view()),

    # industry
    path(f"{API_URL_PREFIX}industries/", IndustryListCreateAPIView.as_view()),
    path(f"{API_URL_PREFIX}industries/<int:id>/", IndustryDetailAPIView.as_view()),

    # salary
    path(f"{API_URL_PREFIX}salaryexpectations/", SalaryExceptationListCreateAPIView.as_view()),
    path(f"{API_URL_PREFIX}salaryexpectations/<int:id>/", SalaryExceptationsDetailAPIView.as_view()),

    # preferences
    path(f"{API_URL_PREFIX}preferences/", PreferencesListCreateAPIView.as_view()),
    path(f"{API_URL_PREFIX}preferences/<int:id>/", PreferencesDetailAPIView.as_view()),

    # user detail view by id
    path(f"{API_URL_PREFIX}users-details/<int:id>/", UserAllDetailsAPIView.as_view()),

    # export all the details
    path(f"{API_URL_PREFIX}export_user_data/<int:id>/", ExportUserDataView.as_view()),
    
    # bulk upload
    path(f"{API_URL_PREFIX}upload-countries/", CountryCSVUploadView.as_view()),
    path(f"{API_URL_PREFIX}upload-states/", StateCSVUploadView.as_view()),
    path(f"{API_URL_PREFIX}upload-cities/", CityCSVUploadView.as_view()),
    path(f"{API_URL_PREFIX}upload-degree/", DegreeCSVUploadView.as_view()),
    path(f"{API_URL_PREFIX}upload-skills/", SkillsCSVUploadView.as_view()),
    path(f"{API_URL_PREFIX}upload-industry/", IndustryCSVUploadView.as_view()),
    path(f"{API_URL_PREFIX}upload-range/", SalaryExpectationsCSVUploadView.as_view()),
    path(f"{API_URL_PREFIX}upload-certificate/", CertificationCSVUploadView.as_view()),
    
    # dash board
    path(f"{API_URL_PREFIX}dash-board/", DashBoardListView.as_view())
] + router.urls