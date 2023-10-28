from django.urls import path
from .views import (
    UsedView,
    AvailableCodesView,
    LoginView,
    LogoutView,
    ActivityLogView,
    PaidStatusView,
    AddEfs,
    Form,
    ActivateStaffView,
    DeactivateStaffView,
    VoidedStatusView,
    StaffView,
    AddMessageView,
    EditNoteView,
    BaseView,
    PageNotFoundView,
    AddStaff,
    ArchiveView,
    UpdateNoteView,
    DeleteNoteView
)



urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('home/', BaseView.as_view(), name='home'),
    path('used/', UsedView.as_view(), name='used'),
    path('available/', AvailableCodesView.as_view(), name='available'),
    path('form/<int:amount>', Form.as_view(), name='form'),
    path('activity/', ActivityLogView.as_view(), name='activity'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('paid/<str:money_code>', PaidStatusView.as_view(), name='paid'),
    path('voided/<str:money_code>', VoidedStatusView.as_view(), name='voided'),
    path('staff/', StaffView.as_view(), name='staff'),
    path('activate/<int:pk>', ActivateStaffView.as_view(), name='activate'),
    path('deactivate/<int:pk>', DeactivateStaffView.as_view(), name='deactivate'),
    path('add_message/', AddMessageView.as_view(), name='add_message'),
    path('edit/<str:money_code>', EditNoteView.as_view(), name='edit_note'),
    path('not-found', PageNotFoundView.as_view(), name='not-found'),
    path('add-staff', AddStaff.as_view(), name='add-staff'),
    path('archive/', ArchiveView.as_view(), name='archive'),
    path('update-note/<int:pk>', UpdateNoteView.as_view(), name='update-note'),
    path('delete-note/<int:pk>', DeleteNoteView.as_view(), name='delete-note'),
]