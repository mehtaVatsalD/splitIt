from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Group, GroupAllocation, Bill, BillSharer, Transaction, RequestSettlement, SetteledTransaction
from datetime import datetime
from django.db.models import Q

# Create your views here.
def index(request):
	if request.user.is_authenticated==False:
		return redirect('/splitit/login')
	transactionsBorrow = Transaction.objects.filter(borrower=request.user)
	transactionsLend = Transaction.objects.filter(lender=request.user)
	requestedToUser = RequestSettlement.objects.filter(requested=request.user)
	setteledTransactions = SetteledTransaction.objects.filter(Q(borrower=request.user) | Q(lender=request.user))
	data = {"transactionsBorrow":transactionsBorrow, "transactionsLend": transactionsLend, "requestedToUser": requestedToUser, "setteledTransactions": setteledTransactions}
	return render(request, 'splitit/index.html', data)

def login_redirect(request):
	return redirect('/splitit/login')

def login(request):
	if request.user.is_authenticated:
		return redirect('/splitit')
	if request.method == 'GET':
		return render(request, 'splitit/login.html')
	elif request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			auth_login(request, user)
			return redirect('/splitit/')
		else:
			messages.error(request, 'Invalid username or password.')
		return redirect('/splitit/login')

def logout(request):
	auth_logout(request)
	messages.success(request, 'Successfully Logged out. Come back soon:)')
	return redirect('/splitit/login')


def signup(request):
	if request.user.is_authenticated:
		return redirect('/splitit')
	if request.method == 'GET':
		return render(request, 'splitit/signup.html')
	elif request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		cpassword = request.POST['cpassword']
		if username == '' or password == '':
			messages.error(request, 'Fill all the fields.')
		elif password != cpassword:
			messages.error(request, 'Password and Confirm Password are not matching.')
		else:
			user = User.objects.create_user(username=username, password=password, is_staff=False, is_superuser=False)
			messages.success(request, 'Successfully signedup. Login to continue.')
			return redirect('/splitit/login')
		return redirect('/splitit/signup')

def newgroup(request):
	if request.user.is_authenticated==False:
		return redirect('/splitit/login')
	if request.method == 'GET':
		return render(request, 'splitit/newgroup.html')
	elif request.method == 'POST':
		grpname = request.POST['grpname']
		newgrp = Group(groupName=grpname, creator=request.user, creationDate= datetime.now())
		newgrp.save()
		grpAlloc = GroupAllocation(group=newgrp, user= request.user, joinDate=datetime.now())
		grpAlloc.save()
		return redirect('/splitit/mygroups/'+str(newgrp.id)+'/')

def groupMembers(request, group_id):
	if request.user.is_authenticated==False:
		return redirect('/splitit/login')
	groupToGive = Group.objects.get(id=group_id)
	if groupToGive.creator == request.user:
		members = GroupAllocation.objects.all().filter(group=groupToGive)
		data = {"members": members, "grpname": groupToGive.groupName, "grpid": groupToGive.id}
		return render(request, 'splitit/groupmems.html' ,data)
	else:
		return HttpResponse('Not Authorized')
	#return HttpResponse(members)

def mygroups(request):
	if request.user.is_authenticated==False:
		return redirect('/splitit/login')
	groups = Group.objects.all().filter(creator = request.user)
	data = {"groups": groups}
	return render(request, 'splitit/mygroups.html', data)

def searchforadding(request, grpid, searchKey):
	if request.user.is_authenticated==False:
		return HttpResponse(status=500)
	group = Group.objects.get(id=grpid)
	allocatedUsers = GroupAllocation.objects.filter(group=group)
	allocatedUsersList = [ allocatedUser.user.username for allocatedUser in allocatedUsers ]
	users = User.objects.filter(Q(username__contains=searchKey))
	dataToSend = []
	for user in users:
		if user.username not in allocatedUsersList:
			dataToSend.append({'id':user.id, 'username': user.username})
	return JsonResponse(dataToSend, safe=False)

def addusertogrp(request, grpid, userid):
	if request.user.is_authenticated==False:
		return HttpResponse(status=500)
	group = Group.objects.get(id=grpid)
	allocatedUsers = GroupAllocation.objects.filter(group=group)
	allocatedUsersList = [ allocatedUser.user.id for allocatedUser in allocatedUsers ]
	if request.method == "POST":
		if int(userid) in allocatedUsersList:
			return JsonResponse({"response":"User Already Added!"})
		else:
			usertoadd = User.objects.get(id=userid)
			grpAlloc = GroupAllocation(group=group, user= usertoadd, joinDate=datetime.now())
			grpAlloc.save()
			group.members+=1;
			group.save()
			return JsonResponse({"response":"success"}, safe=False)
	else:
		return HttpResponse(status=500)

def removeuserfrmgrp(request, grpid, userid):
	if request.user.is_authenticated==False:
		return HttpResponse(status=500)
	group = Group.objects.get(id=grpid)
	allocatedUsers = GroupAllocation.objects.filter(group=group)
	allocatedUsersList = [ allocatedUser.user.id for allocatedUser in allocatedUsers ]
	if request.method == "POST":
		if int(userid) not in allocatedUsersList:
			return JsonResponse({"response":"User Not Added!"})
		else:
			usertormv = User.objects.get(id=userid)
			grpAlloc = GroupAllocation.objects.get(group=group, user= usertormv).delete()
			group.members-=1;
			group.save()
			return JsonResponse({"response":"success"}, safe=False)
def delgrp(request, grpid):
	if request.user.is_authenticated==False:
		return HttpResponse(status=500)
	group = Group.objects.get(id=grpid)
	if request.method == "DELETE":
		group.delete()
		return JsonResponse({"response":"success"}, safe=False)

def showallgrps(request):
	if request.user.is_authenticated==False:
		return redirect('/splitit/login')
	allocations = GroupAllocation.objects.filter(user=request.user).distinct()
	groups = [allocation.group for allocation in allocations]
	data = {"groups": groups}
	return render(request, 'splitit/allocgrps.html', data)

def addbill(request, grpid):
	if request.user.is_authenticated==False:
		return redirect('/splitit/login')
	group = Group.objects.get(id=grpid)
	if request.method=="GET":
		allocations = GroupAllocation.objects.filter(group=group)
		usersingrp = [{'id':allocation.user.id, 'username':allocation.user.username} for allocation in allocations]
		bills = Bill.objects.filter(group=group).order_by("-time")
		dataToSend = []
		for bill in bills:
			sharers = BillSharer.objects.filter(bill=bill)
			dataToSend.append({"bill":bill, "sharers": sharers})
		data = {"bills": dataToSend, "grpid": grpid, "usersingrp" : usersingrp}
		return render(request, 'splitit/addbill.html', data)
	elif request.method=="POST":
		title = request.POST["title"]
		paidbyId = request.POST["paidby"]
		paidby = User.objects.get(id=paidbyId)
		amount = request.POST["amount"]
		creator = request.user
		bill = Bill(title=title, group=group, creator=creator, paidBy=paidby, amount=amount, time=datetime.now())
		bill.save()
		sharers = request.POST.getlist("shrUsr")
		totalSharers = len(sharers)
		perShare = int(amount)/totalSharers;
		for sharer in sharers:
			userToAdd = User.objects.get(id=sharer)
			billSharer = BillSharer(bill=bill, user=userToAdd)
			billSharer.save();
			if userToAdd!=paidby:
				try:
					transaction1 = Transaction.objects.get(lender=userToAdd, borrower=paidby)
				except Transaction.DoesNotExist as e:
					try:
						transaction2=Transaction.objects.get(lender=paidby, borrower=userToAdd)
					except Transaction.DoesNotExist as e:
						newTransaction = Transaction(lender=paidby, borrower=userToAdd, amount=perShare)
						newTransaction.save()
					else:
						transaction2.amount+=perShare
						transaction2.save()
				else:
					if transaction1.amount > perShare:
						transaction1.amount-=perShare
						transaction1.save()
					elif transaction1.amount < perShare:
						newAmount = perShare - transaction1.amount
						transaction1.delete()
						newTransaction = Transaction(lender=paidby, borrower=userToAdd, amount=newAmount)
						newTransaction.save()
					elif transaction1.amount == perShare:
						transaction1.delete()
		messages.success(request, 'Bill successfully added')
		return redirect('/splitit/addbill/'+str(grpid))

def settlerequest(request, transactionId):
	if request.user.is_authenticated==False:
		return HttpResponse(status=500)
	if request.method=="POST":
		transaction = Transaction.objects.get(id=transactionId)
		requestMade = RequestSettlement.objects.filter(transaction=transaction)
		if len(requestMade) != 0:
			messages.error(request, 'Already requested.')
			return HttpResponse("error")
		requester=request.user
		if requester==transaction.lender:
			requested=transaction.borrower
		else:
			requested=transaction.lender
		newRequest = RequestSettlement(transaction=transaction, requester=requester, requested=requested, time=datetime.now())
		newRequest.save()
		messages.success(request, 'Successfully requested for settlement to '+str(requested))
		return HttpResponse("success", status=200)
	else:
		return HttpResponse(status=500)

def settle(request, requestId, transactionId):
	if request.user.is_authenticated==False:
		return HttpResponse(status=500)
	if request.method == "POST":
		requestMade = RequestSettlement.objects.get(id=requestId)
		transaction = Transaction.objects.get(id=transactionId)
		requestMade.delete()
		setteledTransaction = SetteledTransaction(lender=transaction.lender, borrower=transaction.borrower, amount=transaction.amount, time=datetime.now())
		transaction.delete()
		setteledTransaction.save()
		messages.success(request, 'Successfully Settled.')
		return HttpResponse("success", status=200)
	else:
		return HttpResponse(status=500)


