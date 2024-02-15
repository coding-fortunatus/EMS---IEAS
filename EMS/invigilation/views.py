from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import pandas as pd
from .models import Hall, Lecturer, Invigilators, Supervisors, Block
from django.contrib import messages
from typing import List
import random

# Create your views here.


# login functionality
def userlogin(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Login Credentials Does Not Match!')
    context = {}
    return render(request, 'invigilation/login.html', context)


# Logout functionality
def userlogout(request):
    logout(request)
    return redirect('home')


# Index/Home page Functionality
def homePage(request):
    context = {}
    return render(request, 'invigilation/home.html', context)


# Dashboard Page Functionality
@login_required(login_url='login')
def dashboard(request):
    total_halls = Hall.objects.all().count()
    total_lecturers = Lecturer.objects.all().count()
    total_blocks = Block.objects.all().count()
    pbe_lecturers = Lecturer.objects.filter(exam_type="PBE").count()
    pbe_invigs = Lecturer.objects.filter(
        exam_type="PBE", invigilation_type="INVIGILATOR").count()
    pbe_supers = Lecturer.objects.filter(
        exam_type="PBE", invigilation_type="SUPERVISOR").count()
    cbe_lecturers = Lecturer.objects.filter(exam_type="CBE").count()
    cbe_invigs = Lecturer.objects.filter(
        exam_type="CBE", invigilation_type="INVIGILATOR").count()
    cbe_supers = Lecturer.objects.filter(
        exam_type="CBE", invigilation_type="SUPERVISOR").count()
    context = {
        "total_halls": total_halls,
        "total_lecturers": total_lecturers,
        "total_blocks": total_blocks,
        "pbe_lecturers": pbe_lecturers,
        "cbe_lecturers": cbe_lecturers,
        "pbe_invigilators": pbe_invigs,
        "pbe_supervisors": pbe_supers,
        "cbe_invigilatos": cbe_invigs,
        "cbe_supervisors": cbe_supers,

    }
    return render(request, 'invigilation/dashboard.html', context)


# Halls Page Functionality
@login_required(login_url='login')
def halls(request):
    blocks = Block.objects.all()
    hallss = []
    for block in blocks:
        for hall in block.halls.all():
            mydict = {
                "id": hall.id,
                "block_name": block.name,
                "hall_name": hall.hall_name,
                "capacity": hall.hall_capacity,
                "hall_type": hall.hall_type
            }
            hallss.append(mydict)
    context = {"hall_data": hallss}
    return render(request, 'invigilation/halls.html', context=context)


# Lecturers Page Functionality
@login_required(login_url='login')
def lecturers(request):
    lecturerss = Lecturer.objects.all()
    context = {"lecturer_data": lecturerss}
    return render(request, 'invigilation/lecturers.html', context)


# Creating student examination course schedule blueprint
class Schedule:
    def __init__(self, courses, block, exam_hall, exam_day, hall_type, exam_type, exam_period):
        self.courses = courses
        self.block = block
        self.exam_hall = exam_hall
        self.exam_day = exam_day
        self.hall_type = hall_type
        self.exam_type = exam_type
        self.exam_period = exam_period


# creating lecturer schudule blueprint
class Lecturer_Schedule:
    def __init__(self, lecturers, schedule: Schedule):
        self.lecturers = lecturers
        self.schedule = schedule


# Queue data structure implementation
class LecturerQueue:

    def __init__(self, lecturers):
        self.lecturers = lecturers

    def enqueue(self, lecturer):
        """Method that add an element to the rear of a queue, and return the queue elements"""
        self.lecturers.append(lecturer)

    def dequeue(self):
        """Method that removes an elememt from the front of a queue, and return the queue elements."""
        self.lecturers.pop(0)


# Extractin the lecturer data from the database
lecturer_data = Lecturer.objects.all().values()

# Extracting lecturers based on constraints
pbe_invigilators = [
    item for item in lecturer_data if item['exam_type'] == "PBE" and item['invigilation_type'] == "INVIGILATOR"]
pbe_supervisors = [
    item for item in lecturer_data if item['exam_type'] == "PBE" and item['invigilation_type'] == "SUPERVISOR"]
cbe_invigilators = [
    item for item in lecturer_data if item['exam_type'] == "CBE" and item['invigilation_type'] == "INVIGILATOR"]
cbe_supervisors = [
    item for item in lecturer_data if item['exam_type'] == "CBE" and item['invigilation_type'] == "SUPERVISOR"]

# Shuffling the invigilators data for randomization
random.shuffle(pbe_invigilators)
random.shuffle(pbe_supervisors)
random.shuffle(cbe_invigilators)
random.shuffle(cbe_supervisors)

# Implementating queue data structure on the invigilator datas
pbe_invigilators_queue = LecturerQueue(pbe_invigilators)
pbe_supervisors_queue = LecturerQueue(pbe_supervisors)
cbe_invigilators_queue = LecturerQueue(cbe_invigilators)
cbe_supervisors_queue = LecturerQueue(cbe_supervisors)

# Defining a list for the invigilators and supervisors
lecturer_schedule_list: List[Lecturer_Schedule] = []
supervisor_schedule_list: List[Lecturer_Schedule] = []


# Design the invigilator allocation algorithm based on number of courses in a hall
def schedule_invigilator(day_list, lq: LecturerQueue):
    """Function that takes course daily schedule and lecturer based on examination type, and schedule invigilators to exams and exam halls"""
    for sc in day_list:
        courses_per_hall = sc.courses.split(',')
        if len(courses_per_hall) == 2:
            num_of_invigilators = 2
        elif len(courses_per_hall) == 3:
            num_of_invigilators = 3
        elif len(courses_per_hall) == 4:
            num_of_invigilators = 4
        elif len(courses_per_hall) == 5:
            num_of_invigilators = 5
        else:
            num_of_invigilators = 6

        ls = Lecturer_Schedule(lecturers=[], schedule=sc)

        for i in range(num_of_invigilators):
            ls.lecturers.append(lq.lecturers[0])
            lq.dequeue()
            lq.enqueue(lq.lecturers[0])
        lecturer_schedule_list.append(ls)


# Design the supervisor allocation algorithm based on number of courses in a hall
def schedule_supervisor(block_list, lq: LecturerQueue):
    for sc in block_list:
        ls = Lecturer_Schedule(lecturers=[], schedule=sc)
        for i in range(1):
            ls.lecturers.append(lq.lecturers[0])
            lq.dequeue()
            lq.enqueue(lq.lecturers[0])
        supervisor_schedule_list.append(ls)


def join_name(lec_list):
    names = [item['lecturer_name'] for item in lec_list]
    return ", ".join(names)


def join_code(lec_list):
    codes = [code['lecturer_code'] for code in lec_list]
    return ", ".join(codes)


# Schedule Page Functionality
@login_required(login_url='login')
def schedule(request):
    if request.method == "POST":
        data = request.FILES['courses']
        course_schedules = pd.read_csv(data)
        course_schedule = course_schedules.to_dict()

        scheduled_course = []
        for key in course_schedule['courses']:
            course = Schedule(
                courses=course_schedule['courses'][key],
                block=course_schedule['block'][key],
                exam_hall=course_schedule['exam_hall'][key],
                exam_day=course_schedule['exam_date'][key],
                hall_type=course_schedule['hall_type'][key],
                exam_type=course_schedule['exam_type'][key],
                exam_period=course_schedule['exam_period'][key]
            )
            scheduled_course.append(course)

            # Extract exam dates uniquely from course schedule
            date_list = course_schedules['exam_date'].unique()
            date_list = date_list.tolist()

            # Extract Exam block uniquely from course schedule
            block_list = course_schedules['block'].unique()
            block_list = block_list.tolist()

        # ========================== Invigilator Section ==========================================

        for dates in date_list:
            pbe_day_schedule = [
                day_sch for day_sch in scheduled_course if day_sch.exam_day == dates and day_sch.exam_type == "PBE"]
            cbe_day_schedule = [
                day_sch for day_sch in scheduled_course if day_sch.exam_day == dates and day_sch.exam_type == "CBE"]

            # Schedule invigilators
            schedule_invigilator(
                day_list=pbe_day_schedule,
                lq=pbe_invigilators_queue)
            schedule_invigilator(
                day_list=cbe_day_schedule,
                lq=cbe_invigilators_queue)

        invigilator_schedule = []

        for schedule in lecturer_schedule_list:
            daily_schedule = {
                # "Lecturer Names": join_name(schedule.lecturers),
                "Lecturer Codes": join_code(schedule.lecturers),
                "Exam Hall": schedule.schedule.exam_hall,
                "Courses": schedule.schedule.courses,
                "Exam Type": schedule.schedule.exam_type,
                "Exam Day": schedule.schedule.exam_day,
                "Exam Period": schedule.schedule.exam_period
            }
            invigilator_schedule.append(daily_schedule)

            # Save the exam invigilator as a DataFrame
            # schedules_dataframe = pd.DataFrame(
            #     invigilator_schedule,
            #     columns=[
            #         "Lecturer Codes", "Exam Hall", "Courses", "Exam Type", "Exam Day", "Exam Period"])

        # Delete the old allocation if the allocation is regenerated
        Invigilators.objects.all().delete()

        # Insert the invigilator allocation into the database
        for item in invigilator_schedule:
            schd = Invigilators.objects.get_or_create(
                lecture_code=item['Lecturer Codes'],
                defaults={
                    "exam_hall": item['Exam Hall'],
                    "courses": item['Courses'],
                    "exam_type": item['Exam Type'],
                    "exam_date": item['Exam Day'],
                    "exam_period": item['Exam Period']
                })

        # Create a CVS file for the allocation
        # schedules_dataframe.sort_values(
        #     by="Exam Day", ascending=True).to_csv("../Invigilator Schedule.csv", index=False)

        # ================================ Supervisor section ==============================================
        for block in block_list:
            pbe_spv_day_schedule = [
                day_sch for day_sch in scheduled_course if day_sch.block == block and day_sch.exam_type == "PBE"]
            cbe_spv_day_schedule = [
                day_sch for day_sch in scheduled_course if day_sch.block == block and day_sch.exam_type == "CBE"]

            # Schedule Supervisors
            schedule_supervisor(block_list=pbe_spv_day_schedule,
                                lq=pbe_supervisors_queue)
            schedule_supervisor(block_list=cbe_spv_day_schedule,
                                lq=cbe_supervisors_queue)

        supervisor_schedule = []

        for schedule in supervisor_schedule_list:
            super_daily_schedule = {
                "Lecturer Codes": join_code(schedule.lecturers),
                "Block": schedule.schedule.block,
                "Exam Day": schedule.schedule.exam_day,
                "Exam Type": schedule.schedule.exam_type,
                "Exam Period": schedule.schedule.exam_period
            }
            supervisor_schedule.append(super_daily_schedule)

            # # Save the exam supervisors as a DataFrame
            # super_schedules_dataframe = pd.DataFrame(
            #     supervisor_schedule, columns=[
            #         "Lecturer Codes", "Block", "Exam Day", "Exam Type", "Exam Period"])

        # Delete the old supervisor allocation if the allocation is regenerated
        Supervisors.objects.all().delete()

        # Insert the supervisor allocations into the database
        for key in supervisor_schedule:
            schd = Supervisors.objects.get_or_create(
                lecture_code=key['Lecturer Codes'],
                defaults={
                    "exam_block": key['Block'],
                    "exam_date": key['Exam Day'],
                    "exam_type": key['Exam Type'],
                    "exam_period": key['Exam Period']
                })

        # Export the allocation to a CSV file
        # super_schedules_dataframe.sort_values(by="Exam Day", ascending=True).to_csv(
        #     "../Supervisor Schedule.csv", index=False)

        message = messages.success(request, 'Data successfully uploaded')
        return redirect("schedule")
    else:
        message = messages.error(request, 'Oops, an error occur!')
    # Fetch all the invigilators
    invigilatorss = Invigilators.objects.all()
    # Fetch all the supervisors
    supervisorss = Supervisors.objects.all()
    tablename = "invigilators"
    context = {
        "messages": message,
        "invigilators": invigilatorss,
        "supervisors": supervisorss,
        "table": tablename,
    }
    return render(request, 'invigilation/schedule.html', context)


# Uploading/adding of halls Functionality
def upload_hall(request):
    # To check if the request method is POST
    if request.method == "POST":
        data = request.FILES['halls']
        halls = pd.read_csv(data)
        halls = halls.to_dict()
        for key in halls['LECTURE ROOM']:
            hall = Hall.objects.get_or_create(
                hall_name=halls['LECTURE ROOM'][key],
                defaults={
                    "block_name": halls['LECTURE BLOCK'][key],
                    "hall_capacity": halls['CAPACITY'][key],
                    "hall_type": halls['TYPE'][key]})
        message = messages.success(request, 'Data successfully uploaded')
        return redirect("halls")
    else:
        message = messages.error(request, 'Oops, an error occur!')
    context = {"messages": message}
    return render(request, 'invigilation/halls.html', context)


# Uploading/adding of lecturer Functionality
def upload_lecturers(request):
    # To check if the request method is POST
    if request.method == "POST":
        data = request.FILES['lecturers']
        lecturers = pd.read_csv(data)
        lecturers = lecturers.to_dict()
        for key in lecturers['Lecturer Code']:
            lecturer = Lecturer.objects.get_or_create(
                lecturer_code=lecturers['Lecturer Code'][key],
                defaults={
                    "lecturer_name": lecturers['Lecturer Name'][key],
                    "lecturer_level": lecturers['Lecturer Status'][key],
                    "invigilation_type": lecturers['Invigilation Type'][key],
                    "exam_type": lecturers['Exam Type'][key]
                })
        message = messages.success(request, 'Data successfully uploaded')
        return redirect("lecturers")
    else:
        message = messages.error(request, 'Oops, an error occur!')
    context = {"messages": message}
    return render(request, 'invigilation/lecturers.html', context)
