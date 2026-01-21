from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, AcademicYearViewSet, SchoolViewSet, ClassViewSet,
    SubjectViewSet, StudentViewSet, ParentViewSet, StaffViewSet,
    AttendanceRecordViewSet, FeeStructureViewSet, FeePaymentViewSet,
    ExamViewSet, MarkViewSet, ResultViewSet, TransportRouteViewSet,
    VehicleViewSet, HomeworkViewSet, NotificationViewSet,
    LibraryBookViewSet, ComplaintViewSet, CertificateViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'academic-years', AcademicYearViewSet)
router.register(r'schools', SchoolViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'students', StudentViewSet)
router.register(r'parents', ParentViewSet)
router.register(r'staff', StaffViewSet)
router.register(r'attendance', AttendanceRecordViewSet)
router.register(r'fee-structures', FeeStructureViewSet)
router.register(r'fee-payments', FeePaymentViewSet)
router.register(r'exams', ExamViewSet)
router.register(r'marks', MarkViewSet)
router.register(r'results', ResultViewSet)
router.register(r'transport-routes', TransportRouteViewSet)
router.register(r'vehicles', VehicleViewSet)
router.register(r'homework', HomeworkViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'library-books', LibraryBookViewSet)
router.register(r'complaints', ComplaintViewSet)
router.register(r'certificates', CertificateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
