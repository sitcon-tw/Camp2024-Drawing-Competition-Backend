from django.contrib import admin
from api.models import Challenge, Round, Team, Submission

# Register your models here.
class SubmissionAdmin(admin.ModelAdmin):
    search_fields = ['team__id','challenge__id','round__id']
    list_filter = ['team','challenge','round','status']


admin.site.register(Challenge)
admin.site.register(Round)
admin.site.register(Team)
admin.site.register(Submission,SubmissionAdmin)
