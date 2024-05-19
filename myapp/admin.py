from django.contrib import admin
from .models import ProjectRoom,LabTask,LabFile,Feedback,Task
# Register your models here.
admin.site.register(ProjectRoom)
admin.site.register(LabTask)
admin.site.register(LabFile)
admin.site.register(Feedback)
admin.site.register(Task)