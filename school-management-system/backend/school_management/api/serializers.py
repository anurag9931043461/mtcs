from rest_framework import serializers
from school_management.core.models import (
    User, AcademicYear, School, Class, Subject, Student, Parent, Staff,
    AttendanceRecord, FeeStructure, FeePayment, Exam, Mark, Result,
    TransportRoute, Vehicle, Homework, Notification, LibraryBook,
    Complaint, Certificate
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'is_active']
        read_only_fields = ['id']


class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = ['id', 'name', 'start_date', 'end_date', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'code', 'address', 'city', 'state', 'postal_code', 'phone', 'email', 'website']
        read_only_fields = ['id']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'description', 'max_marks', 'pass_marks']
        read_only_fields = ['id']


class ClassSerializer(serializers.ModelSerializer):
    class_teacher_name = serializers.CharField(source='class_teacher.get_full_name', read_only=True)
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)

    class Meta:
        model = Class
        fields = ['id', 'name', 'class_number', 'section', 'academic_year', 'academic_year_name',
                  'class_teacher', 'class_teacher_name', 'capacity', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class StudentSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user', read_only=True)
    class_name = serializers.CharField(source='current_class.name', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'user_info', 'roll_number', 'admission_number', 'admission_date',
                  'current_class', 'class_name', 'date_of_birth', 'gender', 'father_name', 'mother_name']
        read_only_fields = ['id']


class ParentSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Parent
        fields = ['id', 'user', 'user_info', 'occupation', 'company_name', 'address']
        read_only_fields = ['id']


class StaffSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Staff
        fields = ['id', 'user', 'user_info', 'employee_id', 'designation', 'department',
                  'qualification', 'date_of_joining', 'salary']
        read_only_fields = ['id']


class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = ['id', 'student', 'student_name', 'date', 'status', 'subject', 'subject_name', 'remarks']
        read_only_fields = ['id']


class FeeStructureSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='class_obj.name', read_only=True)

    class Meta:
        model = FeeStructure
        fields = ['id', 'academic_year', 'class_obj', 'class_name', 'fee_type', 'amount', 'frequency', 'due_date']
        read_only_fields = ['id']


class FeePaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)

    class Meta:
        model = FeePayment
        fields = ['id', 'student', 'student_name', 'amount_due', 'amount_paid', 'status',
                  'due_date', 'payment_date', 'payment_method', 'transaction_id']
        read_only_fields = ['id']


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'name', 'description', 'exam_type', 'academic_year', 'start_date',
                  'end_date', 'result_published_date', 'is_published']
        read_only_fields = ['id']


class MarkSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='exam_schedule.subject.name', read_only=True)

    class Meta:
        model = Mark
        fields = ['id', 'exam_schedule', 'student', 'student_name', 'marks_obtained', 'is_absent', 'subject_name']
        read_only_fields = ['id']


class ResultSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    grade_name = serializers.CharField(source='grade.name', read_only=True)

    class Meta:
        model = Result
        fields = ['id', 'exam', 'student', 'student_name', 'total_marks_obtained', 'total_marks',
                  'percentage', 'grade', 'grade_name', 'is_passed', 'rank']
        read_only_fields = ['id']


class TransportRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportRoute
        fields = ['id', 'route_number', 'name', 'starting_point', 'ending_point', 'distance', 'route_fee']
        read_only_fields = ['id']


class VehicleSerializer(serializers.ModelSerializer):
    route_name = serializers.CharField(source='route.name', read_only=True)

    class Meta:
        model = Vehicle
        fields = ['id', 'registration_number', 'vehicle_type', 'model', 'capacity', 'route', 'route_name', 'is_active']
        read_only_fields = ['id']


class HomeworkSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_name = serializers.CharField(source='class_obj.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)

    class Meta:
        model = Homework
        fields = ['id', 'subject', 'subject_name', 'class_obj', 'class_name', 'teacher', 'teacher_name',
                  'title', 'description', 'due_date', 'marks', 'is_active']
        read_only_fields = ['id']


class NotificationSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'notification_type', 'sender', 'sender_name', 'sent_date', 'is_read']
        read_only_fields = ['id', 'sent_date']


class LibraryBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryBook
        fields = ['id', 'title', 'isbn', 'author', 'publisher', 'category', 'total_copies',
                  'available_copies', 'publication_year']
        read_only_fields = ['id']


class ComplaintSerializer(serializers.ModelSerializer):
    complainant_name = serializers.CharField(source='complainant.get_full_name', read_only=True)

    class Meta:
        model = Complaint
        fields = ['id', 'complaint_id', 'complainant', 'complainant_name', 'complaint_type',
                  'title', 'status', 'priority', 'filed_date', 'resolved_date']
        read_only_fields = ['id', 'complaint_id', 'filed_date']


class CertificateSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)

    class Meta:
        model = Certificate
        fields = ['id', 'student', 'student_name', 'certificate_type', 'certificate_number',
                  'issue_date', 'valid_until']
        read_only_fields = ['id']
