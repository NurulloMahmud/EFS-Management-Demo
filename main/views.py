from typing import Any
from django.http import HttpResponseRedirect
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Department, Message, Used, Efs, StatusChange, UserDepartment
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm

        

User = get_user_model()

class BaseView(View):
    def get(self, request):
        user = request.user
        messages = Message.objects.all()

        context = {
            'messages': messages,
        }
        return render(request, 'base.html', context)


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # replace 'home' with the name of the view you want to redirect to after login
        return render(request, 'login.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    


@method_decorator(login_required, name='dispatch')
class AvailableCodesView(View):
    def get(self, request):
        if request.department in [1, 2]:

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
        return render(request, '404.html')


# display efs codes that are already used/given/paid/voided
@method_decorator(login_required, name='dispatch')
class UsedView(ListView):
    model = Used
    template_name = 'used.html'
    context_object_name = 'used'

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(efs__status='given').order_by('-date')


# display all activities done on each money code
@method_decorator(login_required, name='dispatch')
class ActivityLogView(ListView):
    model = StatusChange
    template_name = 'activity.html'
    context_object_name = 'activities'

    def dispatch(self, request, *args, **kwargs):
        if request.department == 1:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('not-found')


# change the money code status to paid
@method_decorator(login_required, name='dispatch')
class PaidStatusView(View):
    def get(self, request, money_code):
        if request.department in [1, 3]:
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


            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect('not-found')


# change the money code status to voided
@method_decorator(login_required, name='dispatch')
class VoidedStatusRequestView(View):
    def get(self, request, money_code):
        print("in view")
        if request.department in [1, 3]:
            print("in if statement")
            efs_code = Efs.objects.get(code=money_code)
            old_status = efs_code.status
            print(efs_code.status)
            print(old_status)

            efs_code.status = 'pending' if request.department == 3 else 'voided'
            print(efs_code.status)
            efs_code.save()

            StatusChange.objects.create(
                efs=efs_code, 
                user=request.user,
                old_status=old_status,
                new_status=efs_code.status
            )
            print("status change completed")

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect('not-found')


@method_decorator(login_required, name='dispatch')
class VoidRequestsView(View):
    def get(self, request):
        if request.department == 1:
            requests = Used.objects.filter(efs__status='pending')
            for req in requests:
                req.difference = req.efs.amount - req.given_amount
            context = {
                'requests': requests
            }
            return render(request, 'void_requests.html', context)

    def post(self, request):
        pass


# display the form to fill after efs money code is given
@method_decorator(login_required, name='dispatch')
class Form(View):
    def get(self, request, amount):
        if request.department in [1, 2]:
            return render(request, 'forms.html', {"amount": amount})
        return render(request, '404.html')
    
    def post(self, request, amount):
        if request.department in [1, 2]:
            # get the form data
            given_amount = request.POST.get('amount')
            reason = request.POST.get('reason')
            expense = request.POST.get('expense')
            fee = request.POST.get('fee') == 'on'
            given_amount = amount if not given_amount else given_amount


            if reason is not None and expense is not None:

                # get the efs code
                efs = Efs.objects.filter(amount=amount, status='available').first()
                efs_code = efs.code
                reference = efs.reference
                efs.status='given'
                efs.save()

                # record the data in used model
                new_used = Used.objects.create(efs=efs, given_by=request.user, given_amount=given_amount, reason=reason, expense=expense, fee=fee)
                new_used.save()

                # record the activity for management team
                StatusChange.objects.create(
                    efs=efs, 
                    user=request.user, 
                    old_status='available',
                    new_status='given',
                    date=timezone.now()
                )

                context = {
                    'code': efs_code,
                    'reference': reference,
                    'amount': given_amount
                }

                return render(request, 'efscode.html', context)
            
            else:
                return redirect('form')
        return render(request, '404.html')

    

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
    model = UserDepartment
    template_name = 'staff.html'
    context_object_name = 'staff'

    def dispatch(self, request, *args, **kwargs):
        if request.department == 1:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('not-found')
    
    def get_queryset(self):
        # Get the queryset and order it by 'is_active' field in descending order
        queryset = super().get_queryset()
        return queryset.order_by('-user__is_active')


@method_decorator(login_required, name='dispatch')
class AddStaff(View):
    def get(self, request):
        if request.department == 1:
            return render(request, 'add_staff.html')
        return render(request, '404.html')
    def post(self, request):
        if request.department == 1:
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            department_id = request.POST.get('department')

            if password1==password2 and not User.objects.filter(username=username).exists():
                department = Department.objects.get(pk=department_id)
                user = User.objects.create_user(username=username, password=password1, first_name=first_name, last_name=last_name)
                user_department = UserDepartment.objects.create(user=user, department=department)
                user_department.save()
                return redirect('staff')
            return render(request, 'already_exists.html')


@method_decorator(login_required, name='dispatch')
class ActivateStaffView(View):
    def get(self, request, pk):
        if request.department == 1:
            staff = User.objects.get(pk=pk)
            if staff:
                staff.is_active=True
                staff.save()
            return redirect('staff')
        else:
            return render(request, '404.html')


@method_decorator(login_required, name='dispatch')
class DeactivateStaffView(View):
    def get(self, request, pk):
        if request.department == 1:
            staff = User.objects.get(pk=pk)

            if staff:
                staff.is_active=False
                staff.save()
            return redirect('staff')
        else:
            return render(request, '404.html')


@method_decorator(login_required, name='dispatch')
class AddMessageView(View):
    def get(self, request):
        return render(request, 'add_message.html')
    def post(self, request):
        msg = request.POST.get('message')
        Message.objects.create(message=msg, user=request.user)
        return redirect('home')


@method_decorator(login_required, name='dispatch')
class EditNoteView(View):    
    def get(self, request, money_code):
        if request.department in [1, 2]:
            efs_instance = Efs.objects.get(code=money_code)
            used_instance = Used.objects.get(efs=efs_instance)
            context = {
                'given_amount': used_instance.given_amount,
                'reason': used_instance.reason,
                'expense': used_instance.expense,
                'fee': used_instance.fee,
                'amount': efs_instance.amount
            }
            return render(request, 'edit_note.html', context)
        return render(request, '404.html')
    
    def post(self, request, money_code):
        # get the efs code given
        given_amount = request.POST.get('amount')
        reason = request.POST.get('reason')
        expense = request.POST.get('expense')
        fee = request.POST.get('fee') == 'on'
        efs_instance = Efs.objects.get(code=money_code)

        # save the maintenance team's notes
        used_object = Used.objects.filter(efs=efs_instance).first()
        used_object.given_amount = given_amount if given_amount else used_object.given_amount
        used_object.reason = reason if reason else used_object.reason
        used_object.expense = expense if expense else used_object.expense
        used_object.fee = fee
        used_object.save()

        return redirect('used')
    

class PageNotFoundView(View):
    def get(self, request):
        return render(request, '404.html')


# working with resolved efs data
@method_decorator(login_required, name='dispatch')
class VoidedView(View):
    def get(self, request):
        if request.department in [1, 3]:
            money_codes = Used.objects.filter(efs__status='voided').order_by('-date')
            context = {
                'money_codes': money_codes
            }
            return render(request, 'voided.html', context)
        return render(request, '404.html')
    

@method_decorator(login_required, name='dispatch')
class PaidView(View):
    def get(self, request):
        if request.department in [1, 3]:
            money_codes = Used.objects.filter(efs__status='paid').order_by('-date')
            context = {
                'money_codes': money_codes
            }
            return render(request, 'voided.html', context)
        return render(request, '404.html')
    

@method_decorator(login_required, name='dispatch')
class UpdateNoteView(UpdateView):
    model = Message
    template_name = 'update_note.html'
    fields = ('message',)

    def get_success_url(self):
        return reverse_lazy('home')


@method_decorator(login_required, name='dispatch')
class DeleteNoteView(DeleteView):
    model = Message
    template_name = 'delete_note.html'
    success_url = reverse_lazy('home')


