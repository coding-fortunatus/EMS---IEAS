from django.db import models

# Create your models here.

# To create Lecturer Model


class Lecturer(models.Model):

    LEVEL = (
        ('Assisstant', 'Assisstant Lecturers'),
        ('Lecturer 1', 'Lecturer 1'),
        ('Lecturer 2', 'Lecturer 2'),
        ('Lecturer 3', 'Lecturer 3'),
        ('Senior', 'Senior Lecturer'),
        ('Principal', 'Principal Lecturer'),
        ('Chief', 'Chief Lecturer'),
        ('HOD', 'Head of Department')
    )

    EXAM_TYPE = (
        ('CBE', 'Computer Based Exam'),
        ('PBE', 'Written Exam')
    )
    INVIGILATION_TYPE = (
        ('SUPERVISOR', 'Supervisor'),
        ('INVIGILATOR', 'Invigilator')
    )

    lecturer_name = models.CharField(max_length=50)
    lecturer_code = models.CharField(max_length=10)
    lecturer_level = models.CharField(max_length=50, choices=LEVEL)
    invigilation_type = models.CharField(
        max_length=20, choices=INVIGILATION_TYPE)
    exam_type = models.CharField(max_length=50, choices=EXAM_TYPE)

    class META:
        ordering = ['lecturer_code']

    def __str__(self):
        return self.lecturer_name


# To create Examnation Hall Model
class Hall(models.Model):

    HALL_TYPES = (
        ('SM', 'Small'),
        ('MD', 'Medium'),
        ('LG', 'Large')
    )
    hall_name = models.CharField(max_length=50)
    hall_capacity = models.IntegerField()
    hall_type = models.CharField(max_length=50, choices=HALL_TYPES)

    class META:
        ordering = ['hall_name']

    def __str__(self):
        return self.hall_name


# To create Block Model
class Block(models.Model):
    name = models.CharField(max_length=50)
    halls = models.ManyToManyField(Hall)

    class META:
        ordering = ['name']

    def __str__(self):
        return self.name


# To create Invigilator Schedule Model
class Invigilators(models.Model):

    PERIOD = (
        ('AM', 'Morning'),
        ('PM', 'Afternoon')
    )

    EXAM_TYPE = (
        ('CBE', 'Computer Based Exam'),
        ('PBE', 'Paper Based Exam')
    )

    lecture_code = models.CharField(max_length=5)
    exam_hall = models.CharField(max_length=50)
    courses = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=5, choices=EXAM_TYPE)
    exam_date = models.CharField(max_length=20)
    exam_period = models.CharField(max_length=5, choices=PERIOD)

    class META:
        ordering = ['exam_period']

    def __str__(self):
        return self.lecture_code


# To create supervisors Schedule Model
class Supervisors(models.Model):

    PERIOD = (
        ('AM', 'Morning'),
        ('PM', 'Afternoon')
    )

    EXAM_TYPE = (
        ('CBE', 'Computer Based Exam'),
        ('PBE', 'Paper Based Exam')
    )

    lecture_code = models.CharField(max_length=5)
    exam_block = models.CharField(max_length=50)
    exam_type = models.CharField(max_length=5, choices=EXAM_TYPE)
    exam_date = models.CharField(max_length=20)
    exam_period = models.CharField(max_length=5, choices=PERIOD)

    class META:
        ordering = ['exam_period']

    def __str__(self):
        return self.lecture_code
