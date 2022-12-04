from django.urls import path,include
from . import views

urlpatterns = [
    path("createProject",views.createUserProject.as_view(),name="project_creation"),
    path("logout",views.logOutFunction,name="LOG_OUT"),
    path("userProjects",views.viewUserProjects.as_view(),name="loadProjects"),
    path("deleteProject",views.deleteUserProjects.as_view(),name="deleteUserProject"),
    path("updateProject",views.updateUserProjects.as_view(),name="updateUserProject"),
    path("deleteRecordingFile",views.deleteRecordingFile.as_view(),name="deleteUserRecordingFile"),
    path("userProjectMeetings/<int:projectId>",views.projectRecordings.as_view(),name="loadProjectMeetings"),
    
]
