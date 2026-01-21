import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class BaseModel(models.Model):
    """Base model with UUID primary key and timestamps"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    """Custom user model with UUID and roles"""
    ROLE_CHOICES = [
        ('SUPER_ADMIN', 'Super Admin'),
        ('ADMIN', 'Admin'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
        ('PARENT', 'Parent'),
        ('ACCOUNTANT', 'Accountant'),
        ('TRANSPORT_MANAGER', 'Transport Manager'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STUDENT')
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set'
    )

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"


class AcademicYear(BaseModel):
    """Academic year configuration"""
    name = models.CharField(max_length=20)  # e.g., 2024-2025
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'academic_years'
        unique_together = ('name',)

    def __str__(self):
        return self.name


class School(BaseModel):
    """School Information"""
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)
    established_year = models.IntegerField(blank=True, null=True)
    principal_name = models.CharField(max_length=255, blank=True, null=True)
    affiliation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'schools'

    def __str__(self):
        return self.name


class Class(BaseModel):
    """Class/Grade Configuration"""
    name = models.CharField(max_length=50)  # 1A, 10B, etc.
    class_number = models.IntegerField()  # 1, 2, 3, ..., 12
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    class_teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='class_teacher')
    capacity = models.IntegerField(default=40)
    section = models.CharField(max_length=10, default='A')

    class Meta:
        db_table = 'classes'
        unique_together = ('name', 'academic_year')
        ordering = ['class_number', 'section']

    def __str__(self):
        return f"{self.name} ({self.academic_year})"


class Subject(BaseModel):
    """Subject Configuration"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    max_marks = models.IntegerField(default=100)
    pass_marks = models.IntegerField(default=35)

    class Meta:
        db_table = 'subjects'

    def __str__(self):
        return self.name


class Student(BaseModel):
    """Student Profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    roll_number = models.CharField(max_length=20, unique=True)
    admission_number = models.CharField(max_length=20, unique=True)
    admission_date = models.DateField()
    current_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    aadhar_number = models.CharField(max_length=12, blank=True, null=True)  # Masked for privacy
    father_name = models.CharField(max_length=255, blank=True, null=True)
    mother_name = models.CharField(max_length=255, blank=True, null=True)
    guardian_name = models.CharField(max_length=255, blank=True, null=True)
    guardian_phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    previous_school = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'students'
        ordering = ['-admission_date']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"


class Parent(BaseModel):
    """Parent Profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent')
    occupation = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    alternate_phone = models.CharField(max_length=15, blank=True, null=True)
    relationship_to_student = models.CharField(max_length=50, blank=True, null=True)  # Father, Mother, Guardian

    class Meta:
        db_table = 'parents'

    def __str__(self):
        return f"{self.user.get_full_name()}"


class StudentParent(BaseModel):
    """Relationship between Students and Parents"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='parents')
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='students')
    relationship = models.CharField(max_length=50)  # Father, Mother, Guardian, etc.
    is_primary_contact = models.BooleanField(default=False)

    class Meta:
        db_table = 'student_parents'
        unique_together = ('student', 'parent')

    def __str__(self):
        return f"{self.student} - {self.parent} ({self.relationship})"


class Staff(BaseModel):
    """Staff/Teacher Profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff')
    employee_id = models.CharField(max_length=20, unique=True)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True, null=True)
    qualification = models.CharField(max_length=255)
    experience_years = models.IntegerField(default=0)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    date_of_joining = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    contract_type = models.CharField(max_length=50, choices=[('PERMANENT', 'Permanent'), ('TEMPORARY', 'Temporary')], default='PERMANENT')
    address = models.TextField(blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    ifsc_code = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        db_table = 'staff'
        ordering = ['employee_id']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.designation})"


class ClassSubject(BaseModel):
    """Subject assignment to a class"""
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects_taught')
    is_mandatory = models.BooleanField(default=True)

    class Meta:
        db_table = 'class_subjects'
        unique_together = ('class_obj', 'subject')

    def __str__(self):
        return f"{self.class_obj} - {self.subject}"


# ============ ATTENDANCE MODELS ============

class AttendanceRecord(BaseModel):
    """Daily Attendance"""
    ATTENDANCE_CHOICES = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('LEAVE', 'Leave'),
        ('LATE', 'Late'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(db_index=True)
    status = models.CharField(max_length=20, choices=ATTENDANCE_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='attendance_marked')
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'attendance_records'
        unique_together = ('student', 'date', 'subject')
        ordering = ['-date']

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"


class BiometricAttendance(BaseModel):
    """Biometric Attendance Records"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='biometric_records')
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField(blank=True, null=True)
    biometric_id = models.CharField(max_length=50)
    device_id = models.CharField(max_length=50)

    class Meta:
        db_table = 'biometric_attendance'
        ordering = ['-date', '-time_in']

    def __str__(self):
        return f"{self.student} - {self.date}"


# ============ FEES MODELS ============

class FeeStructure(BaseModel):
    """Fee Structure Configuration"""
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    fee_type = models.CharField(max_length=50)  # Tuition, Transport, etc.
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    frequency = models.CharField(max_length=20, choices=[('MONTHLY', 'Monthly'), ('QUARTERLY', 'Quarterly'), ('ANNUAL', 'Annual')])
    due_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'fee_structures'
        unique_together = ('academic_year', 'class_obj', 'fee_type')

    def __str__(self):
        return f"{self.class_obj} - {self.fee_type}"


class FeeDiscount(BaseModel):
    """Fee Discounts"""
    name = models.CharField(max_length=100)
    discount_type = models.CharField(max_length=20, choices=[('PERCENTAGE', 'Percentage'), ('FIXED', 'Fixed Amount')])
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    applicable_for = models.ManyToManyField(Student)
    valid_from = models.DateField()
    valid_to = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'fee_discounts'

    def __str__(self):
        return self.name


class FeePayment(BaseModel):
    """Fee Payment Tracking"""
    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('PARTIAL', 'Partial'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
    ]

    PAYMENT_METHOD = [
        ('CASH', 'Cash'),
        ('CHEQUE', 'Cheque'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('ONLINE', 'Online Payment'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fee_payments')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_date = models.DateField()
    payment_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='fees_received')

    class Meta:
        db_table = 'fee_payments'
        ordering = ['-due_date']

    def __str__(self):
        return f"{self.student} - {self.amount_due} - {self.status}"


class Invoice(BaseModel):
    """Fee Invoices"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=50, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    issued_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    period_from = models.DateField()
    period_to = models.DateField()
    is_paid = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'invoices'
        ordering = ['-issued_date']

    def __str__(self):
        return self.invoice_number


# ============ EXAMINATION MODELS ============

class Exam(BaseModel):
    """Exam Configuration"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    exam_type = models.CharField(max_length=50)  # Unit Test, Half Yearly, etc.
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    result_published_date = models.DateField(blank=True, null=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        db_table = 'exams'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} ({self.academic_year})"


class ExamSchedule(BaseModel):
    """Exam Schedule"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='schedules')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_marks = models.IntegerField()
    room_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'exam_schedules'
        unique_together = ('exam', 'class_obj', 'subject')

    def __str__(self):
        return f"{self.exam} - {self.subject} - {self.exam_date}"


class Mark(BaseModel):
    """Exam Marks"""
    exam_schedule = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE, related_name='marks')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    is_absent = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='marks_entered')
    entered_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'marks'
        unique_together = ('exam_schedule', 'student')

    def __str__(self):
        return f"{self.student} - {self.exam_schedule.subject} - {self.marks_obtained}"


class Grade(BaseModel):
    """Grade Configuration"""
    name = models.CharField(max_length=5)  # A+, A, B, etc.
    min_marks = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'grades'
        ordering = ['-min_marks']

    def __str__(self):
        return self.name


class Result(BaseModel):
    """Student Result"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    total_marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.IntegerField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True)
    is_passed = models.BooleanField(default=False)
    rank = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'results'
        unique_together = ('exam', 'student')

    def __str__(self):
        return f"{self.student} - {self.exam}"


class ReportCard(BaseModel):
    """Report Card"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='report_cards')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    term = models.CharField(max_length=50)  # First Term, Second Term, etc.
    generated_date = models.DateTimeField(auto_now_add=True)
    class_performance = models.TextField(blank=True, null=True)
    teacher_comments = models.TextField(blank=True, null=True)
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'report_cards'
        unique_together = ('student', 'academic_year', 'term')

    def __str__(self):
        return f"{self.student} - {self.academic_year} - {self.term}"


# ============ TRANSPORT MODELS ============

class TransportRoute(BaseModel):
    """Transport Route Configuration"""
    route_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    starting_point = models.CharField(max_length=100)
    ending_point = models.CharField(max_length=100)
    distance = models.DecimalField(max_digits=5, decimal_places=2)
    route_fee = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.IntegerField()
    stop_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'transport_routes'

    def __str__(self):
        return f"{self.route_number} - {self.name}"


class RouteStop(BaseModel):
    """Route Stops/Pickup Points"""
    route = models.ForeignKey(TransportRoute, on_delete=models.CASCADE, related_name='route_stops')
    stop_number = models.IntegerField()
    stop_name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    pickup_time = models.TimeField()
    dropoff_time = models.TimeField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    class Meta:
        db_table = 'route_stops'
        unique_together = ('route', 'stop_number')

    def __str__(self):
        return f"{self.route} - Stop {self.stop_number}"


class Vehicle(BaseModel):
    """Vehicle Information"""
    registration_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=50)  # Bus, Van, etc.
    model = models.CharField(max_length=100)
    capacity = models.IntegerField()
    color = models.CharField(max_length=50, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    insurance_expiry = models.DateField(blank=True, null=True)
    pollution_certificate_expiry = models.DateField(blank=True, null=True)
    route = models.ForeignKey(TransportRoute, on_delete=models.SET_NULL, null=True, blank=True, related_name='vehicles')
    is_active = models.BooleanField(default=True)
    gps_device_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'vehicles'

    def __str__(self):
        return f"{self.vehicle_type} - {self.registration_number}"


class Driver(BaseModel):
    """Driver Information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
    license_number = models.CharField(max_length=20, unique=True)
    license_expiry = models.DateField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='drivers')
    experience_years = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=15)
    address = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'drivers'

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.license_number}"


class StudentTransport(BaseModel):
    """Student Transport Assignment"""
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='transport')
    route = models.ForeignKey(TransportRoute, on_delete=models.CASCADE, related_name='assigned_students')
    route_stop = models.ForeignKey(RouteStop, on_delete=models.SET_NULL, null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    seat_number = models.IntegerField(blank=True, null=True)
    transport_fee_waived = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'student_transport'

    def __str__(self):
        return f"{self.student} - {self.route}"


class TransportAttendance(BaseModel):
    """Transport Attendance (GPS/Manual)"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='transport_attendance')
    date = models.DateField()
    picked_up = models.BooleanField()
    pickup_time = models.TimeField(blank=True, null=True)
    dropped_off = models.BooleanField()
    dropoff_time = models.TimeField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'transport_attendance'
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student} - {self.date}"


# ============ HOMEWORK & DIARY MODELS ============

class Homework(BaseModel):
    """Homework Assignment"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='homework_assigned')
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructions = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    created_date = models.DateField(auto_now_add=True)
    marks = models.IntegerField(default=0)
    file_attachment = models.FileField(upload_to='homework/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'homework'
        ordering = ['-due_date']

    def __str__(self):
        return f"{self.title} - {self.class_obj}"


class HomeworkSubmission(BaseModel):
    """Homework Submission"""
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='homework_submissions')
    submission_date = models.DateTimeField(auto_now_add=True)
    file_submission = models.FileField(upload_to='homework_submissions/')
    status = models.CharField(max_length=20, choices=[('SUBMITTED', 'Submitted'), ('LATE', 'Late'), ('MISSING', 'Missing')])
    marks_obtained = models.IntegerField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    evaluated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='homework_evaluated')

    class Meta:
        db_table = 'homework_submissions'
        unique_together = ('homework', 'student')

    def __str__(self):
        return f"{self.student} - {self.homework}"


class ClassDiary(BaseModel):
    """Class Diary Entry"""
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='diary_entries')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='diary_entries')
    date = models.DateField()
    topics_covered = models.TextField()
    homework_assigned = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'class_diary'
        unique_together = ('class_obj', 'subject', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.class_obj} - {self.subject} - {self.date}"


# ============ NOTIFICATION MODELS ============

class Notification(BaseModel):
    """Notifications/Messages"""
    NOTIFICATION_TYPES = [
        ('FEE_REMINDER', 'Fee Reminder'),
        ('EXAM_ALERT', 'Exam Alert'),
        ('BIRTHDAY', 'Birthday'),
        ('HOLIDAY', 'Holiday'),
        ('EMERGENCY', 'Emergency'),
        ('GENERAL', 'General'),
        ('ATTENDANCE', 'Attendance'),
    ]

    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications_sent')
    recipients = models.ManyToManyField(User, related_name='notifications_received')
    is_read = models.BooleanField(default=False)
    sent_date = models.DateTimeField(auto_now_add=True)
    scheduled_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-sent_date']

    def __str__(self):
        return f"{self.title} - {self.notification_type}"


class SMSLog(BaseModel):
    """SMS Sending Log"""
    recipient_phone = models.CharField(max_length=15)
    message = models.TextField()
    sms_type = models.CharField(max_length=50)
    sent_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('SENT', 'Sent'), ('FAILED', 'Failed'), ('PENDING', 'Pending')])
    gateway_response = models.TextField(blank=True, null=True)
    related_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sms_logs')

    class Meta:
        db_table = 'sms_logs'
        ordering = ['-sent_date']

    def __str__(self):
        return f"{self.recipient_phone} - {self.status}"


# ============ TIMETABLE & EVENTS MODELS ============

class TimeTable(BaseModel):
    """Time Table"""
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='timetables')
    day_of_week = models.IntegerField(choices=[(i, f'Day {i}') for i in range(1, 7)])  # 1-6 for Mon-Sat
    period_number = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='timetable_slots')
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'timetable'
        unique_together = ('class_obj', 'day_of_week', 'period_number')

    def __str__(self):
        return f"{self.class_obj} - Day {self.day_of_week} - Period {self.period_number}"


class Event(BaseModel):
    """School Events"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    event_type = models.CharField(max_length=50)  # Holiday, Function, etc.
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255, blank=True, null=True)
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='events_organized')
    is_holiday = models.BooleanField(default=False)

    class Meta:
        db_table = 'events'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} - {self.start_date}"


# ============ LIBRARY MODELS ============

class LibraryBook(BaseModel):
    """Library Books"""
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, unique=True, blank=True, null=True)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    category = models.CharField(max_length=50)
    total_copies = models.IntegerField()
    available_copies = models.IntegerField()
    book_cover = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    rack_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'library_books'

    def __str__(self):
        return self.title


class LibraryTransaction(BaseModel):
    """Book Issue/Return Transactions"""
    book = models.ForeignKey(LibraryBook, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='library_transactions')
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    fine_charged = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_returned = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'library_transactions'
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.student} - {self.book} - Issue"


# ============ INVENTORY MODELS ============

class InventoryItem(BaseModel):
    """Inventory Items"""
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=20)  # Pcs, Kg, L, etc.
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_value = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.CharField(max_length=255, blank=True, null=True)
    purchase_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100)

    class Meta:
        db_table = 'inventory_items'

    def __str__(self):
        return self.name


# ============ PAYROLL MODELS ============

class Salary(BaseModel):
    """Salary Structure"""
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='salaries')
    month = models.IntegerField()  # 1-12
    year = models.IntegerField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('PAID', 'Paid'), ('DELAYED', 'Delayed')])
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'salaries'
        unique_together = ('staff', 'month', 'year')

    def __str__(self):
        return f"{self.staff} - {self.month}/{self.year}"


# ============ COMPLAINTS & GRIEVANCES MODELS ============

class Complaint(BaseModel):
    """Complaint & Grievance System"""
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]

    complaint_id = models.CharField(max_length=50, unique=True)
    complainant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='complaints_filed')
    complaint_type = models.CharField(max_length=50)  # Academic, Behavior, Facility, etc.
    title = models.CharField(max_length=255)
    description = models.TextField()
    attachment = models.FileField(upload_to='complaints/', blank=True, null=True)
    filed_date = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='complaints_assigned')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    resolution_notes = models.TextField(blank=True, null=True)
    resolved_date = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')], default='MEDIUM')

    class Meta:
        db_table = 'complaints'
        ordering = ['-filed_date']

    def __str__(self):
        return self.complaint_id


# ============ AUDIT & SECURITY MODELS ============

class AuditLog(BaseModel):
    """Audit Logs for security and compliance"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=255)
    module = models.CharField(max_length=100)
    action_type = models.CharField(max_length=20, choices=[('CREATE', 'Create'), ('UPDATE', 'Update'), ('DELETE', 'Delete'), ('VIEW', 'View')])
    changed_data = models.JSONField(blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['module', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.module}"


class Certificate(BaseModel):
    """Certificate Generation"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='certificates')
    certificate_type = models.CharField(max_length=100)  # Completion, Transfer, etc.
    issue_date = models.DateField()
    certificate_number = models.CharField(max_length=50, unique=True)
    valid_until = models.DateField(blank=True, null=True)
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='certificates_issued')
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'certificates'

    def __str__(self):
        return f"{self.student} - {self.certificate_type}"
