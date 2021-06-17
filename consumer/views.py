from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from consumer.models import Consumer, Provider, Display, History
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import ConsumerForm, UserForm, ProviderForm, InfoForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

# Create your views here.
def index(request):
    return render(request, 'index.html', {'title': 'index'})

def dashboard(request):
    return render(request, 'dashboard.html', {'title': 'dashboard'})

def register_consumer(request):
    if request.method == 'POST':
        form = ConsumerForm(request.POST or None)
        form1 = UserForm(request.POST or None)
        if form1.is_valid():
            username = form1.cleaned_data.get('username')
            firstname = form1.cleaned_data.get('first_name')
            lastname = form1.cleaned_data.get('last_name')
            password = form1.cleaned_data.get('password')
            email = form1.cleaned_data.get('email')
            usr = User.objects.create_user(username, email, password)
            if form.is_valid():
                f = form.save(commit=False)
                f.user = usr
                f.save()
                """
                htmly = get_template('email.html')
                d = {'username': username}
                subject, from_email, to = 'welcome', 'rishu5727@gmail.com', email
                html_content = htmly.render(d)
                msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                messages.success(request, f'Your account has been created ! You are now able to log in')
                """
                return redirect('login')
    else:
        form1 = UserForm()
        form = ConsumerForm()
        return render(request, 'register_con.html', {'form': form, 'form1': form1, 'title': 'register here'})


def register_provider(request):
    if request.method == 'POST':
        form = ProviderForm(request.POST or None)
        form1 = UserForm(request.POST or None)
        if form1.is_valid():
            username = form1.cleaned_data.get('username')
            firstname = form1.cleaned_data.get('first_name')
            lastname = form1.cleaned_data.get('last_name')
            password = form1.cleaned_data.get('password')
            email = form1.cleaned_data.get('email')
            usr = User.objects.create_user(username, email, password)
            if form.is_valid():
                f = form.save(commit=False)
                f.user = usr
                f.save()
                htmly = get_template('email.html')
                d = {'username': username}
                subject, from_email, to = 'welcome', 'rishu5727@gmail.com', email
                html_content = htmly.render(d)
                msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                messages.success(request, f'Your account has been created ! You are now able to log in')
                return redirect('login')
    else:
        form1 = UserForm()
        form = ProviderForm()
        return render(request, 'register_con.html', {'form': form, 'form1': form1, 'title': 'register here'})



def login(request):
    if request.method == 'POST':
        usrname = request.POST['username']
        psswrd = request.POST['password']
        user = authenticate(request, username=usrname, password=psswrd)
        if user is not None:
            form = auth_login(request, user)
            if Provider.objects.filter(user=user):
                return render(request, 'dashboard_provider.html', {'msg': f" Welcome as Food Provider !!", 'act': "" , 'title': 'dashboard'})
            else:
                providers = []
                for each in Display.objects.filter():
                    providers.append(each)
                    print("putting")
                print(providers)
                return render(request, 'dashboard.html', {'msg': f" Welcome as Food Consumer!!", 'list': providers ,'title': 'dashboard'})
        else:
            messages.info(request, f'account done not exist plz sign in again!')
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'title': 'login'})

def active(request):
    if Provider.objects.filter(user=request.user):
        prov = Provider.objects.get(user=request.user)
        if prov.is_active:
            prov.is_active = False
            prov.save()
            print("inactivated")
            d = Display.objects.filter(provider=prov).delete()
            print("deleted")
            return render(request, 'dashboard_provider.html', {'msg': f" Welcome as Food Provider !!", 'act': f" Inactivated Successfully! ", 'title': 'dashboard'})
        else:
            prov.is_active = True
            prov.save()
            print("activated")
            return render(request, 'info.html', {'title': 'info'})
    else:
        messages.info(request, f'account done not exist')

def information(request):
    if request.method == 'POST':
        print("coming")
        count = request.POST['count']
        time = request.POST['time']
        p = Provider.objects.get(user=request.user)
        d = Display.objects.create(provider=p, food_available_count=count, food_best_till=time)
        print("created")
        d.save()
        return render(request, 'dashboard_provider.html', {'msg': f" Welcome as Food Provider !!", 'act': f" Activated Successfully! ", 'title': 'dashboard'})
    else:
        return render(request, 'info.html', {'title': 'info'})

def transaction(request, my_id):
    if request.method == 'POST':
        if Display.objects.filter(id=my_id):
            dis = Display.objects.get(id=my_id)
            prov = dis.provider
            total_available = int(dis.food_available_count)
            order = request.POST['order']
            order = int(order)
            phone = request.POST['phone']
            if order <= total_available:
                cons = Consumer.objects.get(user=request.user)
                h = History.objects.create(provider=prov, consumer=cons, order=order, consumer_contact_number=phone)
                h.save()
                dis.food_available_count = total_available - order
                dis.save()
                if dis.food_available_count <= 0:
                    prov.is_active = False
                    prov.save()
                    d = Display.objects.filter(id=my_id).delete()
                    print("deleted there")
                providers = []
                for each in Display.objects.filter():
                    providers.append(each)
                    print("putting")
                return render(request, 'dashboard.html',
                              {'msg': f" Transaction successful, check order history!!", 'list': providers, 'title': 'dashboard'})
            else:
                providers = []
                for each in Display.objects.filter():
                    providers.append(each)
                    print("putting")
                return render(request, 'dashboard.html', {'msg': f" Requirement is more than availability, Sorry!", 'list': providers, 'title': 'dashboard'})
        else:
            print("account done not exist")
            return redirect('logout')
    else:
        return render(request, 'transaction.html', {'id': my_id, 'title': 'transaction'})


def history(request):
    if Consumer.objects.filter(user=request.user):
        cons = Consumer.objects.get(user=request.user)
        his = []
        for each in History.objects.filter(consumer=cons):
            his.append(each)
            print("putting there")
        return render(request, 'history.html', {'list': his, 'title': 'history'})
    else:
        prov = Provider.objects.get(user=request.user)
        his = []
        for each in History.objects.filter(provider=prov):
            his.append(each)
            print("putting there")
        return render(request, 'history.html', {'list': his, 'title': 'history'})