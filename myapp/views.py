from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
from datetime import datetime
from .models import ProjectRoom,LabTask,LabFile,Feedback,Task
from django.contrib import messages
import string
from django.contrib.auth import logout
from django.template.loader import render_to_string
from django.utils.html import strip_tags
def login_view(request):
    return render(request,'home.html')
def teacher_login(request):
    # List of allowed emails
    allowed_emails = ['tareqshakib789@gmail.com',"u1904059@student.cuet.ac.bd","u1904039@student.cuet.ac.bd"]  # Add your allowed emails
    if request.method == 'POST':
        email = request.POST.get('email')
        if email in allowed_emails:
            # Generate OTP
            otp = str(random.randint(100000, 999999))
            # Send OTP to the user's email
            send_mail(
                'Login OTP',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            # Store the OTP in the session for verification
            request.session['otp'] = otp
            request.session['email'] = email

            return redirect('otp_verification')
        else:
            return HttpResponse('Unauthorized', status=401)
    return render(request, 'teacher_login.html')
def otp_verification_view(request):
    # Retrieve the stored email and OTP from the session
    email = request.session.get('email')
    stored_otp = request.session.get('otp')
    if request.method == 'POST':
        # Get the entered OTP
        entered_otp = request.POST.get('otp')
        # Verify the entered OTP
        if entered_otp == stored_otp:
            # Successful login, clear the session
            request.session.clear()
            return redirect('create_lab_task')
        else:
            return HttpResponse('Invalid OTP', status=401)
    return render(request, 'otp_verification.html')
def student_registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email=request.POST['email']
        user = User.objects.create_user(username=username, password=password,email=email)
        login(request, user)
        return redirect('room_list')  # redirect to profile page after registration
    return render(request,'student_reg.html')
def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('room_list')   # redirect to profile page after login
    return render(request, 'student_login.html')
@login_required
def create_room(request):
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        description = request.POST.get('description')
        # Generate a unique room ID
        room_id = generate_unique_room_id()
        # Get the current logged-in user as the team leader
        team_leader = request.user
        # Create the project room in the database
        room = ProjectRoom.objects.create(
            project_name=project_name,
            description=description,
            room_id=room_id,
            team_leader=team_leader
        )
        room.team_members.add(request.user)
        room.save()
        email=room.team_leader.email
        send_mail(
                'Room Id',
                f'Your Room Id is: {room_id}\nShare this Id with your team members',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        return redirect('room_details',id=room.id)  # Redirect to the student dashboard or any other desired page
    return render(request, 'create_room.html')
def generate_unique_room_id():
    # Generate a 6-digit random code
    room_id = ''.join(random.choices(string.digits, k=6))
    return room_id
def room_list(request):
    rooms = ProjectRoom.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})
def room_details(request,id):
    room =ProjectRoom.objects.get( id = id )
    team_members = room.team_members.all()
    team_leader = room.team_leader
    return render(request, 'room_details.html', {'room_name': room.project_name,'room_description':room.description,'team_members': team_members, 'team_leader': team_leader})
def enter_room(request,id):
    room=ProjectRoom.objects.get(id = id)
    if request.method == 'POST':
        entered_id=request.POST['roomId']
        # print(entered_id)
        # print(room.room_id)
        if entered_id == room.room_id:
           if request.user not in room.team_members.all():
                # Add the user as a team membere
                room.team_members.add(request.user)
                room.save()
           return redirect('room_details',id=room.id)
    return render(request,'enter_room.html')
# views.py
def create_lab_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline_str = request.POST.get('deadline')
        try:
            # Convert the deadline string to a datetime object
            deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
            
            # Create the lab task for the room
            lab_task = LabTask.objects.create(
                title=title,
                description=description,
                deadline=deadline,
            )
            rooms = ProjectRoom.objects.all()
            for room in rooms:
             subject = 'New Lab Task'
             context = {'title':title,'description':description, 'deadline': deadline}
             message = render_to_string('email.html', context)
             plain_message = strip_tags(message)
            #  m="u1904059@student.cuet.ac.bd"
             send_mail(subject, plain_message, 'taskflow.info@gmail.com', [room.team_leader.email], html_message=message)
            # Send email notification to room leader
            #  send_mail(
            #     'New Lab Task',
            #     f'Description: {lab_task.description}\nDeadline: {lab_task.deadline}',
            #     settings.EMAIL_HOST_USER,
            #     [m],
            #     fail_silently=False,
            #  )
            return redirect('teacher_lab_tasks')
        except ValueError:
            # Handle the case where the deadline string is not a valid datetime format
            error_message = 'Invalid deadline format. Please use the correct format.'
            return render(request, 'create_lab_task.html', {'error': error_message})

    return render(request, 'create_lab_task.html')
def lab_task(request):
    room = ProjectRoom.objects.filter(team_members=request.user).first()    
    lab_tasks = LabTask.objects.all()
    return render(request,'lab_tasks.html',{"lab_tasks":lab_tasks,'room':room})

def upload(request,id):
    lab_task = LabTask.objects.get(id=id)
    user_room = ProjectRoom.objects.filter(team_members=request.user).first()
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        lab_file = LabFile.objects.create(
            lab_task=lab_task,
            team=user_room,
            file=uploaded_file,
        )
        return redirect('lab_task')
    return render(request, 'upload.html',{'room':user_room})

# def lab_files(request):
#     lab_files = LabFile.objects.all()
#     return render(request, 'lab_files.html', {'lab_files': lab_files})

def teacher_lab_tasks(request):
    lab_tasks = LabTask.objects.all()
    return render(request, 'teacher_lab_tasks.html', {'lab_tasks': lab_tasks})

def lab_files(request, id):
    lab_task = LabTask.objects.get(id=id)
    lab_files = LabFile.objects.filter(lab_task=lab_task)
    return render(request, 'lab_files.html', {'lab_task': lab_task, 'lab_files': lab_files})
def feedback(request,id):
    lab_file = LabFile.objects.get(id=id)
    if request.method == 'POST':
        content = request.POST.get('feedback_content')
        feedback = Feedback.objects.create(
            lab_file=lab_file, # Assuming team leader is the student associated with the file
            content=content
        )
        feedback.save()
    return redirect('lab_files', id=lab_file.lab_task.id)
def lab_tasks_feed(request):
    room = ProjectRoom.objects.filter(team_members=request.user).first()        
    lab_tasks = LabTask.objects.all()
    return render(request,'lab_tasks_feed.html',{'lab_tasks':lab_tasks,'room':room})
def feedback_list(request,id):
    room = ProjectRoom.objects.filter(team_members=request.user).first()        
    task=LabTask.objects.get(id=id)
    try:
        file = LabFile.objects.get(lab_task=task, team=room )
        feed = Feedback.objects.get(lab_file=file)
    except LabFile.DoesNotExist or Feedback.DoesNotExist:
        feed = None
    return render(request,'feedback.html',{'feed':feed,'room':room})
def create_task(request):
    # Ensure that the current user is the team leader
    room = ProjectRoom.objects.filter(team_members=request.user).first()
    team_members = room.team_members.all()
    if not request.user == room.team_leader:
        error_message = 'Only team leader can create task'
        return render(request, 'error.html', {'error_message': error_message,'room':room})

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline_str = request.POST.get('deadline')
        assigned_to_id = request.POST.get('assigned_to')

        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
            assigned_to = User.objects.get(id=assigned_to_id)

            task = Task.objects.create(
                room=room,
                title=title,
                description=description,
                deadline=deadline,
                assigned_to=assigned_to,
            )

            # Send email notification to the assigned team member
            subject = 'New Task Assigned By Your Team Leader'
            context = {
                'title': title,
                'description': description,
                'deadline': deadline,
                'assigned_to':assigned_to,
                'room':room
            }
            message = render_to_string('task_assigned.html', context)
            plain_message = strip_tags(message)
            send_mail(subject, plain_message, 'taskflow.info@gmail.com', [assigned_to.email], html_message=message)
            return redirect('create_task')

        except ValueError:
            error_message = 'Invalid deadline format. Please use the correct format.'
            return render(request, 'create_task.html', {'error': error_message})

    return render(request, 'create_task.html', {'team_members': team_members, 'room': room})
def logout_view(request):
    logout(request)
    return redirect('student_login')

def tasks(request):
    # room = get_object_or_404(ProjectRoom, id=room_id)
    room = ProjectRoom.objects.filter(team_members=request.user).first()    
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'tasks.html', {'tasks': tasks,'room':room})
def update_task_status(request, task_id, new_status):
    task = Task.objects.get(id=task_id)
    if task.assigned_to == request.user and task.status == 'Ongoing':
        task.status = new_status
        task.save()
    return redirect('tasks')
def dashboard(request):
    room = ProjectRoom.objects.filter(team_members=request.user).first()
    # room = ProjectRoom.objects.get()
    tasks = Task.objects.filter(room=room)
    return render(request, 'dashboard.html', {'tasks': tasks,'room':room})