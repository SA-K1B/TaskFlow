# models.py
from django.db import models
from django.contrib.auth.models import User

class ProjectRoom(models.Model):
    project_name = models.CharField(max_length=255)
    room_id = models.CharField(max_length=6, unique=True)
    description = models.TextField(null=True)
    team_leader = models.ForeignKey(User, on_delete=models.CASCADE)
    team_members = models.ManyToManyField(User, related_name='team_memberships')
    def __str__(self):
        return self.project_name

class LabTask(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    deadline = models.DateTimeField()

    def __str__(self):
        return self.description

class LabFile(models.Model):
    lab_task = models.ForeignKey(LabTask, on_delete=models.CASCADE)
    team = models.ForeignKey(ProjectRoom, on_delete=models.CASCADE)
    file = models.FileField(upload_to='./media', null=True, blank=True)

    def __str__(self):
        return f"File for Lab Task: {self.lab_task.title} - Team: {self.team.project_name}"
class Feedback(models.Model):
    lab_file = models.ForeignKey(LabFile, on_delete=models.CASCADE)
    content = models.TextField()
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    status_choices = [
        ('Ongoing', 'Ongoing'),
        ('Done', 'Done'),
    ]
    room=models.ForeignKey(ProjectRoom, on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=10, choices=status_choices, default='Ongoing')