import os
import io
import csv
import logging
import time
from celery import shared_task
from apps.common.models.base import *
from .models import *
from .serializers import *
from .metaserializers import *
from .views import *
from .metaviews import *
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter 

logger = logging.getLogger(__name__)

# country upload
@shared_task
def celery_process_countries(file_data, batch_size=10):

    # read the file
    io_string = io.StringIO(file_data)
    reader = csv.reader(io_string, delimiter=',')
    data_chunk = []
    for row in reader:
        if not row or len(row) < 1:
            continue

        country_data = Country(
            country_name=row[0]
        )
        
        data_chunk.append(country_data)

        if len(data_chunk) >= batch_size:
            save_countries(data_chunk)
            data_chunk = []
    if data_chunk:
        save_countries(data_chunk)
    return {'status': 'success', 'message': 'Countries uploaded successfully'}

def save_countries(chunk):
    try:
        Country.objects.bulk_create(chunk)
    except Exception as e:
        print(f"Error during bulk create: {e}")

# state import
@shared_task
def celery_process_states(file_data, batch_size=10):
    # read the csv
    io_string = io.StringIO(file_data)
    reader = csv.reader(io_string, delimiter=',')
    data_chunk = []

    # itearate
    for row in reader:
        if not row or len(row) < 2:
            continue

        try:
            country = Country.objects.get(id=row[0])
            state_data = State(
                country=country,
                state_name=row[1]
            )
            data_chunk.append(state_data)

            if len(data_chunk) >= batch_size:
                save_states(data_chunk)
                data_chunk = [] 

        except Country.DoesNotExist:
            continue 
    # save
    if data_chunk:
        save_states(data_chunk)

    return {'status': 'success', 'message': 'States uploaded successfully'}

def save_states(chunk):
    try:
        State.objects.bulk_create(chunk)
    except Exception as e:
        print(f"Error during bulk create: {e}")
    
# city import
@shared_task
def celery_process_cities(file_data, batch_size=10):
    io_string = io.StringIO(file_data)
    reader = csv.reader(io_string, delimiter=',')
    data_chunk = []

    for row in reader:
        if not row or len(row) < 3: 
            continue

        try:
            country = Country.objects.get(id=row[0])  
            state = State.objects.get(id=row[1], country=country) 
            city_data = City(
                country=country,
                state=state,
                city_name=row[2]
            )
            data_chunk.append(city_data)

            if len(data_chunk) >= batch_size:
                save_cities(data_chunk)
                data_chunk = []  

        except (Country.DoesNotExist, State.DoesNotExist):
            continue 
    if data_chunk:
        save_cities(data_chunk)

    return {'status': 'success', 'message': 'Cities uploaded successfully'}

def save_cities(chunk):
    try:
        City.objects.bulk_create(chunk)
    except Exception as e:
        print(f"Error during bulk create: {e}")

# degree import
@shared_task
def celery_process_degrees(file_data, batch_size=10):
    io_string = io.StringIO(file_data)
    reader = csv.reader(io_string, delimiter=',')
    data_chunk = []

    for row in reader:
        if not row or len(row) < 1: 
            continue

        degree_data = Degree(degree_name=row[0]) 
        data_chunk.append(degree_data)

        if len(data_chunk) >= batch_size:
            save_degrees(data_chunk)
            data_chunk = [] 
    if data_chunk:
        save_degrees(data_chunk)

    return {'status': 'success', 'message': 'Degrees uploaded successfully'}

def save_degrees(chunk):
    try:
        Degree.objects.bulk_create(chunk)
    except Exception as e:
        print(f"Error during bulk create: {e}")

# certificate import
@shared_task
def celery_process_certifications(file_data, batch_size=10):
    io_string = io.StringIO(file_data)
    reader = csv.reader(io_string, delimiter=',')
    data_chunk = []
    for row in reader:
        if not row or len(row) < 2: 
            continue
        try:
            certification_data = Certifications(
                certificate_name=row[0],
                year_of_certification=int(row[1]) 
            )
            data_chunk.append(certification_data)
            if len(data_chunk) >= batch_size:
                save_certifications(data_chunk)
                data_chunk = []  
        except ValueError as e:
            print(f"Error processing row {row}: {e}")
    if data_chunk:
        save_certifications(data_chunk)
    return {'status': 'success', 'message': 'Certifications uploaded successfully'}

def save_certifications(chunk):
    try:
        Certifications.objects.bulk_create(chunk)
    except Exception as e:
        print(f"Error during bulk create: {e}")

# skills import
@shared_task
def celery_process_skills(file_data, batch_size=10):
    io_string = io.StringIO(file_data)
    reader = csv.reader(io_string, delimiter=',')
    data_chunk = []
    for row in reader:
        if not row or len(row) < 1: 
            continue

        skill_data = Skills(skill_name=row[0]) 
        data_chunk.append(skill_data)

        if len(data_chunk) >= batch_size:
            save_skills(data_chunk)
            data_chunk = [] 
    if data_chunk:
        save_skills(data_chunk)

    return {'status': 'success', 'message': 'Skills uploaded successfully'}

def save_skills(chunk):
    try:
        Skills.objects.bulk_create(chunk)
    except Exception as e:
        print(f"Error during bulk create: {e}")

# industry import
@shared_task
def celery_process_industry(file_data, batch_size=10):
    io_string = io.StringIO(file_data)
    reader = csv.reader(io_string, delimiter=',')
    data_chunk = []
    for row in reader:
        if not row or len(row) < 1: 
            continue

        industry_data = Industries(field_name=row[0])
        data_chunk.append(industry_data)

        if len(data_chunk) >= batch_size:
            save_industry(data_chunk)
            data_chunk = [] 
    if data_chunk:
        save_industry(data_chunk)

    return {'status': 'success', 'message': 'Industry uploaded successfully'}

def save_industry(chunk):
    try:
        Industries.objects.bulk_create(chunk)
    except Exception as e:
        print(f"Error during bulk create: {e}")

# salary import
@shared_task
def celery_process_range(file_data, batch_size=10):
    io_string = io.StringIO(file_data)
    reader = csv.reader(io_string, delimiter=',')
    data_chunk = []
    for row in reader:
        if not row or len(row) < 1: 
            continue

        range_data = SalaryExpectation(salary_range=row[0])
        data_chunk.append(range_data)

        if len(data_chunk) >= batch_size:
            save_salary_range(data_chunk)
            data_chunk = [] 
    
    if data_chunk:
        save_salary_range(data_chunk)

    return {'status': 'success', 'message': 'Salary uploaded successfully'}

def save_salary_range(chunk):
    try:
        SalaryExpectation.objects.bulk_create(chunk)
    except Exception as e:
        print(f"Error during bulk create: {e}")
    

# export for all the details in the pdf format
@shared_task()
def export_user_data(id):
    time.sleep(10)
    try:
        # Fetch user's data from all relevant models
        personal_details = PersonalDetails.objects.get(id=id)
        education_certifications = EducationAndCertifications.objects.filter(id=id)
        work_details = WorkDetails.objects.filter(id=id)
        employment_history = EmploymentHistory.objects.filter(id=id)
        awards = Awards.objects.filter(id=id)
        preferences = Preferences.objects.filter(id=id)

        # Combine all data into a single list
        user_data = [
            personal_details,
            *education_certifications,
            *work_details,
            *employment_history,
            *awards,
            *preferences
        ]

        # Generate PDF content
        pdf_content = generate_pdf(user_data, personal_details)

        filename = f"{personal_details.first_name}_{timezone.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
        file_path = save_pdf_to_file(pdf_content, filename)

        return {
            'filename': filename,
            'status': 'success',
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
        }

# this is pdf format we can design and extend whatever we want
def generate_pdf(data, personal_details):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textobj = c.beginText()
    textobj.setTextOrigin(1 * inch, 1 * inch)
    textobj.setFont("Helvetica", 12)

    # Add personal details
    lines = [
        f"Name: {personal_details.first_name} {personal_details.last_name}",
        f"Email: {personal_details.email_id}",
        f"Phone: {personal_details.phone_number}",
        f"Address: {personal_details.address}, {personal_details.city.city_name}, {personal_details.state.state_name}, {personal_details.country.country_name}",
        f"Pincode: {personal_details.pincode}",
    ]
    
    # Education and Certifications
    lines.append("\nEducation and Certifications:")
    for edu in data[1:]:
        if isinstance(edu, EducationAndCertifications):
            # List degrees
            degrees = ", ".join([degree.degree_name for degree in edu.degree.all()])
            certificates = ", ".join([cert.certificate_name for cert in edu.certificate.all()])
            lines.append(f"  Degrees: {degrees}")
            lines.append(f"  Certifications: {certificates}")
            lines.append(f"  School: {edu.school}, Year of Passing: {edu.year_of_passing}")
    
    # Work Details
    lines.append("\nWork Experience:")
    for work in data[2:]:
        if isinstance(work, WorkDetails):
            skills = ", ".join([skill.skill_name for skill in work.skills.all()])
            lines.append(f"  Experience: {work.total_experience} years, Skills: {skills}")
    
    # Employment History
    lines.append("\nEmployment History:")
    for emp in data[3:]:
        if isinstance(emp, EmploymentHistory):
            lines.append(f"  Job Title: {emp.job_title}, Employer: {emp.employer}")
            lines.append(f"  Location: {emp.city.city_name}, {emp.state.state_name}, {emp.country.country_name}")
            lines.append(f"  Duration: {emp.from_date} to {emp.to_date}")

    # Awards
    lines.append("\nAwards:")
    for award in data[4:]:
        if isinstance(award, Awards):
            lines.append(f"  Award: {award.award_name}, Organization: {award.awarding_organization}")
    
    # Preferences
    lines.append("\nPreferences:")
    for pref in data[5:]:
        if isinstance(pref, Preferences):
            lines.append(f"  Position: {pref.position}, Available From: {pref.available_from}")
            lines.append(f"  Preferred Country: {pref.country.country_name}, Industry: {pref.industry.field_name}")
            lines.append(f"  Salary Expectation: {pref.salary_exceptions.salary_range}, Passport: {pref.passport}")
    
    # Adding lines to the PDF
    for line in lines:
        textobj.textLine(line)

    c.drawText(textobj)
    c.showPage()
    c.save()
    buf.seek(0)

    # Return raw bytes for saving
    return buf.getvalue()


# saving pdf in my local
def save_pdf_to_file(pdf_content, filename):
    directory = '/Users/jeevas/Downloads'

    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, filename)

    with open(file_path, 'wb') as f:
        f.write(pdf_content)

    return file_path