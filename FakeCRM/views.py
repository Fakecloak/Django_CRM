from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import *
from .models import *

# Create your views here.

def home(request):
    records= Record.objects.all()
    #if user logged in
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        #authenticate
        user=authenticate(username=username,password=password)
        if user is not None: # if there is a user on db already.
            login(request, user)
            messages.success(request, "User logged in")
            return redirect('home')
        else:
            messages.error(request, "invalid username or password")
            return redirect('home')
    else:
        return render (request, 'FakeCRM/index.html',{'records':records})

def logout_user(request):
    logout(request)
    messages.success(request, "User logged out")
    return redirect('home')

def register_user(request):
    #if user posting
    if request.method == 'POST':
        form= SignUpForm(request.POST)
        #check form is valid and save
        if form.is_valid():
            form.save()
            # Authenticate and login user
            username= form.cleaned_data['username']
            password= form.cleaned_data['password1']
            user= authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,"successfully registered")
            return redirect('home')
    else:
         form=SignUpForm()
         return render(request, 'FakeCRM/register.html',{'form' : form})  
       
    return render(request, 'FakeCRM/register.html',{'form' : form})

def record_view(request,id):
    if request.user.is_authenticated:
        record_view  = Record.objects.get(id=id)
        return render(request, 'FakeCRM/record.html',{'record_view' : record_view})
    else:
        messages.success(request,"Please login to view the records")
        return redirect('home')
    
def delete_record(request,id):
    if request.user.is_authenticated:
        delete_record = Record.objects.get(id=id)
        delete_record.delete()
        messages.success(request,"Successfully deleted")
        return redirect('home')
    else:
        messages.success(request,"Please login to delete the records")
        return redirect('home')


def add_record(request):
    form=AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method=="POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Record Added successfully!")
                return redirect('home')
        return render ( request, 'FakeCRM/AddRecord.html',{'form':form})
    else:
        messages.success(request,"Please login to Add Records")
        return redirect("home")
    
def update_record(request,id):
	if request.user.is_authenticated:
		record_view = Record.objects.get(id=id)
		form = AddRecordForm(request.POST or None, instance = record_view)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'FakeCRM/UpdateRecord.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')

