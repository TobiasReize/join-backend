from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'user']
        # fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True      # damit das password auch nur write_only=True ist!
            }
        }
    
    def save(self):     # save-Methode wird überschrieben
        print('self.validated_data:', self.validated_data)
        user_name = self.validated_data['email']    # username=email (für Login)
        f_name = self.validated_data['first_name']
        l_name = self.validated_data['last_name']
        mail = self.validated_data['email']
        pw = self.validated_data['password']
        
        try:    # es wird geprüft ob die Email bereits vorhanden ist!
            existing_user = User.objects.get(email=self.validated_data['email'])
        except:
            existing_user = None
        
        if existing_user:
            print('existing User with that email: ', existing_user)
            raise serializers.ValidationError({'error': 'Email already exists!'})
        else:
            account = User(username=user_name, first_name=f_name, last_name=l_name, email=mail, is_staff=True)    # neues User-Objekt wird erstellt!
            account.set_password(pw)    # von diesem User wird das Passwort gesetzt!
            account.save()
            user_profil = UserProfile.objects.create(user=account, first_name=f_name, last_name=l_name, email=mail)
            print('user_profil:', user_profil)
            return account
