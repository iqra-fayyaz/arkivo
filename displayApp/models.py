from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

def validate_file_ext(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_ext = ['.pdf', '.docx', '.doc']
    if not ext in valid_ext:
        raise ValidationError('Unsupported file extension.')

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Supervisor', 'Supervisor'),
        ('Admin', 'Admin')
    ]
    role = models.CharField(max_length=200, choices=ROLE_CHOICES, default='Student')

    Department_CHOICES = [
        ('CS', 'Computer Science'),
        ('IT', 'Information Technology'),
        ('SE', 'Software Engineering'),
        ('IS', 'Information Security'),
        ('AI', 'Artificial Intelligence'),
    ]

    department = models.CharField(
        max_length=2,                          # must be at least as long as your longest key
        choices=Department_CHOICES,
        blank=False,                           # makes it required
        null=False,
        default='IT'
    )

    roll_number = models.CharField(max_length=50, unique=True)
    semester = models.IntegerField(blank=True, null=True, default=0)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['roll_number']

    def __str__(self):
        return self.roll_number
    

class Project(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('GRADED', 'Graded'),
    ]

    PROJECT_CATEGORIES = [
        ('Database', 'Database'),
        ('Web Development', 'Web Development'),
        ('Mobile App', 'Mobile App'),
        ('AI/ML', 'AI/ML'),
        ('Networking', 'Networking'),
        ('Security', 'Security'),
    ]
    project_id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=200)
    project_category = models.CharField(max_length=200, choices=PROJECT_CATEGORIES, default='Database')
    description = models.TextField()
    repo_link = models.URLField()
    srs_file = models.FileField(upload_to='files/srs/', validators=[validate_file_ext])
    sdd_file = models.FileField(upload_to='files/sdd/', validators=[validate_file_ext])
    ui_ux_file = models.FileField(upload_to='files/ui_ux/', validators=[validate_file_ext])
    plagiarism_score = models.FloatField(default=0.0)
    grade_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='GRADED')
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Grade(models.Model):
    GRADES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
    ]
    grade_id = models.AutoField(auto_created=True, primary_key=True)
    grade = models.CharField(max_length=20, choices=GRADES)
    review = models.CharField(max_length=200)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.grade
        
class PlagiarismReport(models.Model):
    report_id = models.AutoField(auto_created=True,primary_key=True)
    similarity_score = models.FloatField()
    report_details = models.TextField()
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.similarity_score
    
class Comment(models.Model):
    comment_id = models.AutoField(auto_created=True, primary_key=True)
    comment = models.TextField()
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
