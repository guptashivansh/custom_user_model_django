from django.contrib.auth import (
							authenticate,
							get_user_model,
							login,
							logout)
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from .forms import (
					UserLoginForm,
					RegisterForm,
					UserAdminCreationForm,
					UserAdminChangeForm
				)
# Create your views here.

def login_view(request):
	# print(request.user.is_authenticated())
	if request.user.is_authenticated: # if user is already logged in
		print("Pehle se hi logged in ho")
		return HttpResponseRedirect('/')
	next = request.GET.get('next')
	title = "Login"
	form = UserLoginForm(request.POST or None)
	if request.method == "POST":
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(email=email,password=password)
		if user is None:
			User = get_user_model()
			user_queryset = User.objects.all().filter(
				Q(username__iexact=email) |
				Q(mobile__iexact=email)
				)
			if user_queryset:
				username = user_queryset[0].email
				print(username)
				user = authenticate(email=username, password=password)
		if user is not None:
			login(request,user)
			if next:
				return redirect(next)
			return redirect("/")
		else:
			return HttpResponse("invalid login")
		
		
	return render(request,"forms.html",{"form":form, "title":title})

def register_view(request):
	title = "Register"
	if request.user.is_authenticated: # if user is already logged in
		return HttpResponseRedirect('/')
	form = RegisterForm(request.POST or None)
	next = request.GET.get('next')

	if form.is_valid():
		# print(request.user.is_authenticated())
		user = form.save(commit = False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		new_user = authenticate(email=user.email,password=password)
		login(request, new_user)
		if next:
			return redirect(next)
		return redirect("/")

	context = {
		"form":form,
		"title":title,
	}
	return render(request,"forms.html",context)

def logout_view(request):
	logout(request)
	return redirect("/")
