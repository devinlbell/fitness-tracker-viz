from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Goal, Contact
from .forms import GoalForm, UpdateForm, ContactForm
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import GoalSerializer
from django.contrib.auth.decorators import login_required
from twilio.rest import TwilioRestClient


# Create your views here.
@login_required(login_url='login/')
def goal_list(request):
	contact = Contact.objects.filter(person=request.user)
	if request.method == "POST":
		form = ContactForm(request.POST)
		if form.is_valid():
			contact = form.save(commit=False)
			contact.person = request.user
			contact.save()
			return redirect('goal_list')
	else:
		if len(contact) != 0:
			form = ''
		else:
			form = ContactForm()
	goals = Goal.objects.filter(person=request.user)
	return render(request, 'fitnesstrackerv/mainview.html', {'goals': goals, 'form':form})

@login_required(login_url='login/')
def update_progress(request, pk):
	goal = get_object_or_404(Goal, pk=pk)
	if request.method == "POST":
		form = UpdateForm(request.POST, instance=goal)
		if form.is_valid():
			goal = form.save(commit=False)
			goal.person = request.user
			goal.save()
			return redirect('goal_detail', pk=goal.pk)
	else:
		form = UpdateForm(instance=goal)
	return render(request, 'fitnesstrackerv/update.html', {'form':form})

@login_required(login_url='login/')
def new_goal(request):
	if request.method == "POST":
		form = GoalForm(request.POST)
		if form.is_valid():
			goal = form.save(commit=False)
			goal.person = request.user
			goal.save()
			return redirect('goal_list')
	else:
		form = GoalForm()
	return render(request, 'fitnesstrackerv/newgoal.html',{'form':form})

@login_required(login_url='login/')
def goal_detail(request, pk):
	goal = get_object_or_404(Goal, pk=pk)
	contact = Contact.objects.filter(person=request.user)
	if goal.progress == 100 and goal.achieved is False:
		goal.achieved = True
		goal.save()
		if len(contact) != 0:
			contact = contact[0]
			account_sid = "for my eyes only"
			auth_token = "thanks twilio"
			client = TwilioRestClient(account_sid, auth_token)
			message = client.messages.create(to=('+1' + str(contact.number)), from_="a twilio number goes here", body="Congratulations on achieving your goal! :)")

	return render(request, 'fitnesstrackerv/goal_detail.html', {'goal':goal})

@login_required(login_url='login/')
def delete_goal(request, pk):
	goal = get_object_or_404(Goal, pk=pk)
	goal.delete()
	return redirect('goal_list')

@api_view(['GET', 'POST'])
def api_list(request):
	if request.method == 'GET':
		goals = Goal.objects.filter(person=request.user)
		serializer = GoalSerializer(goals, many=True)
		return Response(serializer.data)
	elif request.method == 'POST':
		serializer = GoalSerializer(data=request.data)
		if serializer.is_valid():
			serializer.person = request.user
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE']) 
def api_detail(request, pk, format=None): 
	try:
		goal = Goal.objects.get(pk=pk)
	except Goal.DoesNotExist: 
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':         
		serializer = GoalSerializer(goal)         
		return Response(serializer.data)
	elif request.method == 'PUT':        
		serializer = GoalSerializer(goal, data=request.data)
		if serializer.is_valid():             
			serializer.save()             
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	elif request.method == 'DELETE': 
		goal.delete() 
		return Response(status=status.HTTP_204_NO_CONTENT)
