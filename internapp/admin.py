from django.contrib import admin
from internapp.models import (
    User,
    Task,
    InternProfile,
    SupervisorProfile,
    SubmittedTask,
)

# Register your models here.
admin.site.register([User, InternProfile, SupervisorProfile, Task, SubmittedTask])
