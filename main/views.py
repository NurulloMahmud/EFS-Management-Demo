from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Message, Used, Efs, StatusChange


User = get_user_model()



class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_active:
            login(request, user)
            return redirect('home')
        return render(request, 'login.html')


@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    

@method_decorator(login_required, name='dispatch')
class HomeView(ListView):
    model = Message
    template_name = 'index.html'
    context_object_name = 'messages' # display messages from management


@method_decorator(login_required, name='dispatch')
class AvailableCodesView(View):
    def get(self, request):
        # get the number of available efs codes for each amount
        fifty = Efs.objects.filter(amount=50, status='available').values('amount').count()
        one_hundered = Efs.objects.filter(amount=100, status='available').values('amount').count()
        two_hundered = Efs.objects.filter(amount=200, status='available').values('amount').count()
        three_hundered = Efs.objects.filter(amount=300, status='available').values('amount').count()
        four_hundered = Efs.objects.filter(amount=400, status='available').values('amount').count()
        fife_hundered = Efs.objects.filter(amount=500, status='available').values('amount').count()
        six_hundered = Efs.objects.filter(amount=600, status='available').values('amount').count()
        seven_hundered = Efs.objects.filter(amount=700, status='available').values('amount').count()
        eight_hundered = Efs.objects.filter(amount=800, status='available').values('amount').count()

        counts = {50: fifty, 
                  100: one_hundered, 
                  200: two_hundered, 
                  300: three_hundered, 
                  400: four_hundered, 
                  500: fife_hundered, 
                  600: six_hundered, 
                  700: seven_hundered, 
                  800: eight_hundered}

        context = {
            "counts": counts
        }

        return render(request, 'available.html', context)


# display efs codes that are already used/given/paid/voided
@method_decorator(login_required, name='dispatch')
class UsedView(ListView):
    model = Used
    template_name = 'used.html'
    context_object_name = 'used'

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().order_by('-date')


# display all activities done on each money code
@method_decorator(login_required, name='dispatch')
class ActivityLogView(ListView):
    model = StatusChange
    template_name = 'activity.html'
    context_object_name = 'activities'


# change the money code status to paid
@method_decorator(login_required, name='dispatch')
class PaidStatusView(View):
    def get(self, request, money_code):
        efs_code = Efs.objects.get(code=money_code)
        old_status = efs_code.status
        
        StatusChange.objects.create(
            efs=efs_code, 
            user=request.user,
            old_status=old_status,
            new_status='paid'
        )

        efs_code.status = 'paid'
        efs_code.save()


        return redirect('used')


# change the money code status to voided
@method_decorator(login_required, name='dispatch')
class VoidedStatusView(View):
    def get(self, request, money_code):
        efs_code = Efs.objects.get(code=money_code)
        old_status = efs_code.status

        StatusChange.objects.create(
            efs=efs_code, 
            user=request.user,
            old_status=old_status,
            new_status='voided'
        )

        efs_code.status = 'voided'
        efs_code.save()
        return redirect('used')
    

# display the form to fill after efs money code is given
@method_decorator(login_required, name='dispatch')
class Form(View):
    def get(self, request, amount):
        user = request.user
        efs = Efs.objects.filter(amount=amount, status='available').first()
        efs_code = efs.code
        reference = Efs.objects.get(code=efs_code).reference  # Use dot notation here
        efs.status='given'
        efs.save()
        
        # record the money code in used for accounting team to review
        new_used = Used.objects.create(efs=efs, given_by=user, date=timezone.now())
        new_used.save()

        # record the activity for management team
        StatusChange.objects.create(
            efs=efs, 
            user=user, 
            old_status='available',
            new_status='given',
            date=timezone.now()
        )

        context = {
            'code': efs_code,
            'reference': reference,
            'amount': amount
        }

        return render(request, 'forms.html', context)
    
    def post(self, request, amount):
        # get the efs code given
        efs_code = request.POST.get('code')
        given_amount = request.POST.get('amount')
        reason = request.POST.get('reason')
        expense = request.POST.get('expense')
        fee = request.POST.get('fee') == 'on'
        efs_instance = Efs.objects.get(code=efs_code)

        # save the maintenance team's notes
        used_object = Used.objects.filter(efs=efs_instance).first()
        used_object.given_amount = given_amount
        used_object.reason = reason
        used_object.expense = expense
        used_object.fee = fee
        used_object.save()

        return redirect('home')
    

@method_decorator(login_required, name='dispatch')
class AddEfs(View):
    def get(self, request):
        return render(request, 'add_code.html')
    
    def post(self, request):
        code = request.POST.get('code')
        reference = request.POST.get('reference')
        amount = request.POST.get('amount')
        status = 'available'

        Efs.objects.create(code=code, reference=reference, amount=amount, status=status)
        
        return redirect('/')


@method_decorator(login_required, name='dispatch')
class StaffView(ListView):
    model = User
    template_name = 'staff.html'
    context_object_name = 'staff'

    def get_queryset(self):
        return super().get_queryset().order_by('-is_active', '-date_joined')


@method_decorator(login_required, name='dispatch')
class ActivateStaffView(View):
    def get(self, request, pk):
        staff = User.objects.get(id=pk)
        if staff:
            staff.active=True
            staff.save()
        return redirect('staff')


@method_decorator(login_required, name='dispatch')
class DeactivateStaffView(View):
    def get(self, request, pk):
        staff = User.objects.get(id=pk)
        if staff:
            staff.active=False
            staff.save()
        return redirect('staff')


@method_decorator(login_required, name='dispatch')
class AddMessageView(View):
    def get(self, request):
        return render(request, 'add_message.html')
    def post(self, request):
        msg = request.POST.get('message')
        Message.objects.create(msg=msg, user=request.user)
        return redirect('home')


@method_decorator(login_required, name='dispatch')
class EditNoteView(View):
    def get(self, request, money_code):
        return render(request, 'edit_note.html')
    
    def post(self, request, money_code):
        # get the efs code given
        given_amount = request.POST.get('amount')
        reason = request.POST.get('reason')
        expense = request.POST.get('expense')
        fee = request.POST.get('fee') == 'on'
        efs_instance = Efs.objects.get(code=money_code)

        # save the maintenance team's notes
        used_object = Used.objects.filter(efs=efs_instance).first()
        used_object.given_amount = given_amount
        used_object.reason = reason
        used_object.expense = expense
        used_object.fee = fee
        used_object.save()

        return redirect('used')