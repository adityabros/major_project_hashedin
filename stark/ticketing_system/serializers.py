from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.fields import CurrentUserDefault


from .models import *



class IssueSerializer(serializers.ModelSerializer):
   
   class Meta:
       model = Issue
       fields = ('id','description', 'type', 'status','title','project','reporter','assignee','labels')

    #    fields = ('__all__')

class UpdateIssueSerializer(serializers.ModelSerializer):

    status_codes = {'open':1,'in_progress':2,'in_review':3,'code_complete':4,'done':5} 
    
    def update(self, issue, upd_data):
        role = self.context['request'].user.user_profile.role
        user_id = self.context['request'].user.id
        
        if role == "standard" and issue.assignee.id != user_id:
          raise serializers.ValidationError({"msg": "User not authorized to update Issues"})

        current_status = self.status_codes[issue.status]
        new_status = self.status_codes[upd_data['status']]
        
        
        
        if issue.description != upd_data['description']:
           #create event
           event_log = event_logs.objects.create(updated_field="description",previous_value=issue.description,new_value=upd_data['description'],issue=issue)
        if issue.type != upd_data['type']:
           #create event
           event_log = event_logs.objects.create(updated_field="type",previous_value=issue.type,new_value=upd_data['type'],issue=issue)
        if issue.status != upd_data['status']:
           #create event
           event_log = event_logs.objects.create(updated_field="status",previous_value=issue.status,new_value=upd_data['status'],issue=issue)
        
        if issue.title != upd_data['title']:
           #create event
           event_log = event_logs.objects.create(updated_field="title",previous_value=issue.title,new_value=upd_data['title'],issue=issue)
        if issue.assignee != upd_data['assignee']:
           #create event
           event_log = event_logs.objects.create(updated_field="assignee",previous_value=str(issue.assignee.id),new_value=str(upd_data['assignee'].id),issue=issue)
        
        #avoid status and updating all other fields as we have handled status ourself in different way
        
        for k, v in upd_data.items():
           
           if k != "status" and k != 'labels':
              setattr(issue, k, v)
           elif k == 'labels':
              for lbl in v:
                 issue.labels.add(lbl)

        issue.save()
        status_diff = new_status-current_status
        if new_status < current_status or  status_diff in [1,0]:
           issue.status = upd_data['status']
           issue.save()
           return issue
        else:
           raise serializers.ValidationError('Cannot Jump more than 1 on statuses') 
        

    class Meta:
        model = Issue
        fields = ('id','description', 'type', 'status','title','project','reporter','assignee','labels')

class TimeLogSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = TimeLog
        fields = ('user', 'issue','time_taken','work_description')

class ProjectSerializer(serializers.ModelSerializer):
   issues = IssueSerializer(many=True,read_only=True)

   def create(self, validated_data):
        role = self.context['request'].user.user_profile.role
       
       #Only admin can create projects

        if role != "admin":
          raise serializers.ValidationError({"msg": "User not authorized to create projects"}) 

        return Project.objects.create(**validated_data) 
   class Meta:
       model = Project
       fields = ('description', 'title', 'creator','issues')
    #    fields = ('__all__')

class UpdateProjectSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = Project
        fields = ('title', 'description')

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user

class UserSerializer(serializers.ModelSerializer):
    Project = ProjectSerializer(many=True,read_only=True)
    class Meta:
        model = User
        fields = ('username','Project','email')

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labels
        fields = ('name',)

class WatcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watcher
        fields = ('user','issue')

class WatcherProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatcherProject
        fields = ('user','project')
        

class event_logsSerializer(serializers.ModelSerializer):
    class Meta:
        model = event_logs
        fields = ('updated_field','timestamp','previous_value','new_value','issue')

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('author','text','issue')

class user_profileSerializer(serializers.ModelSerializer):


    class Meta:
        model = User_Profile
        fields = ('user','role')
   
    def update(self, user_profile, upd_data):
      #  print(self.__dir__())
       
       role = self.context['request'].user.user_profile.role
       
       #Only admin can assign roles

       if role != "admin":
          raise serializers.ValidationError({"msg": "User not authorized"})
       user_profile.role = upd_data['role']
       user_profile.save()

       return user_profile


