# Database Schema Documentation

## Overview

The School Management System uses SQLite with UUID primary keys. All models follow a consistent pattern with timestamp tracking (created_at, updated_at).

## User & Authentication

### User Model
- **id** (UUID): Primary Key
- **username** (String): Unique username
- **email** (String): Unique email
- **password** (String): Hashed password
- **first_name** (String): First name
- **last_name** (String): Last name
- **role** (Choice): SUPER_ADMIN, ADMIN, TEACHER, STUDENT, PARENT, ACCOUNTANT, TRANSPORT_MANAGER
- **phone** (String): Contact phone number
- **profile_picture** (Image): Profile photo
- **is_active** (Boolean): Account active status
- **is_verified** (Boolean): Email/Phone verification
- **created_at**, **updated_at** (DateTime): Timestamps

## Academic Structure

### AcademicYear
- **id** (UUID): Primary Key
- **name** (String): Year identifier (e.g., "2024-2025")
- **start_date**, **end_date** (Date): Academic year duration
- **is_active** (Boolean): Current active year

### School
- **id** (UUID): Primary Key
- **name** (String): School name
- **code** (String): Unique school code
- **address**, **city**, **state**, **postal_code** (String): Location
- **phone**, **email**, **website** (String): Contact info
- **logo** (Image): School logo
- **principal_name**, **affiliation** (String): Additional info

### Class
- **id** (UUID): Primary Key
- **name** (String): Class identifier (e.g., "10A")
- **class_number** (Integer): Numeric class level (1-12)
- **section** (String): Section letter (A, B, C, etc.)
- **academic_year_id** (FK): Reference to AcademicYear
- **class_teacher_id** (FK): Reference to User (Teacher)
- **capacity** (Integer): Maximum students

### Subject
- **id** (UUID): Primary Key
- **name** (String): Subject name
- **code** (String): Unique subject code
- **description** (Text): Subject details
- **max_marks** (Integer): Total marks
- **pass_marks** (Integer): Passing marks threshold

### ClassSubject
- **id** (UUID): Primary Key
- **class_obj_id** (FK): Reference to Class
- **subject_id** (FK): Reference to Subject
- **teacher_id** (FK): Reference to User (Teacher)
- **is_mandatory** (Boolean): Required/Optional subject

## Student & Staff

### Student
- **id** (UUID): Primary Key
- **user_id** (FK): Reference to User (OneToOne)
- **roll_number** (String): Unique roll number
- **admission_number** (String): Unique admission number
- **admission_date** (Date): Admission date
- **current_class_id** (FK): Reference to Class
- **date_of_birth** (Date): DOB
- **gender** (Choice): M, F, O
- **blood_group** (String): Blood group
- **aadhar_number** (String): Masked Aadhar (privacy)
- **father_name**, **mother_name**, **guardian_name** (String): Parents/Guardian names
- **guardian_phone**, **address** (String): Contact info
- **previous_school** (String): Previous school name

### Parent
- **id** (UUID): Primary Key
- **user_id** (FK): Reference to User (OneToOne)
- **occupation** (String): Job/profession
- **company_name** (String): Company name
- **annual_income** (Decimal): Income (optional)
- **address** (Text): Residential address
- **alternate_phone** (String): Alternative contact

### StudentParent (Junction Table)
- **id** (UUID): Primary Key
- **student_id** (FK): Reference to Student
- **parent_id** (FK): Reference to Parent
- **relationship** (String): Father, Mother, Guardian, etc.
- **is_primary_contact** (Boolean): Primary contact person

### Staff
- **id** (UUID): Primary Key
- **user_id** (FK): Reference to User (OneToOne)
- **employee_id** (String): Unique employee ID
- **designation** (String): Job title
- **department** (String): Department
- **qualification** (String): Qualifications
- **experience_years** (Integer): Work experience
- **date_of_birth** (Date): DOB
- **gender** (Choice): M, F, O
- **date_of_joining** (Date): Joining date
- **salary** (Decimal): Monthly salary
- **contract_type** (Choice): PERMANENT, TEMPORARY
- **address** (Text): Address
- **account_number**, **bank_name**, **ifsc_code** (String): Banking details

## Attendance

### AttendanceRecord
- **id** (UUID): Primary Key
- **student_id** (FK): Reference to Student
- **date** (Date): Attendance date (indexed)
- **status** (Choice): PRESENT, ABSENT, LEAVE, LATE
- **subject_id** (FK): Reference to Subject (Optional, for subject-wise)
- **marked_by_id** (FK): Reference to User (Teacher)
- **remarks** (Text): Notes
- **Unique**: (student, date, subject)

### BiometricAttendance
- **id** (UUID): Primary Key
- **student_id** (FK): Reference to Student
- **date** (Date): Attendance date
- **time_in**, **time_out** (Time): Entry/exit times
- **biometric_id** (String): Device biometric ID
- **device_id** (String): Biometric device identifier

## Fees & Payments

### FeeStructure
- **id** (UUID): Primary Key
- **academic_year_id** (FK): Reference to AcademicYear
- **class_obj_id** (FK): Reference to Class
- **fee_type** (String): Tuition, Transport, Activities, etc.
- **amount** (Decimal): Fee amount
- **frequency** (Choice): MONTHLY, QUARTERLY, ANNUAL
- **due_date** (Date): Payment due date
- **is_active** (Boolean): Current structure
- **Unique**: (academic_year, class, fee_type)

### FeeDiscount
- **id** (UUID): Primary Key
- **name** (String): Discount name
- **discount_type** (Choice): PERCENTAGE, FIXED
- **discount_value** (Decimal): Discount amount/percentage
- **applicable_for** (ManyToMany): Students eligible
- **valid_from**, **valid_to** (Date): Validity period
- **is_active** (Boolean): Active discount

### FeePayment
- **id** (UUID): Primary Key
- **student_id** (FK): Reference to Student
- **fee_structure_id** (FK): Reference to FeeStructure
- **amount_due** (Decimal): Total amount due
- **amount_paid** (Decimal): Amount paid so far
- **due_date** (Date): Payment deadline
- **payment_date** (Date): Actual payment date
- **status** (Choice): PENDING, PARTIAL, PAID, OVERDUE
- **payment_method** (Choice): CASH, CHEQUE, BANK_TRANSFER, ONLINE
- **transaction_id** (String): Payment gateway transaction ID
- **received_by_id** (FK): Reference to User (Accountant)
- **remarks** (Text): Notes

### Invoice
- **id** (UUID): Primary Key
- **student_id** (FK): Reference to Student
- **invoice_number** (String): Unique invoice number
- **total_amount** (Decimal): Total amount
- **discount_amount** (Decimal): Discount applied
- **net_amount** (Decimal): Final amount
- **issued_date**, **due_date** (Date): Dates
- **period_from**, **period_to** (Date): Billing period
- **is_paid** (Boolean): Payment status
- **notes** (Text): Notes

## Examinations

### Exam
- **id** (UUID): Primary Key
- **name** (String): Exam name
- **exam_type** (String): Unit Test, Half Yearly, Final, etc.
- **academic_year_id** (FK): Reference to AcademicYear
- **start_date**, **end_date** (Date): Exam period
- **result_published_date** (Date): Results publication date
- **is_published** (Boolean): Results published flag

### ExamSchedule
- **id** (UUID): Primary Key
- **exam_id** (FK): Reference to Exam
- **class_obj_id** (FK): Reference to Class
- **subject_id** (FK): Reference to Subject
- **exam_date** (Date): Exam date
- **start_time**, **end_time** (Time): Exam timing
- **total_marks** (Integer): Total marks for exam
- **room_number** (String): Exam room
- **Unique**: (exam, class, subject)

### Mark
- **id** (UUID): Primary Key
- **exam_schedule_id** (FK): Reference to ExamSchedule
- **student_id** (FK): Reference to Student
- **marks_obtained** (Decimal): Marks scored
- **is_absent** (Boolean): Absence flag
- **remarks** (Text): Comments
- **entered_by_id** (FK): Reference to User (Teacher)
- **entered_date** (DateTime): Entry timestamp
- **Unique**: (exam_schedule, student)

### Grade
- **id** (UUID): Primary Key
- **name** (String): Grade symbol (A+, A, B, etc.)
- **min_marks**, **max_marks** (Decimal): Grade range
- **description** (String): Grade description

### Result
- **id** (UUID): Primary Key
- **exam_id** (FK): Reference to Exam
- **student_id** (FK): Reference to Student
- **total_marks_obtained** (Decimal): Sum of all marks
- **total_marks** (Integer): Total possible marks
- **percentage** (Decimal): Score percentage
- **grade_id** (FK): Reference to Grade
- **is_passed** (Boolean): Pass/Fail status
- **rank** (Integer): Class rank
- **Unique**: (exam, student)

### ReportCard
- **id** (UUID): Primary Key
- **student_id** (FK): Reference to Student
- **academic_year_id** (FK): Reference to AcademicYear
- **term** (String): First Term, Second Term, etc.
- **generated_date** (DateTime): Generation timestamp
- **class_performance** (Text): Performance analysis
- **teacher_comments** (Text): Teacher comments
- **attendance_percentage** (Decimal): Attendance %
- **Unique**: (student, academic_year, term)

## Transport

### TransportRoute
- **id** (UUID): Primary Key
- **route_number** (String): Unique route identifier
- **name** (String): Route name
- **starting_point**, **ending_point** (String): Locations
- **distance** (Decimal): Route distance (km)
- **route_fee** (Decimal): Monthly fee
- **duration_minutes** (Integer): Estimated duration
- **stops** (Integer): Number of stops

### RouteStop
- **id** (UUID): Primary Key
- **route_id** (FK): Reference to TransportRoute
- **stop_number** (Integer): Sequential stop number
- **stop_name** (String): Stop name/location
- **location** (String): Full address
- **pickup_time**, **dropoff_time** (Time): Timings
- **latitude**, **longitude** (Decimal): GPS coordinates
- **Unique**: (route, stop_number)

### Vehicle
- **id** (UUID): Primary Key
- **registration_number** (String): Vehicle registration
- **vehicle_type** (String): Bus, Van, etc.
- **model** (String): Vehicle model
- **capacity** (Integer): Seating capacity
- **color** (String): Vehicle color
- **purchase_date** (Date): Purchase date
- **insurance_expiry**, **pollution_certificate_expiry** (Date): Document expiry
- **route_id** (FK): Reference to TransportRoute
- **is_active** (Boolean): Active vehicle
- **gps_device_id** (String): GPS tracking device ID

### Driver
- **id** (UUID): Primary Key
- **user_id** (FK): Reference to User (OneToOne)
- **license_number** (String): Driver license number
- **license_expiry** (Date): License expiry
- **vehicle_id** (FK): Reference to Vehicle
- **experience_years** (Integer): Driving experience
- **phone_number**, **emergency_contact** (String): Contacts
- **address** (Text): Address
- **is_active** (Boolean): Active status

### StudentTransport
- **id** (UUID): Primary Key
- **student_id** (FK): Reference to Student (OneToOne)
- **route_id** (FK): Reference to TransportRoute
- **route_stop_id** (FK): Reference to RouteStop
- **vehicle_id** (FK): Reference to Vehicle
- **seat_number** (Integer): Assigned seat
- **transport_fee_waived** (Boolean): Fee waiver status
- **is_active** (Boolean): Current assignment

### TransportAttendance
- **id** (UUID): Primary Key
- **student_id** (FK): Reference to Student
- **date** (Date): Attendance date
- **picked_up** (Boolean): Pickup status
- **pickup_time** (Time): Pickup timestamp
- **dropped_off** (Boolean): Dropoff status
- **dropoff_time** (Time): Dropoff timestamp
- **remarks** (Text): Notes
- **Unique**: (student, date)

## Academics - Homework & Diary

### Homework
- **id** (UUID): Primary Key
- **subject_id** (FK): Reference to Subject
- **class_obj_id** (FK): Reference to Class
- **teacher_id** (FK): Reference to User (Teacher)
- **title** (String): Assignment title
- **description** (Text): Detailed description
- **instructions** (Text): How to submit
- **due_date** (Date): Submission deadline
- **created_date** (Date): Creation date
- **marks** (Integer): Marks allocated
- **file_attachment** (File): Assignment file
- **is_active** (Boolean): Assignment active

### HomeworkSubmission
- **id** (UUID): Primary Key
- **homework_id** (FK): Reference to Homework
- **student_id** (FK): Reference to Student
- **submission_date** (DateTime): Submission timestamp
- **file_submission** (File): Student's submission file
- **status** (Choice): SUBMITTED, LATE, MISSING
- **marks_obtained** (Integer): Marks awarded
- **feedback** (Text): Teacher feedback
- **evaluated_by_id** (FK): Reference to User (Teacher)
- **Unique**: (homework, student)

### ClassDiary
- **id** (UUID): Primary Key
- **class_obj_id** (FK): Reference to Class
- **subject_id** (FK): Reference to Subject
- **teacher_id** (FK): Reference to User
- **date** (Date): Class date
- **topics_covered** (Text): Topics taught
- **homework_assigned** (Text): Homework details
- **remarks** (Text): Class notes/remarks
- **created_date** (DateTime): Entry timestamp
- **Unique**: (class, subject, date)

## Communication

### Notification
- **id** (UUID): Primary Key
- **title** (String): Notification title
- **message** (Text): Message content
- **notification_type** (Choice): FEE_REMINDER, EXAM_ALERT, BIRTHDAY, HOLIDAY, EMERGENCY, GENERAL, ATTENDANCE
- **sender_id** (FK): Reference to User
- **recipients** (ManyToMany): Target users
- **is_read** (Boolean): Read status
- **sent_date** (DateTime): Sending timestamp
- **scheduled_date** (DateTime): Scheduled for (future)

### SMSLog
- **id** (UUID): Primary Key
- **recipient_phone** (String): Phone number
- **message** (Text): SMS content
- **sms_type** (String): Type of SMS
- **sent_date** (DateTime): Sending timestamp
- **status** (Choice): SENT, FAILED, PENDING
- **gateway_response** (Text): API response
- **related_user_id** (FK): Reference to User

## Timetable & Events

### TimeTable
- **id** (UUID): Primary Key
- **class_obj_id** (FK): Reference to Class
- **day_of_week** (Integer): 1-6 (Mon-Sat)
- **period_number** (Integer): Period sequence
- **subject_id** (FK): Reference to Subject
- **teacher_id** (FK): Reference to User
- **start_time**, **end_time** (Time): Period timing
- **room_number** (String): Classroom number
- **Unique**: (class, day, period)

### Event
- **id** (UUID): Primary Key
- **name** (String): Event name
- **description** (Text): Event details
- **event_type** (String): Holiday, Function, Sports, etc.
- **start_date**, **end_date** (Date): Event duration
- **location** (String): Event venue
- **organizer_id** (FK): Reference to User
- **is_holiday** (Boolean): School holiday flag

## Library

### LibraryBook
- **id** (UUID): Primary Key
- **title** (String): Book title
- **isbn** (String): ISBN number
- **author** (String): Author name
- **publisher** (String): Publisher
- **publication_year** (Integer): Year published
- **category** (String): Genre/Category
- **total_copies** (Integer): Total books owned
- **available_copies** (Integer): Available for issue
- **book_cover** (Image): Cover image
- **description** (Text): Book description
- **rack_number** (String): Library rack location

### LibraryTransaction
- **id** (UUID): Primary Key
- **book_id** (FK): Reference to LibraryBook
- **student_id** (FK): Reference to Student
- **issue_date** (Date): Issuance date
- **due_date** (Date): Return due date
- **return_date** (Date): Actual return date
- **fine_charged** (Decimal): Late fine
- **is_returned** (Boolean): Return status
- **remarks** (Text): Notes

## Inventory & Payroll

### InventoryItem
- **id** (UUID): Primary Key
- **name** (String): Item name
- **category** (String): Item category
- **description** (Text): Details
- **quantity** (Integer): Current quantity
- **unit** (String): Unit of measurement
- **purchase_price** (Decimal): Cost per unit
- **current_value** (Decimal): Current stock value
- **supplier** (String): Supplier name
- **purchase_date** (Date): Purchase date
- **expiry_date** (Date): Expiration date
- **location** (String): Storage location

### Salary
- **id** (UUID): Primary Key
- **staff_id** (FK): Reference to Staff
- **month** (Integer): 1-12
- **year** (Integer): Year
- **basic_salary** (Decimal): Base salary
- **deductions** (Decimal): Total deductions
- **allowances** (Decimal): Allowances
- **net_salary** (Decimal): Final salary
- **payment_date** (Date): Payment date
- **payment_status** (Choice): PENDING, PAID, DELAYED
- **remarks** (Text): Notes
- **Unique**: (staff, month, year)

## Complaints & Compliance

### Complaint
- **id** (UUID): Primary Key
- **complaint_id** (String): Unique complaint number
- **complainant_id** (FK): Reference to User
- **complaint_type** (String): Academic, Behavior, Facility, etc.
- **title** (String): Complaint title
- **description** (Text): Detailed complaint
- **attachment** (File): Supporting document
- **filed_date** (DateTime): Filing timestamp
- **assigned_to_id** (FK): Reference to User (Handler)
- **status** (Choice): OPEN, IN_PROGRESS, RESOLVED, CLOSED
- **resolution_notes** (Text): Resolution details
- **resolved_date** (DateTime): Resolution timestamp
- **priority** (Choice): LOW, MEDIUM, HIGH

### AuditLog
- **id** (UUID): Primary Key
- **user_id** (FK): Reference to User
- **action** (String): Action performed
- **module** (String): System module (Students, Fees, etc.)
- **action_type** (Choice): CREATE, UPDATE, DELETE, VIEW
- **changed_data** (JSON): Data changes
- **ip_address** (IPAddress): Request IP
- **timestamp** (DateTime): Action timestamp
- **Indexes**: (user, timestamp), (module, timestamp)

### Certificate
- **id** (UUID): Primary Key
- **student_id** (FK): Reference to Student
- **certificate_type** (String): Completion, Transfer, etc.
- **issue_date** (Date): Issue date
- **certificate_number** (String): Unique certificate number
- **valid_until** (Date): Validity period
- **issued_by_id** (FK): Reference to User (Principal)
- **remarks** (Text): Notes

## Indexing Strategy

For performance optimization, the following fields are indexed:

- `AttendanceRecord.date` - Frequent date-based queries
- `User.email, User.username` - Unique lookups
- `Student.roll_number, Student.admission_number` - Frequent searches
- `AuditLog.user, AuditLog.module, AuditLog.timestamp` - Audit trail queries
- `FeePayment.due_date, FeePayment.status` - Fee queries
- `Mark.exam_schedule, Mark.student` - Result lookups

## Data Integrity

- Foreign keys enforce referential integrity
- Unique constraints prevent duplicate records
- Check constraints validate data ranges
- Timestamps track record modifications
- UUID ensures distributed system compatibility
