from .models import *
from rest_framework import serializers
from .serializers import *

# country serializers
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']

# state serializers
class StateSerializer(serializers.ModelSerializer):

    # nested serializers for country
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.filter(is_active=True),write_only=True)

    class Meta:
        model = State
        fields = ['country', 'state_name']

# city serializers
class CitySerializer(serializers.ModelSerializer):

    # nested serializers for country, state
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.filter(is_active=True),write_only=True)
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.filter(country__is_active=True),write_only=True)

    class Meta:
        model = City
        fields = ['country', 'state', 'city_name']

# degree serializers
class DegreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Degree
        fields = ['degree_name']

# certificate serializers
class CertificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Certifications
        fields = ['certificate_name','year_of_certification']

# skill serializers
class SkillsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skills
        fields = ['skill_name']

# industry serializers
class IndustriesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Industries
        fields = ['field_name']

# salary exceptations serializers
class SalaryExpectationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SalaryExpectation
        fields = ['salary_range']


# job posting serializer
class JobPostingSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobPosting
        fields = ['company_name', 'location', 'skills', 'industry', 'vacancy']