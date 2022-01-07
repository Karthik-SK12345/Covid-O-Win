from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from .filters import PatientFilter
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# PatientFilter = OrderFilter
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.template.loader import get_template
from django.http import HttpResponse
from django.views import View
from .models import LineItem, Invoice
from .forms import LineItemFormset, InvoiceForm
# Create your vie

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')
        else:
            return render(request, 'main/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')




def dashboard(request):
    patients = Patient.objects.all()
    patient_count = patients.count()
    patients_recovered = Patient.objects.filter(status="Recovered")
    patients_deceased = Patient.objects.filter(status="Deceased")
    deceased_count = patients_deceased.count()
    recovered_count = patients_recovered.count()
    beds = Bed.objects.all()
    beds_available = Bed.objects.filter(occupied=False).count()
    context = {
        'patient_count': patient_count,
        'recovered_count': recovered_count,
        'beds_available': beds_available,
        'deceased_count':deceased_count,
        'beds':beds
    }
    print(patient_count)
    return render(request, 'main/dashboard.html', context)

def add_patient(request):
    beds = Bed.objects.filter(occupied=False)
    doctors = Doctor.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        phone_num = request.POST['phone_num']
        patient_relative_name = request.POST['patient_relative_name']
        patient_relative_contact = request.POST['patient_relative_contact']
        address = request.POST['address']
        symptoms = request.POST['symptoms']
        prior_ailments = request.POST['prior_ailments']
        bed_num_sent = request.POST['bed_num']
        bed_num = Bed.objects.get(bed_number=bed_num_sent)
        dob = request.POST['dob']
        status = request.POST['status']
        doctor = request.POST['doctor']
        doctor = Doctor.objects.get(name=doctor)
        print(request.POST)
        patient = Patient.objects.create(
            name = name,
        phone_num = phone_num,
        patient_relative_name = patient_relative_name,
        patient_relative_contact = patient_relative_contact, 
        address = address, 
        symptoms = symptoms, 
        prior_ailments = prior_ailments, 
        bed_num = bed_num,
        dob = dob, 
        doctor=doctor,
        status = status
        )
        patient.save()

        bed = Bed.objects.get(bed_number=bed_num_sent)
        bed.occupied = True
        bed.save()
        id = patient.id
        return redirect(f"/patient/{id}")
        
    context = {
        'beds': beds,
        'doctors': doctors
    }
    return render(request, 'main/add_patient.html', context)

def patient(request, pk):
    patient = Patient.objects.get(id=pk)
    if request.method == "POST":
        doctor = request.POST['doctor']
        doctor_time = request.POST['doctor_time']
        doctor_notes = request.POST['doctor_notes']
        mobile = request.POST['mobile']
        mobile2 = request.POST['mobile2']
        relativeName = request.POST['relativeName']
        address  = request.POST['location']
        print(doctor_time)
        print(doctor_notes)
        status = request.POST['status']
        doctor = Doctor.objects.get(name=doctor)
        print(doctor)
        patient.phone_num = mobile
        patient.patient_relative_contact = mobile2
        patient.patient_relative_name = relativeName
        patient.address = address
        patient.doctor = doctor
        patient.doctors_visiting_time = doctor_time
        patient.doctors_notes = doctor_notes
        print(patient.doctors_visiting_time)
        print(patient.doctors_notes)
        patient.status = status
        patient.save()
    context = {
        'patient': patient
    }
    return render(request, 'main/patient.html', context)


def patient_list(request):
    patients = Patient.objects.all()

    # filtering
    myFilter = PatientFilter(request.GET, queryset=patients)

    patients = myFilter.qs
    context = {
        'patients': patients,
        'myFilter': myFilter
    }

    return render(request, 'main/patient_list.html', context)

'''
def autocomplete(request):
    if patient in request.GET:
        name = Patient.objects.filter(name__icontains=request.GET.get(patient))
        name = ['js', 'python']
        
        names = list()
        names.append('Shyren')
        print(names)
        for patient_name in name:
            names.append(patient_name.name)
        return JsonResponse(names, safe=False)
    return render (request, 'main/patient_list.html')
'''

def autosuggest(request):
    query_original = request.GET.get('term')
    queryset = Patient.objects.filter(name__icontains=query_original)
    mylist = []
    mylist += [x.name for x in queryset]
    return JsonResponse(mylist, safe=False)

def autodoctor(request):
    query_original = request.GET.get('term')
    queryset = Doctor.objects.filter(name__icontains=query_original)
    mylist = []
    mylist += [x.name for x in queryset]
    return JsonResponse(mylist, safe=False)

def info(request):
    return render(request, "main/info.html")

def stats(request):
    return render(request, "main/stats.html")

def contact(request):
    return render(request, "main/contact.html")

def location(request):
    return render(request, "main/location.html")

def doctors(request):
    return render(request, "main/doctors.html")

def aboutus(request):
    return render(request, "main/aboutus.html")

import pdfkit

class InvoiceListView(View):
    def get(self, *args, **kwargs):
        invoices = Invoice.objects.all()
        context = {
            "invoices":invoices,
        }

        return render(self.request, 'main/invoice-list.html', context)
    
    def post(self, request):        
        # import pdb;pdb.set_trace()
        invoice_ids = request.POST.getlist("invoice_id")
        invoice_ids = list(map(int, invoice_ids))

        update_status_for_invoices = int(request.POST['status'])
        invoices = Invoice.objects.filter(id__in=invoice_ids)
        # import pdb;pdb.set_trace()
        if update_status_for_invoices == 0:
            invoices.update(status=False)
        else:
            invoices.update(status=True)

        return redirect('invoice:invoice-list')

def createInvoice(request):
    """
    Invoice Generator page it will have Functionality to create new invoices, 
    this will be protected view, only admin has the authority to read and make
    changes here.
    """

    heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = LineItemFormset(request.GET or None)
        form = InvoiceForm(request.GET or None)
    elif request.method == 'POST':
        formset = LineItemFormset(request.POST)
        form = InvoiceForm(request.POST)
        
        if form.is_valid():
            invoice = Invoice.objects.create(customer=form.data["customer"],
                    customer_email=form.data["customer_email"],
                    billing_address = form.data["billing_address"],
                    date=form.data["date"],
                    due_date=form.data["due_date"], 
                    message=form.data["message"],
                    )
            # invoice.save()
            
        if formset.is_valid():
            # import pdb;pdb.set_trace()
            # extract name and other data from each form and save
            total = 0
            for form in formset:
                service = form.cleaned_data.get('service')
                description = form.cleaned_data.get('description')
                quantity = form.cleaned_data.get('quantity')
                rate = form.cleaned_data.get('rate')
                if service and description and quantity and rate:
                    amount = float(rate)*float(quantity)
                    total += amount
                    LineItem(customer=invoice,
                            service=service,
                            description=description,
                            quantity=quantity,
                            rate=rate,
                            amount=amount).save()
            invoice.total_amount = total
            invoice.save()
            try:
                generate_PDF(request, id=invoice.id)
            except Exception as e:
                print(f"********{e}********")
            return redirect('/')
    context = {
        "title" : "Invoice Generator",
        "formset": formset,
        "form": form,
    }
    return render(request, 'main/invoice-create.html', context)


def view_PDF(request, id=None):
    invoice = get_object_or_404(Invoice, id=id)
    lineitem = invoice.lineitem_set.all()

    context = {
        "company": {
            "name": "BioFarma Services",
            "address" :"67542 Jeru, Chatsworth, CA 92145, US",
            "phone": "(818) XXX XXXX",
            "email": "contact@farmaservice.com",
        },
        "invoice_id": invoice.id,
        "invoice_total": invoice.total_amount,
        "customer": invoice.customer,
        "customer_email": invoice.customer_email,
        "date": invoice.date,
        "due_date": invoice.due_date,
        "billing_address": invoice.billing_address,
        "message": invoice.message,
        "lineitem": lineitem,

    }
    return render(request, 'main/pdf_template.html', context)

def generate_PDF(request, id):
    # Use False instead of output path to save pdf to a variable
    pdf = pdfkit.from_url(request.build_absolute_uri(reverse('invoice:invoice-detail', args=[id])), False)
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response


def change_status(request):
    return redirect('invoice:invoice-list')

def view_404(request,  *args, **kwargs):

    return redirect('invoice:invoice-list')