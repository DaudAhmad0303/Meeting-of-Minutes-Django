from datetime import datetime
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.http import HttpResponseRedirect,HttpResponse
import json
from userAuthentication.models import user
from userProjects.models import userProject,userProjectRecording
from django.http import JsonResponse
from meetingMinutes import settings

# Create your views here.

class createUserProject(View):
    def get(self,request):
        if(request.session.get("userEmail")):
            return render(request,"userProjects/projectCreation.html")
        else:
            loginPage=reverse("sign_In_ULR")
            return HttpResponseRedirect(loginPage)
        
    def post(self,request):
        if(request.session.get("userEmail")):
            userId=request.session["userEmail"]
            userProjectName=request.POST["projectName"]
            if(userProjectName!=""):
                associatedUser=user.objects.get(userEmail=userId)
                try:
                    if(self.isProjectWithSameNameExist(associatedUser,userProjectName)):
                        return HttpResponse(json.dumps({'message': -3}))
                    else:
                        userCreatedProject=userProject(projectName=userProjectName)
                        userCreatedProject.projectCreator=associatedUser
                        userCreatedProject.save(force_insert=True)
                        return HttpResponse(json.dumps({'message': 0}))
                except:
                    return HttpResponse(json.dumps({'message': -2}))
            else:
                return HttpResponse(json.dumps({'message': -1}))
        else:
            return HttpResponse(json.dumps({'message': 1}))
        
    def isProjectWithSameNameExist(self,user,projectName):
        filteredProjects=userProject.objects.filter(projectCreator=user,projectName=projectName)
        return True if(len(filteredProjects)>0) else False
             
class viewUserProjects(View):
    def get(self,request):
        if(request.session.get("userEmail")):
            userId=request.session["userEmail"]
            loggedUser=user.objects.get(userEmail=userId)
            loggedUserProjects=userProject.objects.filter(projectCreator=loggedUser)
            return render(request,"userProjects/recentProjects.html",{"projects":loggedUserProjects})
        else:
            loginPage=reverse("sign_In_ULR")
            return HttpResponseRedirect(loginPage)
    
def logOutFunction(request):
    request.session.clear()
    redirectPath = reverse("sign_In_ULR")
    return HttpResponseRedirect(redirectPath)

class projectRecordings(View):
    def post(self,request,projectId):
        print("Inside upload view")
        if(request.session.get("userEmail")):
            projectRequested=userProject.objects.get(id=projectId)
            self.__saveFileToDB(request, projectRequested)
            return HttpResponse(json.dumps({'message': 0}))
        else:
            return HttpResponse(json.dumps({'message': 1}))

    def __saveFileToDB(self, request, projectRequested):
        presentDateAndTime = datetime.now()
        presentDateAndTime = str(
                presentDateAndTime.strftime("%d %m %Y %H %M %S"))
        for recording in request.FILES.getlist("userFiles"):
            #default file name is recording.name
            fileName=self.__getFileName()
            uploadedRecording=userProjectRecording(myRecording=recording,folderName=presentDateAndTime,fileName=fileName,associatedProject=projectRequested)
            uploadedRecording.save()
            
    def __getFileName(self):
        uploadedRecordings=userProjectRecording.objects.all()
        rankNo=1
        if len(uploadedRecordings)>0:
            rankNo=len(uploadedRecordings)+1
            
        return settings.FILE_INITIAL+str(rankNo)
        
    def get(self,request,projectId):
        if(request.session.get("userEmail")):
            try:
                userEmail=request.session["userEmail"]
                myUser=user.objects.get(userEmail=userEmail)
                projectRequested=userProject.objects.get(id=projectId,projectCreator=myUser)
                projectAssociatedRecordings=userProjectRecording.objects.filter(associatedProject=projectRequested)
                return render(request,"userProjects/projectRecordings.html",{"recordings":projectAssociatedRecordings,"projectId":projectId})
            except:
                invalidRequest=reverse("Page_404",args=["invalidRequest"])
                return HttpResponseRedirect(invalidRequest)
        else:
            loginPage=reverse("sign_In_ULR")
            return HttpResponseRedirect(loginPage)
        
class deleteUserProjects(View):
    def get(self,request):
        invalidRequest=reverse("Page_404",args=["invalidRequest"])
        return HttpResponseRedirect(invalidRequest)
    
    def post(self,request):
        if(request.session.get("userEmail")):
            projectID=request.POST["projectId"]
            try:
                projectToDel=userProject.objects.get(id=projectID)
                projectToDel.delete()
                return HttpResponse(json.dumps({'message': 0}))
            except:
                return HttpResponse(json.dumps({'message': -1}))
        else:
            return HttpResponse(json.dumps({'message': -2}))
        
class updateUserProjects(View):
    def get(self,request):
        invalidRequest=reverse("Page_404",args=["invalidRequest"])
        return HttpResponseRedirect(invalidRequest)
    
    def post(self,request):
        if(request.session.get("userEmail")):
            projectID=request.POST["projectId"]
            projectName=request.POST["projectName"]
            userEmail=request.session["userEmail"]
            myValidator=createUserProject()
            if(projectName!=""):
                try:
                    projectToUpdate=userProject.objects.get(id=projectID)
                    if(projectToUpdate.projectName==projectName):
                        return HttpResponse(json.dumps({'message': -4}))
                    else:
                        myUser=user.objects.get(userEmail=userEmail)
                        if(myValidator.isProjectWithSameNameExist(myUser,projectName)):
                            return HttpResponse(json.dumps({'message': -5}))
                        else:
                            projectToUpdate.projectName=projectName
                            projectToUpdate.save()
                            return HttpResponse(json.dumps({'message': 0}))
                except:
                    return HttpResponse(json.dumps({'message': -1}))
            else:
                return HttpResponse(json.dumps({'message': -2}))
        else:
            return HttpResponse(json.dumps({'message': -3}))
        
class deleteRecordingFile(View):
    def get(self,request):
        invalidRequest=reverse("Page_404",args=["invalidRequest"])
        return HttpResponseRedirect(invalidRequest)
    
    def post(self,request):
        if(request.session.get("userEmail")):
            recordingFileID=request.POST["recordingID"]
            try:
                fileToDelete=userProjectRecording.objects.get(id=recordingFileID)
                fileToDelete.delete()
                return HttpResponse(json.dumps({'message': 0}))
            except:
                return HttpResponse(json.dumps({'message': -1}))
        else:
            return HttpResponse(json.dumps({'message': -2}))
        