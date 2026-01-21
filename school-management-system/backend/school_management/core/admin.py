from django.contrib import admin
from .models import (
    User, AcademicYear, School, Class, Subject, Student, Parent, StudentParent, Staff,
    ClassSubject, AttendanceRecord, BiometricAttendance, FeeStructure, FeeDiscount,
    FeePayment, Invoice, Exam, ExamSchedule, Mark, Grade, Result, ReportCard,
    TransportRoute, RouteStop, Vehicle, Driver, StudentTransport, TransportAttendance,
    Homework, HomeworkSubmission, ClassDiary, Notification, SMSLog, TimeTable, Event,
    LibraryBook, LibraryTransaction, InventoryItem, Salary, Complaint, AuditLog, Certificate
)


class BaseAdminConfig(admin.ModelAdmin):
    """Base admin configuration"""
    list_per_page = 50
    date_hierarchy = 'created_at'
    list_filter = ('created_at', 'updated_at')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'is_active', 'is_verified')
    list_filter = ('role', 'is_active', 'is_verified', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(School)
class SchoolAdmin(BaseAdminConfig):
    list_display = ('id', 'name', 'code', 'city', 'email')
    search_fields = ('name', 'code', 'city')


@admin.register(AcademicYear)
class AcademicYearAdmin(BaseAdminConfig):
    list_display = ('id', 'name', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date')


@admin.register(Class)
class ClassAdmin(BaseAdminConfig):
    list_display = ('id', 'name', 'class_number', 'section', 'academic_year', 'class_teacher')
    list_filter = ('class_number', 'section', 'academic_year')
    search_fields = ('name',)


@admin.register(Subject)
class SubjectAdmin(BaseAdminConfig):
    list_display = ('id', 'name', 'code', 'max_marks', 'pass_marks')
    search_fields = ('name', 'code')


@admin.register(Student)
class StudentAdmin(BaseAdminConfig):
    list_display = ('id', 'user', 'roll_number', 'admission_number', 'current_class')
    list_filter = ('current_class', 'admission_date', 'gender')
    search_fields = ('roll_number', 'admission_number', 'user__first_name', 'user__last_name')
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(Parent)
class ParentAdmin(BaseAdminConfig):
    list_display = ('id', 'user', 'occupation', 'company_name')
    search_fields = ('user__first_name', 'user__last_name', 'company_name')


@admin.register(Staff)
class StaffAdmin(BaseAdminConfig):
    list_display = ('id', 'user', 'employee_id', 'designation', 'department')
    list_filter = ('designation', 'department', 'contract_type')
    search_fields = ('employee_id', 'user__first_name', 'user__last_name')


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(BaseAdminConfig):
    list_display = ('id', 'student', 'date', 'status', 'subject')
    list_filter = ('date', 'status', 'subject')
    search_fields = ('student__roll_number',)


@admin.register(FeeStructure)
class FeeStructureAdmin(BaseAdminConfig):
    list_display = ('id', 'academic_year', 'class_obj', 'fee_type', 'amount')
    list_filter = ('academic_year', 'fee_type')


@admin.register(FeePayment)
class FeePaymentAdmin(BaseAdminConfig):
    list_display = ('id', 'student', 'amount_due', 'amount_paid', 'status', 'due_date')
    list_filter = ('status', 'payment_method', 'due_date')
    search_fields = ('student__roll_number',)


@admin.register(Exam)
class ExamAdmin(BaseAdminConfig):
    list_display = ('id', 'name', 'exam_type', 'academic_year', 'start_date', 'is_published')
    list_filter = ('exam_type', 'academic_year', 'is_published')


@admin.register(Mark)
class MarkAdmin(BaseAdminConfig):
    list_display = ('id', 'student', 'exam_schedule', 'marks_obtained', 'is_absent')
    list_filter = ('is_absent', 'entered_date')
    search_fields = ('student__roll_number',)


@admin.register(Homework)
class HomeworkAdmin(BaseAdminConfig):
    list_display = ('id', 'title', 'subject', 'class_obj', 'due_date')
    list_filter = ('class_obj', 'subject', 'due_date')
    search_fields = ('title',)


@admin.register(TransportRoute)
class TransportRouteAdmin(BaseAdminConfig):
    list_display = ('id', 'route_number', 'name', 'distance', 'route_fee')
    search_fields = ('route_number', 'name')


@admin.register(Vehicle)
class VehicleAdmin(BaseAdminConfig):
    list_display = ('id', 'registration_number', 'vehicle_type', 'capacity', 'route')
    list_filter = ('vehicle_type', 'is_active')
    search_fields = ('registration_number',)


@admin.register(LibraryBook)
class LibraryBookAdmin(BaseAdminConfig):
    list_display = ('id', 'title', 'author', 'category', 'available_copies')
    list_filter = ('category', 'publication_year')
    search_fields = ('title', 'author', 'isbn')


@admin.register(Complaint)
class ComplaintAdmin(BaseAdminConfig):
    list_display = ('id', 'complaint_id', 'complaint_type', 'status', 'priority', 'filed_date')
    list_filter = ('status', 'complaint_type', 'priority')
    search_fields = ('complaint_id', 'title')


@admin.register(AuditLog)
class AuditLogAdmin(BaseAdminConfig):
    list_display = ('id', 'user', 'action_type', 'module', 'timestamp')
    list_filter = ('action_type', 'module', 'timestamp')
    search_fields = ('user__username', 'module')
    readonly_fields = ('id', 'timestamp')


# Register remaining models with default admin
admin.site.register(StudentParent)
admin.site.register(ClassSubject)
admin.site.register(BiometricAttendance)
admin.site.register(FeeDiscount)
admin.site.register(Invoice)
admin.site.register(ExamSchedule)
admin.site.register(Grade)
admin.site.register(Result)
admin.site.register(ReportCard)
admin.site.register(RouteStop)
admin.site.register(Driver)
admin.site.register(StudentTransport)
admin.site.register(TransportAttendance)
admin.site.register(HomeworkSubmission)
admin.site.register(ClassDiary)
admin.site.register(Notification)
admin.site.register(SMSLog)
admin.site.register(TimeTable)
admin.site.register(Event)
admin.site.register(LibraryTransaction)
admin.site.register(InventoryItem)
admin.site.register(Salary)
admin.site.register(Certificate)
