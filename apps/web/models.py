from django.db import models
import uuid
from apps.common.models.base import *
from django.core.validators import MinValueValidator, MaxValueValidator



# base model for all the model
class Base(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)  
    status = models.BooleanField(**COMMON_NULLABLE_FIELD_CONFIG)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


# country model
class Country(Base):

    country_name = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)

    def __str__(self) -> str:
        return self.country_name

# state model
class State(Base):

    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state_name = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)

    def __str__(self) -> str:
        return f"{self.state_name}, {self.country.country_name}"

# city model
class City(Base):

    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)

    def __str__(self) -> str:
        return f"{self.city_name}, {self.state.state_name}, {self.country.country_name}"

# user model    
class PersonalDetails(Base):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    last_name = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    phone_number = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    email_id = models.EmailField()
    address = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    pincode = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

# degree model
class Degree(Base):
    
    degree_name = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)

    def __str__(self) -> str:
        return self.degree_name

# certificate model
class Certifications(Base):

    certificate_name = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    year_of_certification = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.certificate_name

# educations and certificate model
class EducationAndCertifications(Base):

    degree = models.ManyToManyField(Degree)
    certificate = models.ManyToManyField(Certifications)
    year_of_passing = models.PositiveIntegerField()
    school = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)

    def __str__(self) -> str:
        degrees = ", ".join([str(d) for d in self.degree.all()])
        return f"{degrees} from {self.school}"
    
# skill model
class Skills(Base):

    skill_name = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)

    def __str__(self) -> str:
        return self.skill_name

# workdetail model
class WorkDetails(Base):

    skills = models.ManyToManyField(Skills)
    total_experience = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(15)]) 

    def __str__(self) -> str:
        skills = ", ".join([str(skill) for skill in self.skills.all()])
        return f"Work Details: {self.total_experience} years, Skills: {skills}."

# employement history model
class EmploymentHistory(Base):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    employer = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    from_date = models.DateField()
    to_date = models.DateField()

    def __str__(self) -> str:
        return f"{self.job_title} at {self.employer}"

# award model
class Awards(Base):

    award_name = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    awarding_organization = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)

    def __str__(self) -> str:
        return self.award_name

# industry model
class Industries(Base):

    field_name = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)

    def __str__(self) -> str:
        return self.field_name
    
# salary exceptations model
class SalaryExpectation(Base):

    salary_range = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)

    def __str__(self) -> str:
        return self.salary_range

# preferences model
class Preferences(Base):

    country = models.ForeignKey(Country, on_delete=models.CASCADE, default=1)
    industry = models.ForeignKey(Industries, on_delete=models.CASCADE)
    salary_exceptions = models.ForeignKey(SalaryExpectation, on_delete=models.CASCADE, default=1)
    position = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    available_from = models.DateField()
    passport = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Preferences: {self.position} in {self.country} for {self.industry}"



# job posting 
class JobPosting(Base):
    company_name = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    location = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    skills = models.TextField()
    industry = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    vacancy = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.company_name} - {self.location}"
    
# notification model
class Notification(Base):

    message = models.TextField(**COMMON_NULLABLE_FIELD_CONFIG)