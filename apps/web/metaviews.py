from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from apps.common.pagination import AppPagination
from rest_framework.permissions import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from .tasks import *

# pagination
class AppPagination(PageNumberPagination):
    page_size = 10 

# change password
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(
                {"status": "Success", "message": "Password updated."},
                status=status.HTTP_200_OK
            )
        return Response(
            {"status": "Failed", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

# token authentications
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

# Views for Country
class CountryListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        countries = Country.objects.all()
        paginator = AppPagination()
        paginated_countries = paginator.paginate_queryset(countries, request)
        serializer = CountrySerializer(paginated_countries, many=True)
        return paginator.get_paginated_response({
            "status": "success",
            "data": serializer.data
        })

    def post(self, request):
        serializer = CountrySerializer(data=request.data)
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


class CountryDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        country = get_object_or_404(Country, id=id)
        serializer = CountrySerializer(country)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, id):
        country = get_object_or_404(Country, id=id)
        serializer = CountrySerializer(country, data=request.data)
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
        country = get_object_or_404(Country, id=id)
        country.delete()
        return Response({
            "status": "success",
            "message": "Country deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


# Views for State
class StateListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        states = State.objects.all()
        paginator = AppPagination()
        paginated_states = paginator.paginate_queryset(states, request)
        serializer = StateSerializer(paginated_states, many=True)
        return paginator.get_paginated_response({
            "status": "success",
            "data": serializer.data
        })

    def post(self, request):
        serializer = StateSerializer(data=request.data)
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


class StateDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        state = get_object_or_404(State, id=id)
        serializer = StateSerializer(state)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, id):
        state = get_object_or_404(State, id=id)
        serializer = StateSerializer(state, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "State updated successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        state = get_object_or_404(State, id=id)
        state.delete()
        return Response({
            "status": "success",
            "message": "State deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


# Views for City
class CityListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CitySerializer(data=request.data)
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


class CityDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        city = get_object_or_404(City, id=id)
        serializer = CitySerializer(city)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, id):
        city = get_object_or_404(City, id=id)
        serializer = CitySerializer(city, data=request.data)
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
        city = get_object_or_404(City, id=id)
        city.delete()
        return Response({
            "status": "success",
            "message": "City deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)

# Views for Degree
class DegreeListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        degrees = Degree.objects.all()
        serializer = DegreeSerializer(degrees, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DegreeSerializer(data=request.data)
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


class DegreeDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        degree = get_object_or_404(Degree, id=id)
        serializer = DegreeSerializer(degree)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, id):
        degree = get_object_or_404(Degree, id=id)
        serializer = DegreeSerializer(degree, data=request.data)
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
        degree = get_object_or_404(Degree, id=id)
        degree.delete()
        return Response({
            "status": "success",
            "message": "Degree deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)

# Views for Certification
class CertificationsListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        certifications = Certifications.objects.all()
        serializer = CertificationSerializer(certifications, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CertificationSerializer(data=request.data)
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


class CertificationDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        certification = get_object_or_404(Certifications, id=id)
        serializer = CertificationSerializer(certification)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, id):
        certification = get_object_or_404(Certifications, id=id)
        serializer = CertificationSerializer(certification, data=request.data)
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
        certification = get_object_or_404(Certifications, id=id)
        certification.delete()
        return Response({
            "status": "success",
            "message": "Certification deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)

# Views for Skills
class SkillsListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        skills = Skills.objects.all()
        paginator = AppPagination()  # Instantiate the pagination class
        paginated_skills = paginator.paginate_queryset(skills, request)
        serializer = SkillsSerializer(paginated_skills, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = SkillsSerializer(data=request.data)
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

class SkillsDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        skill = get_object_or_404(Skills, id=id)
        serializer = SkillsSerializer(skill)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, id):
        skill = get_object_or_404(Skills, id=id)
        serializer = SkillsSerializer(skill, data=request.data)
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
        skill = get_object_or_404(Skills, id=id)
        skill.delete()
        return Response({
            "status": "success",
            "message": "Skill deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)

# Views for Industry
class IndustryListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        industries = Industries.objects.all()
        paginator = AppPagination()
        paginated_industries = paginator.paginate_queryset(industries, request)
        serializer = IndustriesSerializer(paginated_industries, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = IndustriesSerializer(data=request.data)
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

class IndustryDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        industry = get_object_or_404(Industries, id=id)
        serializer = IndustriesSerializer(industry)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, id):
        industry = get_object_or_404(Industries, id=id)
        serializer = IndustriesSerializer(industry, data=request.data)
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
        industry = get_object_or_404(Industries, id=id)
        industry.delete()
        return Response({
            "status": "success",
            "message": "Industry deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)

# Views for Salary Expectations
class SalaryExceptationListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        salary_expectations = SalaryExpectation.objects.all()
        paginator = AppPagination()
        paginated_salary_expectations = paginator.paginate_queryset(salary_expectations, request)
        serializer = SalaryExpectationSerializer(paginated_salary_expectations, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = SalaryExpectationSerializer(data=request.data)
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

class SalaryExceptationsDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        salary_expectation = get_object_or_404(SalaryExpectation, id=id)
        serializer = SalaryExpectationSerializer(salary_expectation)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, id):
        salary_expectation = get_object_or_404(SalaryExpectation, id=id)
        serializer = SalaryExpectationSerializer(salary_expectation, data=request.data)
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
        salary_expectation = get_object_or_404(SalaryExpectation, id=id)
        salary_expectation.delete()
        return Response({
            "status": "success",
            "message": "Salary Expectation deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)

class JobProstingViewSet(viewsets.ModelViewSet):

    queryset = JobPosting.objects.all()
    
    serializer_class = JobPostingSerializer
    