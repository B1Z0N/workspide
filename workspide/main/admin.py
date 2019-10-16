from django.contrib import admin

from .models import User, \
    Responsibilities, SkillsForResume, SkillsForVacancy, Vacancy, PetProject, Resume

def AdminFactory(name : str):
    return type(name + "Admin", admin.ModelAdmin)

admin.site.register(User)
admin.site.register(Responsibilities)
admin.site.register(SkillsForResume)
admin.site.register(SkillsForVacancy)
admin.site.register(Vacancy)
admin.site.register(PetProject)
admin.site.register(Resume)
