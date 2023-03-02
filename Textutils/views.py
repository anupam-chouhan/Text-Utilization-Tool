from django.http import HttpResponse
from django.shortcuts import render,redirect
from datetime import datetime
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate,login

def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request,'index.html')

def aboutus(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request,'about.html')

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        
        user = authenticate(username=username,password=password)
        
        if user is not None:
            login(request,user)
            messages.success(request,f"Hello, {request.user}! You are Successfully logged in |")
            return redirect("/")
        else:
            messages.success(request, 'Wrong Username / Password !')
            return render(request, 'login.html')
    return render(request, 'login.html')

def analyze(request):
    if request.user.is_anonymous:
        return redirect("/login")
    
    djtext = request.POST.get('text','default')

    removepunc = request.POST.get('removepunc','off')
    charcount = request.POST.get('charcount','off')
    fullcaps = request.POST.get('fullcaps','off')
    newlineremover = request.POST.get('newlineremover','off')
    extraspaceremover = request.POST.get('extraspaceremover','off')

    if removepunc == 'on':
        punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_'''
        analyzed = ""
        for char in djtext:
            if char not in punctuation:
                analyzed = analyzed + char
        params = {'purpose':'Removed Punctuations','analyzed_text':analyzed}
        djtext = analyzed

    if charcount == "on":
        analyzed = ""
        for char in djtext:
            analyzed = analyzed + char
        params = {'purpose':'character counting','analyzed_text':f"Total Character in your text = {analyzed} : {len(analyzed)}"}
        djtext = analyzed

    if fullcaps=="on":
        analyzed = ""
        for char in djtext:
            analyzed = analyzed+char.upper()
        params = {'purpose':'changed to uppercase','analyzed_text':analyzed}
        djtext = analyzed

    if newlineremover == "on":
        analyzed = ""
        for char in djtext:
            if char!="\n" and char!="\r":
                analyzed = analyzed+char
        params = {'purpose':'removed new lines','analyzed_text':analyzed}
        djtext = analyzed

    if extraspaceremover == "on":
        analyzed = "" 
        for index, char in enumerate(djtext):
            if djtext[index] == " " and djtext[index+1]==" ":
                pass
            else:
                analyzed = analyzed+char

        params = {'purpose':'removed extra spaces','analyzed_text':analyzed}
        djtext = analyzed
                
    if (removepunc !="on" and charcount !="on" and fullcaps !="on" and newlineremover !="on" and extraspaceremover !="on"):
        return HttpResponse("Error! Plz select atleast one option to analyze text!")
    return render(request,'analyze.html',params)


def contactus(request):
    if request.user.is_anonymous:
        return redirect("/login")
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        # date = request.POST.get('date')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent!')
    return render(request,'contact.html')


def logoutUser(request):
    if request.user.is_anonymous:
        messages.success(request, 'already logged out ! login again to continue...')  
        return redirect("/login")
    logout(request)
    messages.success(request, 'logged out successfully...')
    return redirect("/login")