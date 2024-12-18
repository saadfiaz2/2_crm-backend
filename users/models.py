from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from math import ceil
from datetime import date


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         profile = Profile.objects.create(user=instance)
#         profile.calculate_leave_quota()
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Division Lead', 'Division Lead'),
        ('HR', 'HR'),
        ('BD', 'BD'),
        ('Employee', 'Employee'),
        ('Project Manager', 'Project Manager'),
        ('IT', 'IT'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Not Prefer', 'Not Prefer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Employee')
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    cnic = models.CharField(max_length=13, unique=True, blank=True, null=True)  # CNIC with 13 digits
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_joining = models.DateField(blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField()
    emergency_phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    marital_status = models.CharField(max_length=50, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    employment_of_spouse = models.CharField(max_length=100, blank=True, null=True)
    number_of_children = models.IntegerField(blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_holder_name = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=30, blank=True, null=True)
    iban_number = models.CharField(max_length=34, blank=True, null=True)
    lead = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='subordinates')
    emergency_contact_primary_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_primary_relationship = models.CharField(max_length=50, blank=True, null=True)
    emergency_contact_primary_phone = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact_secondary_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_secondary_relationship = models.CharField(max_length=50, blank=True, null=True)
    emergency_contact_secondary_phone = models.CharField(max_length=15, blank=True, null=True)
    skills = models.ManyToManyField('Skill', related_name='profiles', blank=True)
    casual_leave_quota = models.FloatField(default=0)
    sick_leave_quota = models.FloatField(default=0)
    annual_leave_quota = models.FloatField(default=0)

    def calculate_leave_quota(self):
        if not self.date_of_joining:
            return

        current_year = date.today().year
        # Leave rate per month
        leave_rate = 1.8
        # Joining month
        joining_month = self.date_of_joining.month
        # Calculate remaining months in the year
        remaining_months = 12 - joining_month + 1
        # Total leave based on joining date
        total_leaves = leave_rate * remaining_months

        # Before July (first half of the year)
        if joining_month <= 6:
            # Divide into 3 categories: casual, sick, and annual
            casual = ceil(total_leaves / 3)
            sick = ceil((total_leaves - casual) / 2)
            annual = total_leaves - casual - sick
        # After July (mid-year and onwards)
        else:
            # Divide into 2 categories: casual and sick
            casual = ceil(total_leaves / 2)
            sick = total_leaves - casual
            annual = 0

        # Set quotas
        self.casual_leave_quota = casual
        self.sick_leave_quota = sick
        self.annual_leave_quota = annual
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Accessory(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='accessories')
    accessory_name = models.CharField(max_length=100)
    assigned_date = models.DateField()

    def __str__(self):
        return self.accessory_name


class Dependent(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='dependents')
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.relationship})"


class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='educations')
    institute_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.degree} - {self.institute_name}"


class WorkExperience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='work_experiences')
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)  # null and blank to allow open-ended jobs
    location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"


class Leave(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('Casual', 'Casual'),
        ('Sick', 'Sick'),
        ('Annual', 'Annual'),
        ('Umrah', 'Umrah'),
        ('Compensatory', 'Compensatory'),
        ('Parental', 'Parental'),
        ('Maternity', 'Maternity'),
        ('Bereavement', 'Bereavement'),
    ]

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.CharField(max_length=50, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True, null=True)

    # Approval process fields
    is_approved_by_lead = models.BooleanField(default=False)
    is_approved_by_hr = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def approve_by_lead(self):
        self.is_approved_by_lead = True
        self.save()

    def approve_by_hr(self):
        if self.is_approved_by_lead:
            self.is_approved_by_hr = True
            self.is_approved = True
        self.save()


def __str__(self):
    return f"{self.user.user.username} - {self.leave_type} ({self.start_date} to {self.end_date})"
