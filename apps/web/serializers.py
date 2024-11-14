from .models import *
from rest_framework import serializers
import re
from .metaserializers import *

# phone number validations
def validate_phone_number(value):
    if not re.match(r'^\+?[1-9]\d{1,14}$', value):
        raise serializers.ValidationError("Invalid phone number format.")
    return value

# pincode validations
def validate_pincode(value):
    if not value.isdigit() or len(value) != 6:
        raise serializers.ValidationError("Pincode must contain numbers and  be 6 digits long.")
    return value

# user serializers
class PersonalDetailsSerializer(serializers.ModelSerializer):

    # nested serializers for country, state, city
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.filter(is_active=True),write_only=True)
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.filter(country__is_active=True),write_only=True)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.filter(state__country__is_active=True),write_only=True)

    phone_number = serializers.CharField(validators=[validate_phone_number])
    pincode = serializers.CharField(validators=[validate_pincode])

    class Meta:
        model = PersonalDetails
        fields=['first_name','last_name','phone_number','email_id','address','pincode','country','state','city']

# educations and certificate serializers
class EducationAndCertificationsSerializer(serializers.ModelSerializer):

    # many to many degree, certificate
    degree = DegreeSerializer(many=True)
    certificate = CertificationSerializer(many=True)

    class Meta:
        model = EducationAndCertifications
        fields = ['degree', 'certificate', 'year_of_passing', 'school']

    def create(self, validated_data):
        degrees_data = validated_data.pop('degree')
        certificates_data = validated_data.pop('certificate')
        education_instance = EducationAndCertifications.objects.create(**validated_data)
        
        for degree_data in degrees_data:
            degree, _ = Degree.objects.get_or_create(**degree_data)
            education_instance.degree.add(degree)
        
        for certificate_data in certificates_data:
            certificate, _ = Certifications.objects.get_or_create(**certificate_data)
            education_instance.certificate.add(certificate)

        return education_instance


# workdetail serializers
class WorkDetailsSerializer(serializers.ModelSerializer):

    # many to many field skills
    skills = SkillsSerializer(many=True)

    class Meta:
        model = WorkDetails
        fields = ['skills', 'total_experience']
    
    def create(self, validated_data):
        skills_data = validated_data.pop('skills', [])
        work_details_instance = WorkDetails.objects.create(**validated_data)

        for skill_data in skills_data:
            skill, _ = Skills.objects.get_or_create(**skill_data)
            work_details_instance.skills.add(skill)

        return work_details_instance

# employment history serializers
class EmploymentHistorySerializer(serializers.ModelSerializer):

    # nested serializers for country, state, city
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.filter(is_active=True),write_only=True)
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.filter(country__is_active=True),write_only=True)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.filter(state__country__is_active=True),write_only=True)

    class Meta:
        model = EmploymentHistory
        fields = ['job_title','employer','country','state','city','from_date','to_date']

# award serializers
class AwardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Awards
        fields = ['award_name', 'awarding_organization']

# preferences serializers
class PreferencesSerializer(serializers.ModelSerializer):

    # nested serializers for country, industry, salary
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.filter(is_active=True), write_only=True)
    industry = serializers.PrimaryKeyRelatedField(queryset=Industries.objects.filter(is_active=True), write_only=True)
    salary_exceptions = serializers.PrimaryKeyRelatedField(queryset=SalaryExpectation.objects.filter(is_active=True), write_only=True)
    
    class Meta:
        model = Preferences
        fields = ['country', 'industry', 'position', 'available_from', 'salary_exceptions']

# password serializers
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
    
# serializers for notifications    
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['message'] 