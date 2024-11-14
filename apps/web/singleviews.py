from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *
from rest_framework.views import APIView
from .tasks import *
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size'
    max_page_size = 100

# create and get a user in a single request
class SaveDataCreateListViewSet(ViewSet):
    def create(self, request, *args, **kwargs):
        personal_details_data = request.data.get('personal_details')
        education_certifications_data = request.data.get('education_and_certifications')
        work_details_data = request.data.get('work_details')
        employment_history_data = request.data.get('employment_history')
        awards_data = request.data.get('awards')
        preferences_data = request.data.get('preferences')
        
        # Initialize serializers
        personal_details_serializer = PersonalDetailsSerializer(data=personal_details_data)
        education_certifications_serializer = EducationAndCertificationsSerializer(data=education_certifications_data, many=True)
        work_details_serializer = WorkDetailsSerializer(data=work_details_data, many=True)
        employment_history_serializer = EmploymentHistorySerializer(data=employment_history_data, many=True)
        awards_serializer = AwardSerializer(data=awards_data, many=True)
        preferences_serializer = PreferencesSerializer(data=preferences_data)
        
        # Check if all serializers are valid
        serializers_valid = all([
            personal_details_serializer.is_valid(),
            education_certifications_serializer.is_valid(),
            work_details_serializer.is_valid(),
            employment_history_serializer.is_valid(),
            awards_serializer.is_valid(),
            preferences_serializer.is_valid()
        ])
        
        # If valid, save the data
        if serializers_valid:
            # Save instances for each serializer
            personal_details_instance = personal_details_serializer.save()
            education_certifications_instance = education_certifications_serializer.save()
            work_details_instance = work_details_serializer.save()
            employment_history_instance = employment_history_serializer.save()
            awards_instance = awards_serializer.save()
            preferences_instance = preferences_serializer.save()
            
            # Return response with saved data
            return Response(
                {
                    'personal_details': personal_details_serializer.data,
                    'education_and_certifications': education_certifications_serializer.data,
                    'work_details': work_details_serializer.data,
                    'employment_history': employment_history_serializer.data,
                    'awards': awards_serializer.data,
                    'preferences': preferences_serializer.data,
                },
                status=status.HTTP_201_CREATED
            )
        else:
            # Return error response if serializers are invalid
            return Response(
                {
                    'error': {
                        'personal_details': personal_details_serializer.errors,
                        'education_and_certifications': education_certifications_serializer.errors,
                        'work_details': work_details_serializer.errors,
                        'employment_history': employment_history_serializer.errors,
                        'awards': awards_serializer.errors,
                        'preferences': preferences_serializer.errors,
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def list(self, request, *args, **kwargs):
        # Query all users' related data
        personal_details = PersonalDetails.objects.all()
        education_certifications = EducationAndCertifications.objects.all()
        work_details = WorkDetails.objects.all()
        employment_history = EmploymentHistory.objects.all()
        awards = Awards.objects.all()
        preferences = Preferences.objects.all()

        # Apply pagination to each queryset
        paginator = CustomPagination()

        # Paginate 
        personal_details_page = paginator.paginate_queryset(personal_details, request)
        education_certifications_page = paginator.paginate_queryset(education_certifications, request)
        work_details_page = paginator.paginate_queryset(work_details, request)
        employment_history_page = paginator.paginate_queryset(employment_history, request)
        awards_page = paginator.paginate_queryset(awards, request)
        preferences_page = paginator.paginate_queryset(preferences, request)

        # Serialize 
        personal_details_serializer = PersonalDetailsSerializer(personal_details_page, many=True)
        education_certifications_serializer = EducationAndCertificationsSerializer(education_certifications_page, many=True)
        work_details_serializer = WorkDetailsSerializer(work_details_page, many=True)
        employment_history_serializer = EmploymentHistorySerializer(employment_history_page, many=True)
        awards_serializer = AwardSerializer(awards_page, many=True)
        preferences_serializer = PreferencesSerializer(preferences_page, many=True)


        return paginator.get_paginated_response({
            'personal_details': personal_details_serializer.data,
            'education_and_certifications': education_certifications_serializer.data,
            'work_details': work_details_serializer.data,
            'employment_history': employment_history_serializer.data,
            'awards': awards_serializer.data,
            'preferences': preferences_serializer.data,
        })

# detail views
class UserAllDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        try:
            # Fetch user details for all related fields
            personal_details = PersonalDetails.objects.get(id=id)
            work_details = WorkDetails.objects.get(id=id)
            employment_history = EmploymentHistory.objects.filter(id=id)
            awards = Awards.objects.filter(id=id)
            preferences = Preferences.objects.get(id=id)
            education_and_certifications = EducationAndCertifications.objects.filter(id=id)

            # Serialize the data
            personal_details_serializer = PersonalDetailsSerializer(personal_details)
            work_details_serializer = WorkDetailsSerializer(work_details)
            employment_history_serializer = EmploymentHistorySerializer(employment_history, many=True)
            awards_serializer = AwardSerializer(awards, many=True)
            preferences_serializer = PreferencesSerializer(preferences)
            education_and_certifications_serializer = EducationAndCertificationsSerializer(education_and_certifications, many=True)

            # Return the serialized data
            return Response({
                'personal_details': personal_details_serializer.data,
                'work_details': work_details_serializer.data,
                'employment_history': employment_history_serializer.data,
                'awards': awards_serializer.data,
                'preferences': preferences_serializer.data,
                'education_and_certifications': education_and_certifications_serializer.data
            }, status=status.HTTP_200_OK)

        except PersonalDetails.DoesNotExist:
            return Response({'error': 'Personal details not found'}, status=status.HTTP_404_NOT_FOUND)
        except WorkDetails.DoesNotExist:
            return Response({'error': 'Work details not found'}, status=status.HTTP_404_NOT_FOUND)
        except Preferences.DoesNotExist:
            return Response({'error': 'Preferences not found'}, status=status.HTTP_404_NOT_FOUND)
        except EmploymentHistory.DoesNotExist:
            return Response({'error': 'Employment history not found'}, status=status.HTTP_404_NOT_FOUND)
        except EducationAndCertifications.DoesNotExist:
            return Response({'error': 'Education and Certifications not found'}, status=status.HTTP_404_NOT_FOUND)
        except Awards.DoesNotExist:
            return Response({'error': 'Awards not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        try:
            # Fetch user details for update
            personal_details = PersonalDetails.objects.get(id=id)
            work_details = WorkDetails.objects.get(id=id)
            preferences = Preferences.objects.get(id=id)

            # Handle the patch update for each section
            personal_details_serializer = PersonalDetailsSerializer(personal_details, data=request.data.get('personal_details'), partial=True)
            work_details_serializer = WorkDetailsSerializer(work_details, data=request.data.get('work_details'), partial=True)
            preferences_serializer = PreferencesSerializer(preferences, data=request.data.get('preferences'), partial=True)

            # Validate and save data
            if personal_details_serializer.is_valid():
                personal_details_serializer.save()
            if work_details_serializer.is_valid():
                work_details_serializer.save()
            if preferences_serializer.is_valid():
                preferences_serializer.save()

            # Return updated data
            return Response({
                'personal_details': personal_details_serializer.data,
                'work_details': work_details_serializer.data,
                'preferences': preferences_serializer.data
            }, status=status.HTTP_200_OK)

        except PersonalDetails.DoesNotExist:
            return Response({'error': 'Personal details not found'}, status=status.HTTP_404_NOT_FOUND)
        except WorkDetails.DoesNotExist:
            return Response({'error': 'Work details not found'}, status=status.HTTP_404_NOT_FOUND)
        except Preferences.DoesNotExist:
            return Response({'error': 'Preferences not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            # Delete all related details for the user
            personal_details = PersonalDetails.objects.get(id=id)
            work_details = WorkDetails.objects.get(id=id)
            employment_history = EmploymentHistory.objects.filter(id=id)
            awards = Awards.objects.filter(id=id)
            preferences = Preferences.objects.get(id=id)
            education_and_certifications = EducationAndCertifications.objects.filter(id=id)

            # Delete each section
            personal_details.delete()
            work_details.delete()
            employment_history.delete()
            awards.delete()
            preferences.delete()
            education_and_certifications.delete()

            return Response({'message': 'User details deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        except PersonalDetails.DoesNotExist:
            return Response({'error': 'Personal details not found'}, status=status.HTTP_404_NOT_FOUND)
        except WorkDetails.DoesNotExist:
            return Response({'error': 'Work details not found'}, status=status.HTTP_404_NOT_FOUND)
        except Preferences.DoesNotExist:
            return Response({'error': 'Preferences not found'}, status=status.HTTP_404_NOT_FOUND)
        except EmploymentHistory.DoesNotExist:
            return Response({'error': 'Employment history not found'}, status=status.HTTP_404_NOT_FOUND)
        except EducationAndCertifications.DoesNotExist:
            return Response({'error': 'Education and Certifications not found'}, status=status.HTTP_404_NOT_FOUND)
        except Awards.DoesNotExist:
            return Response({'error': 'Awards not found'}, status=status.HTTP_404_NOT_FOUND)