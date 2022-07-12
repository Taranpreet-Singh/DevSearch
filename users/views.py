from email import message
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Skill, Message
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, ProfileForm, skillForm, MessageForm
from django.db.models import Q
from .utils import searchProfiles, paginationProfiles

def loginUser(request):
    page = 'login'

    # if the user is already logged in, dont show them the login page
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']
        # check if user even exists or not
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username doesnot exist')

        # if user exist check if the credentials are correct or not, that what authenticate does
        user = authenticate(request, username=username, password=password)
        # if credentials are correct login the user creating session in cookies and if database is there, in that too
        # login creates session for the user, so once logged in it doesnt have to login until session expires
        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, "Usename OR Password is incorrect")    
    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request, "User was logged out ")
    return redirect('login')


def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # so we dont want username to be case sensitive, so changing that issue
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "User account was created!")
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, "An error was occured during the registration")



    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def profiles(request):
    profiles, search_query = searchProfiles(request)
    results = 3
    custom_range, profiles = paginationProfiles(request, profiles, results)
    context = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)


# User CRUD
@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {'profile': profile,
               'skills': skills,
               'projects': projects
            }
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
             
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


# Skill CRUD
@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = skillForm()
    if request.method == "POST":
        form = skillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill was added Successfully!!!")
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = skillForm(instance=skill)
    if request.method == "POST":
        form = skillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill was updated Successfully!!!")
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill was deleted Successfully!!!")
        return redirect('account')
    
    return render(request, 'delete.html', context={'object': skill})


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:    
        message.is_read = True
        message.save()

    context = {'message': message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    form = MessageForm()
    recipient = Profile.objects.get(id=pk)

    # check if user is authenticated or not, can also do with is_authenticated but yeahh
    try:
        sender = request.user.profile
    except:
        sender = None
    
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            if sender:
                message.name = sender.name
                message.email = sender.email
            
            message.save()
            messages.success(request, "Your message was successfully dilivered!")
            return redirect('user-profile', pk=recipient.id)

    context = {'form': form, 'recipient': recipient}
    return render(request, 'users/message_form.html', context)
