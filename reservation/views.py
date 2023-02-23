from django.shortcuts import render, redirect
from .models import *
from django.db.models import Sum, Count


def home(request):
    if not request.session.get('email'):
        request.session['email'] = ''
    rooms = [
        Room.objects.filter(title='Single Room')[:1][0],
        Room.objects.filter(title='Double Suite')[:1][0],
        Room.objects.filter(title='Deluxe Room')[:1][0]
    ]
    return render(request, 'hotel/index.html', {'rooms': rooms})


def register(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        guest = Guest.objects.filter(email=email)
        if guest:
            request.session['msg'] = "Email already exist! Kindly login."
            return redirect('/login')
        else:
            newguest = Guest.objects.create(firstname=fname,
                                            lastname=lname,
                                            email=email,
                                            phone=phone,
                                            password=password)
            newguest.save()
            request.session['msg'] = "Congrats! Guest account for " + \
                fname + " " + lname + " has been created. Please login."
            return redirect('/login')
    return render(request, 'hotel/register.html')


def login(request):
    email = request.session['email']
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        guests = Guest.objects.all()
        for guest in guests:
            if guest.email == email:
                if guest.password == password:
                    request.session['guest_id'] = guest.id
                    request.session['email'] = guest.email
                    request.session['isadmin'] = guest.is_admin
                    request.session['msg'] = "Guest " + guest.firstname + \
                        " " + guest.lastname + " logged in."
                    stat = LoginStat.objects.create()
                    stat.save()
                    return redirect('/')
                else:
                    request.session['msg'] = "Wrong password!"
                break
        else:
            request.session['msg'] = "Guest does not exist!"
    return render(request, 'hotel/login.html')


def logout(request):
    email = request.session['email']
    if email == '':
        request.session['msg'] = "No one has logged in!"
    else:
        request.session['msg'] = "Guest logged out."
        request.session['email'] = ''
        request.session['isadmin'] = False
    return redirect('/')


def rooms(request):
    return render(request, 'hotel/rooms.html', {'rooms': Room.objects.all().order_by('room_no')})


def each_room(request, r_no):
    room = Room.objects.get(room_no=r_no)
    rooms_matched = Room.objects.filter(title=room.title)
    context = {
        'room': room,
        'rooms_matched': rooms_matched
    }
    if request.method == 'POST':
        f_room_no = request.POST.get('f_room_no')
        f_start_date = request.POST.get('f_start_date')
        f_end_date = request.POST.get('f_end_date')
        guest = Guest.objects.get(email=request.session.get('email'))
        room = Room.objects.get(room_no=f_room_no)
        room.is_reserved = True
        room.save()
        newres = Reservation.objects.create(guest=guest,
                                            room=room,
                                            bill=room.price,
                                            start_date=f_start_date,
                                            end_date=f_end_date)
        newres.save()
        request.session['msg'] = "Congrats! Room no. " + f_room_no + " booked."
    return render(request, 'hotel/each-room.html', context)


def booking(request):
    return render(request, 'hotel/booking.html')


def dashboard(request):
    rooms = Room.objects.all().order_by('-date')
    services = Service.objects.all()
    payments1 = Payment.objects.filter(method='Mastercard').count()
    payments2 = Payment.objects.filter(method='Visa').count()

    context = {
        'rooms': rooms,
        'services': services,
        'is_form': False,
        'payments1': payments1,
        'payments2': payments2,
    }

    if request.method == 'POST':
        s_id = request.POST.get('room_service')
        if s_id != 'all':
            service = Service.objects.get(id=s_id)
            context['electricity__sum'] = service.electricity
            context['gas__sum'] = service.gas
            context['internet__sum'] = service.internet
            context['is_form'] = True
            context['selected_service'] = service
            return render(request, 'admin/dashboard.html', context)

    expenses = [
        Service.objects.aggregate(Sum('electricity')),
        Service.objects.aggregate(Sum('gas')),
        Service.objects.aggregate(Sum('internet')),
    ]
    for i in expenses:
        context.update(i)

    return render(request, 'admin/dashboard.html', context)


def reservations(request):
    stats = Reservation.objects.all()
    reservation_counter = {}
    for stat in stats:
        reservation_counter[stat.room.title] = 0
    for stat in stats:
        reservation_counter[stat.room.title] += 1
    labels = list(reservation_counter.keys())
    data = list(reservation_counter.values())
    context = {
        'labels': labels,
        'data': data
    }
    return render(request, 'admin/reservations.html', context)


def logins(request):
    stats = LoginStat.objects.all()
    login_counter = {}
    for stat in stats:
        login_counter[str(stat.date)] = 0
    for stat in stats:
        login_counter[str(stat.date)] += 1
    labels = list(login_counter.keys())
    data = list(login_counter.values())
    context = {
        'labels': labels,
        'data': data
    }
    return render(request, 'admin/logins.html', context)
