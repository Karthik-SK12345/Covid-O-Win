from django.urls import path
from . import views
from .views import InvoiceListView, createInvoice, generate_PDF, view_PDF
from .views import autosuggest
urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login, name="login"),
    path('logout', views.logout, name='logout'),
    path("add_patient/", views.add_patient, name="add_patient"),
    path("patient_list/", views.patient_list, name="patient_list"),
    path("patient/<str:pk>", views.patient, name="patient"),
    path("autosuggest/", views.autosuggest, name="autosuggest"),
    path("autodoctor/", views.autodoctor, name="autodoctor"),
    path("info/", views.info, name="info"),
    path("covidcases/", views.stats, name="stats"),
    path("contact/", views.contact, name="contact"),
    path("closerhospitals/", views.location, name="location"),
    path("doctorsdetails/", views.doctors, name="doctors"),
    path("aboutus/", views.aboutus, name="aboutus"),
    path('list', InvoiceListView.as_view(), name="invoice-list"),
    path('create/', views.createInvoice, name="invoice-create"),
    path('invoice-detail/<id>', views.view_PDF, name='invoice-detail'),
    path('invoice-download/<id>', views.generate_PDF, name='invoice-download')
]
