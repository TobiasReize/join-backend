from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user']


class RegistrationSerializer(serializers.ModelSerializer):
    # repeated_password = serializers.CharField(write_only=True)  # write_only=True damit es nicht wieder zurückgegeben wird!
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True      # damit das password auch nur write_only=True ist!
            }
        }
    
    def save(self):     # save-Methode wird überschrieben
        pw = self.validated_data['password']
        # repeated_pw = self.validated_data['repeated_password']

        # if pw != repeated_pw:
        #     raise serializers.ValidationError({'error': 'Passwords don\'t match'})
        
        try:    # es wird geprüft ob die Email bereits vorhanden ist!
            existing_user = User.objects.get(email=self.validated_data['email'])
        except:
            existing_user = None
        
        if existing_user:
            print('existing User with that email: ', existing_user)
            raise serializers.ValidationError({'error': 'Email already exists!'})
        else:
            account = User(email=self.validated_data['email'], username=self.validated_data['username'])    # neues User-Objekt wird erstellt!
            account.set_password(pw)    # von diesem User wird das Passwort gesetzt!
            account.save()
            return account
