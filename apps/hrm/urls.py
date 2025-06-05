from django.urls import path 
from apps.hrm.views import *
from apps.hrm.employee import *
from apps.hrm.manager import *
from apps.hrm.hr import *

urlpatterns = [
    
    # HRM Admin Dashboard
    path('admin/hrm/home/', hrmDashboard, name='hrmDashboard'),    
    
    # Others Dashboard
    path('hrm/manager/dashboard/', hrmManagerDashboard, name='hrmManagerDashboard'),
    path('hrm/hr/dashboard/', hrmHrDashboard, name='hrmHrDashboard'),
    path('hrm/employee/dashboard/', hrmEmployeeDashboard, name='hrmEmployeeDashboard'),
    
    # Payroll
    path('hrm/payroll/', hrmPayroll, name='hrmPayroll'),
    path('hrm/payroll/details/<int:id>/', hrmPayrollDetail, name='hrmPayrollDetail'),
    path('hrm/payroll/delete/<int:id>/', hrmPayrollDelete, name='hrmPayrollDelete'),
    
    path('hrm/payroll/salary/edit/<int:id>/', salaryEdit, name='salaryEdit'),
    path('hrm/payroll/salary/delete/<int:id>/', salaryDelete, name='salaryDelete'),
    
    path('hrm/payroll/allowance/edit/<int:id>/', allowanceEdit, name='allowanceEdit'),
    path('hrm/payroll/allowance/delete/<int:id>/', allowanceDelete, name='allowanceDelete'),
    
    path('hrm/payroll/deduction/edit/<int:id>/', deductionEdit, name='deductionEdit'),
    path('hrm/payroll/deduction/delete/<int:id>/', deductionDelete, name='deductionDelete'),
    
    path('hrm/payslips/', hrmPayslip, name='hrmPayslip'),
    path('hrm/payslip/<int:id>/mark-as-paid/', hrmPayslipMarkPaid, name='hrmPayslipMarkPaid'),
    path('hrm/payslip/email/<int:id>/', emailPyslip, name='emailPyslip'),
    path('hrm/payslip/<int:id>/', hrmPayslipDetail, name='hrmPayslipDetail'),
    
    # Events
    path("hrm/event/calender/", CalendarViewNew.as_view(), name="calendar"),
    path('delete_event/<int:event_id>/', delete_event, name='delete_event'),
    path('next_week/<int:event_id>/', next_week, name='next_week'),
    path('next_day/<int:event_id>/', next_day, name='next_day'),
    
    # Admin Employee
    path('hrm/employees/', hrmEmployeeList, name='hrmEmployeeList'),
    path('hrm/employee/edit/<str:slug>/', hrmEmployeeEdit, name='hrmEmployeeEdit'),
    path('hrm/employee/delete/<str:slug>/', hrmEmployeeDelete, name='hrmEmployeeDelete'),
    
    # Admin Manager
    path('hrm/managers/', hrmManagerList, name='hrmManagerList'),
    path('hrm/manager/edit/<str:slug>/', hrmManagerEdit, name='hrmManagerEdit'),
    path('hrm/manager/delete/<str:slug>/', hrmManagerDelete, name='hrmManagerDelete'),
    
    # Admin Hr
    path('hrm/hrs/', hrmHrList, name='hrmHrList'),
    path('hrm/hr/edit/<str:slug>/', hrmHrEdit, name='hrmHrEdit'),
    path('hrm/hr/delete/<str:slug>/', hrmHrDelete, name='hrmHrDelete'),
    
    # Admin Branch
    path('hrm/branches/', hrmBranch, name='hrmBranch'),
    path('hrm/branch/edit/<int:id>/', hrmBranchEdit, name='hrmBranchEdit'),
    path('hrm/branch/delete/<int:id>/', hrmBranchDelete, name='hrmBranchDelete'),
    
    # Admin Department
    path('hrm/departments/', hrmDepartment, name='hrmDepartment'),
    path('hrm/department/edit/<int:id>/', hrmDepartmentEdit, name='hrmDepartmentEdit'),
    path('hrm/department/delete/<int:id>/', hrmDepartmentDelete, name='hrmDepartmentDelete'),
    
    # Admin Designation
    path('hrm/designations/', hrmDesignation, name='hrmDesignation'),
    path('hrm/designation/edit/<int:id>/', hrmDesignationEdit, name='hrmDesignationEdit'),
    path('hrm/designation/delete/<int:id>/', hrmDesignationDelete, name='hrmDesignationDelete'),
    
    # Admin Job Type
    path('hrm/job-types/', hrmJobType, name='hrmJobType'),
    path('hrm/job-type/edit/<int:id>/', hrmJobTypeEdit, name='hrmJobTypeEdit'),
    path('hrm/job-type/delete/<int:id>/', hrmJobTypeDelete, name='hrmJobTypeDelete'),
    
    # Admin Notice
    path('hrm/notices/', hrmNotices, name='hrmNotices'),
    path('hrm/notice/edit/<int:id>/', hrmNoticeEdit, name='hrmNoticeEdit'),
    path('hrm/notice/delete/<int:id>/', hrmNoticeDelete, name='hrmNoticeDelete'),
    
    # Admin Holiday
    path('hrm/holidays/', hrmHolidays, name='hrmHolidays'),
    path('hrm/holiday/edit/<int:id>/', hrmHolidayEdit, name='hrmHolidayEdit'),
    path('hrm/holiday/delete/<int:id>/', hrmHolidayDelete, name='hrmHolidayDelete'),
    
    # Admin Leave Types
    path('hrm/leave-types/', hrmLeaveTypes, name='hrmLeaveTypes'),
    path('hrm/leave-type/edit/<int:id>/', hrmLeaveTypeEdit, name='hrmLeaveTypeEdit'),
    path('hrm/leave-type/delete/<int:id>/', hrmLeaveTypeDelete, name='hrmLeaveTypeDelete'),
    
    # Admin Leave
    path('hrm/leaves/', hrmLeaves, name='hrmLeaves'),
    path('hrm/leave/edit/<int:id>/', hrmLeaveEdit, name='hrmLeaveEdit'),
    path('hrm/leave/mark-as-approved/<int:id>/', hrmLeaveMarkApproved, name='hrmLeaveMarkApproved'),
    path('hrm/leave/delete/<int:id>/', hrmLeaveDelete, name='hrmLeaveDelete'),
    
    # Admin Meeting
    path('hrm/meetings/', hrmMeetings, name='hrmMeetings'),
    path('hrm/meeting/edit/<int:id>/', hrmMeetingEdit, name='hrmMeetingEdit'),
    path('hrm/meeting/delete/<int:id>/', hrmMeetingDelete, name='hrmMeetingDelete'),
    
    # Admin Warning
    path('hrm/warnings/', hrmWarnings, name='hrmWarnings'),
    path('hrm/warning/edit/<int:id>/', hrmWarningEdit, name='hrmWarningEdit'),
    path('hrm/warning/delete/<int:id>/', hrmWarningDelete, name='hrmWarningDelete'),
    
    # Admin Termination Type
    path('hrm/termination-types/', hrmTerminationTypes, name='hrmTerminationTypes'),
    path('hrm/termination-type/edit/<int:id>/', hrmTerminationTypeEdit, name='hrmTerminationTypeEdit'),
    path('hrm/termination-type/delete/<int:id>/', hrmTerminationTypeDelete, name='hrmTerminationTypeDelete'),
    
    # Admin Termination
    path('hrm/terminations/', hrmTerminations, name='hrmTerminations'),
    path('hrm/termination/delete/<int:id>/', hrmTerminationDelete, name='hrmTerminationDelete'),
    
    # Notificaton
    path('notification/<int:notification_id>/mark_as_read/', mark_notification_as_read, name='mark_notification_as_read'),
    
    # Employe Salary Details
    path('hrm/employee/salary/details', hrmEmployeeSalaryDetails, name='hrmEmployeeSalaryDetails'),
    
    # Employee Projects
    path('hrm/employee/projects/', hrmEmployeeProjects, name='hrmEmployeeProjects'),
    path('hrm/employee/project/<str:slug>/', hrmEmployeeProjectTask, name='hrmEmployeeProjectTask'),
    
    # Attendance
    path('hrm/attendance/all-records/', hrmAttendanceRecordByByDateMonthYear, name='hrmAttendanceRecordByByDateMonthYear'),
    path('hrm/attendance/', hrmAttendance, name='hrmAttendance'),
    path('hrm/attendance/records/', hrmAttendanceRecord, name='hrmAttendanceRecord'),
]
