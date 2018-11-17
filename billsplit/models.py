from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Group(models.Model):
	groupName = models.CharField(max_length=100)
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	creationDate = models.DateTimeField('date created')
	members = models.IntegerField(default=1)

	def __str__(self):
		return self.groupName

class GroupAllocation(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	joinDate = models.DateTimeField('date joined')

	def __str__(self):
		return self.group.groupName + ":" + self.user.username

class Bill(models.Model):
	title = models.CharField(max_length=100)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
	paidBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="paidBy")
	amount = models.IntegerField(default=0)
	time = models.DateTimeField('Transaction Time')

	def __str__(self):
		return str(self.group) + ":" + self.title

class BillSharer(models.Model):
	bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.bill) + ":" + str(self.user)

class Transaction(models.Model):
	lender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lender")
	borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrower")
	amount = models.FloatField(default=0)

	def __str__(self):
		return str(self.lender) + "->" + str(self.borrower)

class RequestSettlement(models.Model):
	transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
	requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requester")
	requested = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requested")
	time = models.DateTimeField('Time for request')

	def __str__(self):
		return str(self.transaction)+" "+str(self.transaction.amount)+":"+str(self.requester)+"->"+str(self.requested)

class SetteledTransaction(models.Model):
	lender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lenderSettled")
	borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowerSettled")
	amount = models.FloatField(default=0)
	time = models.DateTimeField('Time settled by both parties')

	def __str__(self):
		return str(self.lender) + "->" + str(self.borrower)


# class Transaction(models.Model):
# 	bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
# 	lender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lender")
# 	borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrower")
# 	def __str__(self):
# 		return str(self.bill) + ":" + self.lender +"->"+self.lender


