from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from apps.common.pagination import AppPagination
from rest_framework.permissions import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import *
from rest_framework import viewsets

# pagination
class AppPagination(PageNumberPagination):
    page_size = 10 

# views for User
class UserListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = AppPagination

    def get(self, request):
        users = PersonalDetails.objects.all()
        paginator = self.pagination_class()
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = PersonalDetailsSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        serializer = PersonalDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = get_object_or_404(PersonalDetails, id=id)
        serializer = PersonalDetailsSerializer(user)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        user = get_object_or_404(PersonalDetails, id=id)
        serializer = PersonalDetailsSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = get_object_or_404(PersonalDetails, id=id)
        user.delete()
        return Response({
            "status": "success",
            "message": "User deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)

# views for Education and Certifications
class EducationAndCertificationsListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = AppPagination

    def get(self, request):
        ed = EducationAndCertifications.objects.all()
        paginator = self.pagination_class()
        paginated_ed = paginator.paginate_queryset(ed, request)
        serializer = EducationAndCertificationsSerializer(paginated_ed, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        serializer = EducationAndCertificationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class EducationAndCertificationsDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        ed = get_object_or_404(EducationAndCertifications, id=id)
        serializer = EducationAndCertificationsSerializer(ed)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, id):
        ed = get_object_or_404(EducationAndCertifications, id=id)
        serializer = EducationAndCertificationsSerializer(ed, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        ed = get_object_or_404(EducationAndCertifications, id=id)
        ed.delete()
        return Response({
            "status": "success",
            "message": "Education and Certifications deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)

# views for work details
class WorkDetailsListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = AppPagination

    def get(self, request):

        work = WorkDetails.objects.all()
        serializer = WorkDetailsSerializer(work, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):

        serializer = WorkDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class WorkDetailsDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        work = get_object_or_404(WorkDetails, id=id)
        serializer = WorkDetailsSerializer(work)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, id):

        work = get_object_or_404(WorkDetails, id=id)
        serializer = WorkDetailsSerializer(work, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):

        work = get_object_or_404(WorkDetails, id=id)
        work.delete()
        return Response({
            "status": "success",
            "message": "WorkDetails deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)

# views for employment history
class EmploymentHistoryListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = AppPagination

    def get(self, request):

        employee = EmploymentHistory.objects.all()
        serializer = EmploymentHistorySerializer(employee, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):

        serializer = EmploymentHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class EmploymentHistoryDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        employee = get_object_or_404(EmploymentHistory, id=id)
        serializer = EmploymentHistorySerializer(employee)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, id):

        employee = get_object_or_404(EmploymentHistory, id=id)
        serializer = EmploymentHistorySerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):

        employee = get_object_or_404(EmploymentHistory, id=id)
        employee.delete()
        return Response({
            "status": "success",
            "message": "Employment History deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)

# views for awards
class AwardsListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]
    pagination_class = AppPagination

    def get(self, request):

        award = Awards.objects.all()
        serializer = AwardSerializer(award, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):

        serializer = AwardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class AwardDetailAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, id):

        award = get_object_or_404(Awards, id=id)
        serializer = AwardSerializer(award)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, id):

        award = get_object_or_404(Awards, id=id)
        serializer = AwardSerializer(award, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):

        award = get_object_or_404(Awards, id=id)
        award.delete()
        return Response({
            "status": "success",
            "message": "Award deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)

# views for preferences
class PreferencesListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]
    pagination_class = AppPagination

    def get(self, request):

        preference = Preferences.objects.all()
        serializer = PreferencesSerializer(preference, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):

        serializer = PreferencesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class PreferencesDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        preference = get_object_or_404(Preferences, id=id)
        serializer = PreferencesSerializer(preference)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, id):

        preference = get_object_or_404(Preferences, id=id)
        serializer = PreferencesSerializer(preference, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):

        preference = get_object_or_404(Preferences, id=id)
        preference.delete()
        return Response({
            "status": "success",
            "message": "Preferences deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)

# export for all the user details using id
class ExportUserDataView(APIView):
    def get(self, request, id): 
        try:
            export_user_data.delay(id)

            # Return a success response
            return Response({
                'status': 'success',
                'message': f'Please wait for the process to complete.'
            }, status=200)  

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=500)

# notification views   
class NotificationListView(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    
# dash board 
class DashBoardListView(APIView):

    def get(self, request):

        job_count = JobPosting.objects.count()
        personal_detail_count = PersonalDetails.objects.count()
        data = {
            'job_posting_count': job_count,
            'Appliations': personal_detail_count
        }

        return Response({
            'status' : 'success',
            'data' : data
        })
    
# bulk uploads for country, state, city, degree, skills, certificate, industry, salary
class CountryCSVUploadView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'File is not CSV type'}, status=status.HTTP_400_BAD_REQUEST)
        decoded_file = csv_file.read().decode('utf-8')
        celery_process_countries.delay(decoded_file)
        return Response({'message': 'File is being processed. Please wait for the result.'}, status=status.HTTP_202_ACCEPTED)


class StateCSVUploadView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'File is not CSV type'}, status=status.HTTP_400_BAD_REQUEST)
        decoded_file = csv_file.read().decode('utf-8')
        celery_process_states.delay(decoded_file)
        return Response({'message': 'File is being processed. Please wait for the result.'}, status=status.HTTP_202_ACCEPTED)
    
class CityCSVUploadView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'error' : 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'File is not CSV type'}, status=status.HTTP_400_BAD_REQUEST)
        decoded_file = csv_file.read().decode('utf-8')
        celery_process_cities.delay(decoded_file)
        return Response({'message': 'File is being processed. Please wait for the result.'}, status=status.HTTP_202_ACCEPTED)

class DegreeCSVUploadView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'error' : 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'File is not CSV type'}, status=status.HTTP_400_BAD_REQUEST)
        decoded_file = csv_file.read().decode('utf-8')
        celery_process_degrees.delay(decoded_file)
        return Response({'message': 'File is being processed. Please wait for the result.'}, status=status.HTTP_202_ACCEPTED)

class CertificationCSVUploadView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'error' : 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'File is not CSV type'}, status=status.HTTP_400_BAD_REQUEST)
        decoded_file = csv_file.read().decode('utf-8')
        celery_process_certifications.delay(decoded_file)
        return Response({'message': 'File is being processed. Please wait for the result.'}, status=status.HTTP_202_ACCEPTED)

class SkillsCSVUploadView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'error' : 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'File is not CSV type'}, status=status.HTTP_400_BAD_REQUEST)
        decoded_file = csv_file.read().decode('utf-8')
        celery_process_skills.delay(decoded_file)
        return Response({'message': 'File is being processed. Please wait for the result.'}, status=status.HTTP_202_ACCEPTED)

class IndustryCSVUploadView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'error' : 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'File is not CSV type'}, status=status.HTTP_400_BAD_REQUEST)
        decoded_file = csv_file.read().decode('utf-8')
        celery_process_industry.delay(decoded_file)
        return Response({'message': 'File is being processed. Please wait for the result.'}, status=status.HTTP_202_ACCEPTED)

class SalaryExpectationsCSVUploadView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'error' : 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'File is not CSV type'}, status=status.HTTP_400_BAD_REQUEST)
        decoded_file = csv_file.read().decode('utf-8')
        celery_process_range.delay(decoded_file)
        return Response({'message': 'File is being processed. Please wait for the result.'}, status=status.HTTP_202_ACCEPTED)
