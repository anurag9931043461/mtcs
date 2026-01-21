from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from school_management.core.models import (
    User, AcademicYear, School, Class, Subject, Student, Parent, Staff,
    AttendanceRecord, FeeStructure, FeePayment, Exam, Mark, Result,
    TransportRoute, Vehicle, Homework, Notification, LibraryBook,
    Complaint, Certificate
)
from .serializers import (
    UserSerializer, AcademicYearSerializer, SchoolSerializer, ClassSerializer,
    SubjectSerializer, StudentSerializer, ParentSerializer, StaffSerializer,
    AttendanceRecordSerializer, FeeStructureSerializer, FeePaymentSerializer,
    ExamSerializer, MarkSerializer, ResultSerializer, TransportRouteSerializer,
    VehicleSerializer, HomeworkSerializer, NotificationSerializer,
    LibraryBookSerializer, ComplaintSerializer, CertificateSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['role', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['created_at', 'first_name']

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current user profile"""
        if not request.user.is_authenticated:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_active']
    ordering_fields = ['start_date']

    @action(detail=False, methods=['get'])
    def active_year(self, request):
        """Get active academic year"""
        active_year = AcademicYear.objects.filter(is_active=True).first()
        if active_year:
            serializer = self.get_serializer(active_year)
            return Response(serializer.data)
        return Response({'error': 'No active academic year'}, status=status.HTTP_404_NOT_FOUND)


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['academic_year', 'class_number']
    search_fields = ['name']


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    search_fields = ['name', 'code']


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['current_class', 'gender']
    search_fields = ['roll_number', 'admission_number', 'user__first_name', 'user__last_name']

    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        """Get student attendance records"""
        student = self.get_object()
        records = student.attendance_records.all()
        serializer = AttendanceRecordSerializer(records, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def fee_details(self, request, pk=None):
        """Get student fee details"""
        student = self.get_object()
        payments = student.fee_payments.all()
        serializer = FeePaymentSerializer(payments, many=True)
        return Response(serializer.data)


class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    search_fields = ['user__first_name', 'user__last_name', 'company_name']


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['designation', 'department']
    search_fields = ['employee_id', 'user__first_name', 'user__last_name']


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['student', 'date', 'status']
    ordering_fields = ['-date']

    @action(detail=False, methods=['post'])
    def bulk_mark(self, request):
        """Bulk mark attendance"""
        records_data = request.data.get('records', [])
        created_records = []
        for record in records_data:
            serializer = self.get_serializer(data=record)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            created_records.append(serializer.data)
        return Response(created_records, status=status.HTTP_201_CREATED)


class FeeStructureViewSet(viewsets.ModelViewSet):
    queryset = FeeStructure.objects.all()
    serializer_class = FeeStructureSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['academic_year', 'class_obj', 'fee_type']


class FeePaymentViewSet(viewsets.ModelViewSet):
    queryset = FeePayment.objects.all()
    serializer_class = FeePaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['student', 'status', 'payment_method']
    ordering_fields = ['-due_date']

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue payments"""
        from django.utils import timezone
        overdue_payments = FeePayment.objects.filter(
            status__in=['PENDING', 'PARTIAL'],
            due_date__lt=timezone.now().date()
        )
        serializer = self.get_serializer(overdue_payments, many=True)
        return Response(serializer.data)


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['academic_year', 'exam_type']

    @action(detail=True, methods=['post'])
    def publish_results(self, request, pk=None):
        """Publish exam results"""
        exam = self.get_object()
        exam.is_published = True
        exam.save()
        return Response({'status': 'Results published'})


class MarkViewSet(viewsets.ModelViewSet):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['exam_schedule', 'student']

    @action(detail=False, methods=['post'])
    def bulk_upload(self, request):
        """Bulk upload marks"""
        marks_data = request.data.get('marks', [])
        created_marks = []
        for mark in marks_data:
            serializer = self.get_serializer(data=mark)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            created_marks.append(serializer.data)
        return Response(created_marks, status=status.HTTP_201_CREATED)


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['exam', 'student']


class TransportRouteViewSet(viewsets.ModelViewSet):
    queryset = TransportRoute.objects.all()
    serializer_class = TransportRouteSerializer
    search_fields = ['route_number', 'name']


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['vehicle_type', 'route', 'is_active']
    search_fields = ['registration_number']


class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['class_obj', 'subject']
    ordering_fields = ['-due_date']


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['notification_type']
    ordering_fields = ['-sent_date']

    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread notifications for current user"""
        notifications = Notification.objects.filter(recipients=request.user, is_read=False)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)


class LibraryBookViewSet(viewsets.ModelViewSet):
    queryset = LibraryBook.objects.all()
    serializer_class = LibraryBookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'author', 'isbn']


class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'complaint_type', 'priority']
    ordering_fields = ['-filed_date']


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['certificate_type', 'student']


class TokenAuthView(APIView):
    """Custom token authentication view"""
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Missing username or password'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id})
