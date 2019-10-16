from django.contrib import admin

from .models import User, \
    Responsibility, SkillForResume, SkillForVacancy, Vacancy, PetProject, Resume

def AdminFactory(name : str):
    return type(name + "Admin", admin.ModelAdmin)

admin.site.register(User)
admin.site.register(Responsibility)
admin.site.register(SkillForResume)
admin.site.register(SkillForVacancy)
admin.site.register(Vacancy)
admin.site.register(PetProject)
admin.site.register(Resume)
