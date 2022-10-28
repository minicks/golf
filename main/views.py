from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from main.forms import UserForm
import calendar
import json
from .models import Month, Day
from account.models import *


def index(request):
    yearCalender = calendar.HTMLCalendar().formatyear(2021)
    context = {
        'YC': yearCalender,
    }
    return render(request, 'main.html', context)


def viewSeat(request):
    month_list = Month.objects.all()
    dateDay = request.POST.get('dateDay')
    selMonth = request.POST.get('selMonth')
    resSeat = 0
    for ml in month_list:
        if ml.month == selMonth:
            for dl in ml.day_set.all():
                if dl.day == dateDay:
                    resSeat = dl.remain_seat
    context = {
        'resSeat': resSeat,
    }
    return HttpResponse(json.dumps(context), content_type="application/json")


def checkSeat(request):
    month_list = Month.objects.all()
    user = request.user
    reqDay = request.POST.get('reqDay')
    conCheck = request.POST.get('conCheck')
    selMonth = request.POST.get('selMonth')
    print(reqDay, conCheck, selMonth)

    if conCheck == "purchase":
        for ml in month_list:
            if ml.month == selMonth:
                for dl in ml.day_set.all():
                    if dl.day == reqDay:
                        dl.remain_seat -= 1
                        dl.save()
                        user.profile.book_day.add(dl)
                        print(user.profile.book_day.filter(id=dl.id))
                        user.save
                        resSeat = dl.remain_seat
    elif conCheck == "cancel":
        for ml in month_list:
            if ml.month == selMonth:
                for dl in ml.day_set.all():
                    if dl.day == reqDay:
                        dl.remain_seat += 1
                        dl.save()
                        resSeat = dl.remain_seat
    context = {
        'resSeat': resSeat,
    }
    return HttpResponse(json.dumps(context), content_type="application/json")


def cancelSeat(request):
    month_list = Month.objects.all()
    reqDay = request.POST.get('reqDay')
    selMonth = request.POST.get('selMonth')

    for ml in month_list:
        if ml.month == selMonth:
            for dl in ml.day_set.all():
                if dl.day == reqDay:
                    dayId = dl.id
                    request.user.profile.book_day.filter(id=dayId).delete()
                    # print(request.user.profile.book_day.filter(id=dl.id))
                    dl.remain_seat += 1
                    dl.save()
                    resSeat = dl.remain_seat
    context = {
        'resSeat': resSeat,
    }
    return HttpResponse(json.dumps(context), content_type="application/json")


dayMax = 32


def saveData(request):
    global dayMax
    month_list = Month.objects.all()
    for ml in month_list:
        if ml.month == 'May':
            dayMax = 32
        elif ml.month == 'June':
            dayMax = 31
        elif ml.month == 'July':
            dayMax = 32
        elif ml.month == 'August':
            dayMax = 32
        for i in range(1, dayMax):
            varDay = Day()
            varDay.day = i
            varDay.remain_seat = 4
            varDay.f_month = ml
            varDay.save()
    return render(request, 'main.html')


# REGISTER
def register(request):
    """ 계정생성 """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main:main')
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})


def data(request):
    return render(request, 'lottie.html')
