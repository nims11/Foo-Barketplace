from django.forms import ModelForm, Form
from django import forms
from models import user_profile, admins

class ProfileForm(ModelForm):
    class Meta:
        model = user_profile
        fields = ('f_name', 'l_name', 'email_visibility', 'about_me')

class AdminProfileForm(ModelForm):
    class Meta:
        model = user_profile

class NickForm(forms.Form):
	nick = forms.CharField(max_length=20)
	def clean_nick(self):
		import re
		#Nick Validation
		regex = re.compile(r'^[a-z][a-z0-9_]+$')
		nick = self.cleaned_data['nick']
		if len(nick)>20 or len(nick)<3 or regex.match(nick)==None:
			raise forms.ValidationError("Nick should have 3-20 lowercase alphanumeric characters, underscores and should start with a letter")

		#Check if nick is available
		try:
			user_profile.objects.get(nick=nick)
			raise forms.ValidationError("Nick %s is already taken!" % nick)
		except user_profile.DoesNotExist:
			return nick

class DelForm(forms.Form):
	confirm = forms.BooleanField(label='Confirm Account Deletion?')

class ConfirmForm(forms.Form):
	confirm = forms.BooleanField(label='Confirm?')

class AddAdminForm(forms.Form):
	email = forms.EmailField(label='Email of the existing user to give admins rights to')
	def clean_email(self):
		email = self.cleaned_data['email']
		# error if user does not exist
		try:
			target_user = user_profile.objects.get(email=email)
		except user_profile.DoesNotExist:
			raise forms.ValidationError("User with such email doesn't exist")
		# error if user is inactive
		if not target_user.is_active:
			raise forms.ValidationError("Inactive User cannot be given admin rights")

		# error if user is already an admin
		try:
			foo = admins.objects.get(email=email)
			raise forms.ValidationError("User already an admin")
		except admins.DoesNotExist:
			# No problems
			return email
