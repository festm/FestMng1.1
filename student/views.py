# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import template
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Fuser,Request,Brmsg,QCM,Oversee,FileUpload,CallMeet
from django.contrib.auth.decorators import login_required,user_passes_test #even after loging in the function only if he is certain user
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from random import randint, choice
from string import ascii_lowercase,digits
from django.utils.timezone import now as timezone_now
from datetime import datetime,date

register = template.Library()

def saveData(request):

	if request.method == "POST":
		cid = request.POST['spid']
		print(cid)
		
	if Fuser.objects.filter(fid=cid).exists():
		if Fuser.objects.filter(fid=cid,nop=0).exists() :
 			return redirect(dispCred,cid)
		else:
			check = {}
			check['msg'] = 1
			check['flag'] = 0
			return render(request, 'login.html',check)	
	else:
		text="""<h2> Invalid ID </h2>"""
		check = {}
		check['msg'] = 2
		check['flag'] = 0
		return render(request, 'login.html',check)

def gen_rand_user(length=8,chars=ascii_lowercase+digits,split=4,delimiter='-'):
	check = ''.join([choice(chars) for i in xrange(length)])
	return check
	
	
def dispCred(request,id):

	if Fuser.objects.filter(fid=id,nop=1).exists():
			text="""<h1> Credentials already issued </h1>"""
			check = {}
			check['msg'] = 1
			check['flag'] = 0

			return render(request, 'login.html',check) 

#			return render(request, 'login.html',check)
	if Fuser.objects.filter(fid=id).exists() == False:
			text="""<h1> Invalid ID </h1>"""
			check = {}
			check['msg'] = 1
			check['flag'] = 0
			return render(request, 'login.html',check)			
			

	obj=Fuser.objects.filter(fid=id)
	
	resp={}
	resp['flag']=1
	resp['msg'] = 0
		
	
	usn = gen_rand_user()
	pw = gen_rand_user()
	
	resp['username']=usn
	print(pw)
	while User.objects.filter(username=resp['username']):
		resp['username'] = gen_rand_user()
	resp['password']=pw
	user = User.objects.create_user(username = usn,password = pw,email='')
	fob=Fuser.objects.filter(fid=id).update(nop=1,un=usn)
	return render(request, 'login.html',resp)


def fourdig(request):
#need to write code to check if first time
	return render(request, 'start.html')

def user_rating_def(usernm):

	count = 0
	time_taken = 0
	for r in Request.objects.filter(touser = usernm):
		count = count + 1
	for u in Request.objects.filter(touser = usernm,result='done'):
		f_date = u.created_at
		l_date = u.done_at
		delta = l_date - f_date
		time_taken = time_taken + delta.seconds/60/60
		
	ideal_time = count * 24
	eff = (time_taken* 100/ideal_time) 
	if eff < 20 :
		return 1
	elif eff < 40 :
		return 2
	elif eff < 60 :
		return 3
	elif eff < 80 :
		return 4
	else :
		return 5
		
def count_req_no(usernm):
	countr = 0
	counta = 0
	countp = 0
	countc = 0
	counts = 0
	check = {}
	for r in Request.objects.filter(touser = usernm):
		if r.result == 'done':
			countr = countr + 1
			counta = counta + 1
			countc = countc + 1
		elif r.result == 'yes' :
			countr = countr + 1
			counta = counta + 1
		else :
			countr = countr + 1
	for r in Request.objects.filter(fromuser = usernm):
		counts = counts + 1
		
	check['countr'] = countr
	check['counta'] = counta
	check['countp'] = countp
	check['countc'] = countc
	check['counts'] = counts
	
	return check

		
	
@login_required(login_url='/signin')	
def home(request):
	
	resp ={}
	rp1={}
	rp2={}
	msgs = {}
	msgs =  Brmsg.objects.all()	
	
	current_user = request.user.username
	rating = user_rating_def(current_user)
	count_req = count_req_no(current_user)
	rec_act = Request.objects.filter(fromuser = current_user)
	files = FileUpload.objects.all()
	
#	current_user = User.get_username()
	if Fuser.objects.filter(un=current_user,filter=1).exists():
		flag=False
	else :
		flag=True

		
	if Oversee.objects.filter(qcms=current_user).exists():
		g=True #display 
	else:
		g=False
	
	oobj=Oversee.objects.filter(qcms=current_user)	
	rp1 = dispreqno(request)
	rp2 = meetcheck(request)
	rp3 = dispdonereq(request)
	rp1['notif'] = rp1['notif'] + rp3['notif']
	resp['one']=rp1
	resp['two']=rp2
	resp['three']=rp3
	resp['curr']=flag
	resp['g']=g
	resp['rating']=rating
	resp['name'] = current_user
	resp['count']=count_req
	resp['msgs'] = msgs
	resp['rec_act'] = rec_act
	resp['myfiles'] =files
	resp['qobj']=oobj

	return render(request,'production/index.html',resp)

def meetcheck(request):

	count=0
	ch={}
	req={}
	current_user = request.user
	for r in CallMeet.objects.filter(cto=current_user, stat='not seen'):
		req[count] = {'fruser1':r.cfrom,'msg':r.agen,'id':count}
		count = count + 1
		
	ch['notif'] = count
	ch['req'] = req
	return ch
	
@login_required(login_url='/signin')	
def dispreqno(request):
	count = 0
	check = {}

	req = {}
	current_user = request.user
	for r in Request.objects.filter(touser=current_user,result='notseen'):
		req[count] = {'fruser1':r.fromuser_id,'msg':r.descrp,'rid':r.rid}
		count = count + 1
		
	check['notif'] = count
	check['req'] = req
	return check
	
@login_required(login_url='/signin')	
def dispdonereq(request):
	count = 0
	check = {}

	req = {}
	current_user = request.user
	for r in Request.objects.filter(fromuser=current_user,result='done'):
		req[count] = {'fruser1':r.touser_id,'msg':r.descrp,'rid':r.rid}
		count = count + 1
		
	check['notif'] = count
	check['req'] = req
	return check
	
@login_required(login_url='/signin')	
def prof(request):
	response ={}
	current_user = request.user.username
#	current_user = User.get_username()
	response['name'] = current_user
	count = 0 
	for r in Request.objects.filter(touser=current_user):
		count = count + 1
	response['notif'] = count
	response['flag']=0
	for u in Fuser.objects.filter(un=current_user):
		if u.nop == 1 :
			fob=Fuser.objects.filter(fid=id).update(nop=2)
			response['flag']=1
			
	return render(request,'production/profile.html',response)

@login_required(login_url='/signin')	
def pendrequestchk(request,req):
	resp = {}	
	rp1 = {}
	rp2 = {}
	rp1 = dispreqno(request)
	rp2 = meetcheck(request)
	rp3 = dispdonereq(request)
	rp1['notif'] = rp1['notif'] + rp3['notif']
	resp['one']=rp1
	resp['two']=rp2
	r = Request.objects.get(rid = req)
	resp['rid'] = r.rid
	resp['fromuserreq'] = r.fromuser
	resp['msg'] = r.descrp
	resp['date'] = r.date
	resp['type'] = r.Type
	return render(request,'production/pendrequestchk.html',resp)	
	
@login_required(login_url='/signin')	
def pendrequest(request):
	count = 0
	req = {}
	rp2={}
	current_user = request.user.username
	response = {}
	rp1 = dispreqno(request)
	rp2= meetcheck(request)
	rp3 = dispdonereq(request)
	rp1['notif'] = rp1['notif'] + rp3['notif']
	response['one'] = Request.objects.filter(touser=current_user,result='yes')
	response['name'] = current_user
	response['two']=rp2
	return render(request,'production/pendrequest.html',response)

@login_required(login_url='/signin')	
def updpendreq(request,req):
	
	if request.method == "POST":
		curr_req = Request.objects.get(rid = req)
		curr_req_check = Request.objects.filter(rid  = req).update(result = 'done')
		files = request.FILES.getlist('myfiles')
		for a_file in files:
			print('hello')
			instance = FileUpload(
				rid=curr_req,
				file_name=a_file.name,
				attachment=a_file
			)
			instance.save()
			
	return redirect('/index')
	
@login_required(login_url='/signin')	
def profupd(request):

	return redirect('/index')
	
#Request View
	
@login_required(login_url='/signin')	
def recrequest(request):
	resp ={}
	rp1={}
	rp2={}
	
	current_user = request.user.username
#	current_user = User.get_username()
	rp1 = dispreqno(request)
	rp2= meetcheck(request)
	rp3 = dispdonereq(request)
	rp1['notif'] = rp1['notif'] + rp3['notif']
	resp['one']=rp1
	resp['two']=rp2
	resp['name'] = current_user
	return render(request,'production/recrequest.html',resp)

@login_required(login_url='/signin')	
def recrequestchk(request,req):
	resp ={}
	rp1={}
	rp2={}
	current_user = request.user.username
	rp1 = dispreqno(request)
	rp2= meetcheck(request)
	rp3 = dispdonereq(request)
	rp1['notif'] = rp1['notif'] + rp3['notif']
	resp['one']=rp1
	resp['two']=rp2
	r = Request.objects.get(rid = req)
	resp['rid'] = r.rid
	resp['fromuserreq'] = r.fromuser
	resp['msg'] = r.descrp
	resp['type'] = r.Type
	count = 0
	rp = {}
	if r.Type == 'approv' :
		resp['files'] = FileUpload.objects.filter(rid = r.rid)
	resp['date'] = r.date
	
	return render(request,'production/acrequest.html',resp)
	
@login_required(login_url='/signin')	
def updreq(request,req):
	
	if request.method == "POST":
		print(request.POST['resp'])
		obj = Request.objects.filter(rid = req).update(result = request.POST['resp'])
		obj1 = Request.objects.get(rid = req)
		if obj1.Type == 'approv':
			obj = Request.objects.filter(rid = req).update(result = 'done',done_at=timezone_now())
			
	return redirect('/index')	

#Request View End
	
@login_required(login_url='/signin')	
def newmsg(request):

	if request.method == "POST":
		msg = request.POST['msg']	
		check = random_no()
		while Brmsg.objects.filter(mid=check):
			check = random_no()
		obj = Brmsg()
		obj.mid = check
		obj.msg = msg
		obj.save()
		
	return redirect('/index')	
	
@login_required(login_url='/signin')	
def newreq(request, to='xyzab'):
	response ={}
	rp1={}
	rp2={}
	rp1 = dispreqno(request)
	rp2= meetcheck(request)
	rp3 = dispdonereq(request)
	rp1['notif'] = rp1['notif'] + rp3['notif']
	allUsers = User.objects.all()
	current_user = request.user.username
	response['name'] = current_user
	response['users'] = allUsers
	response['one']=rp1
	response['two']=rp2
	allFusers = Fuser.objects.all().exclude(un=current_user)
	response['allFusers'] = allFusers	
	count = 0
	for r in Request.objects.filter(touser=current_user):
		count = count + 1

	if to == 'xyzab':
		flag=False
	else :
		flag=True
	response['flag']=flag
	response['notif'] = count	
	response['touser']=to
	

	return render(request,'production/request.html',response)
	
	
@register.assignment_tag()
def random_no(length=3) :
		return randint(10**(length-1),(10**(length)-1))

@login_required(login_url='/signin')		
def savereq(request,par):

	if request.method == 'POST' :

		
		if par == 'xyzab':
			type = request.POST['type']
			descrp = request.POST['message']
			to = request.POST.getlist('tousers1')
			datereq = request.POST['date']
			check = random_no()
			
			
			for c in to :
				obj = Request()
				obj.touser= User.objects.get(username = c)
				while Request.objects.filter(rid=check):
					check = random_no()
				obj.rid=check
				obj.Type=type
				obj.descrp=descrp
				obj.fromuser = request.user	
				obj.date = datereq
				obj.save()
				if request.POST['type'] == 'approv':
					files = request.FILES.getlist('myfiles')
					for a_file in files:
						instance = FileUpload(
							rid=obj,
							file_name=a_file.name,
							attachment=a_file
						)
						instance.save()
				
		else:
			type = request.POST['type']
			descrp = request.POST['message']
			datereq = request.POST['date']
			check = random_no()
			key=range(3)
			d=""
			p=""
			for i in key:
				d=d+par[i]
				if i!=2 :
					p=p+par[i+3]
		
			if Fuser.objects.filter(un=request.user,dept=d).exists():
				f=True #same dept
			else:
				f=False #diff dept
			
			g=True
			
			if f==True :
			
				curr=Fuser.objects.get(un=request.user)
				if p=='su' :
					to = curr.subc
				elif p=='co' :
					to = curr.core
				else:
					g=False
				
				if g==True:
					
					while Request.objects.filter(rid=check):
						check = random_no()
					obj = Request()
					obj.rid=check
					obj.Type=type
					obj.descrp=descrp
					obj.fromuser = request.user
					obj.touser = to
					obj.date = datereq
					obj.save();
					if request.POST['type'] == 'approv':
						files = request.FILES.getlist('myfiles')
						for a_file in files:
							instance = FileUpload(
								rid=obj,
								file_name=a_file.name,
								attachment=a_file
							)
							instance.save()
					
			if f==False or g==False:
				
				to = 'admin'
				minw=10
				
				for usr in Fuser.objects.filter(dept=d,post=p):
					count=0
					for r in Request.objects.filter(touser=usr.un):
						count = count + 1
					if count<minw :
						minw=count
						to = usr
					else :
						to = Fuser.objects.get(un='admin')
				
				print(to)
				
				while Request.objects.filter(rid=check):
					check = random_no()
					
				obj = Request()
				obj.rid=check
				obj.Type=type
				obj.descrp=descrp
				obj.fromuser = request.user
				obj.touser = to
				obj.date = datereq
				obj.save();
				
				if request.POST['type'] == 'approv':
						files = request.FILES.getlist('myfiles')
						for a_file in files:
							instance = FileUpload(
								rid=obj,
								file_name=a_file.name,
								attachment=a_file
							)
							instance.save()
							
				if g==True: #diff dept
					 
					if ( d=='log' or d=='des') and Fuser.objects.filter(un=request.user.username, dept='ecc').exists():
						# identify which qcm su to send notification to
						minw=10
						for qrec in QCM.objects.filter(qdept= 'doc',qpost='su'):
							count=0
							for rec in Request.objects.filter(touser=qrec.quser) :
								count = count +1
							if count<minw:
								minw=count
								toq = User.objects.get(username=qrec.quser)
							else :
								toq = User.objects.get(username='admin')
						print toq
						sobj = Oversee()
						print check
						sobj.link = FileUpload.objects.get(rid=check)
						print sobj.link
						sobj.fromd = 'ecc'
						sobj.tod = d
						sobj.qcms = toq
						sobj.msg = descrp
						sobj.save();
						
			
	return redirect('/index')	

def callameet(request):

	resp={}
	rp1={}
	rp2={}
	current_user = request.user.username
	rp1 = dispreqno(request)
	rp2= meetcheck(request)
	rp3 = dispdonereq(request)
	rp1['notif'] = rp1['notif'] + rp3['notif']
	resp['one']=rp1
	resp['two']=rp2
	resp['name'] = request.user.username
	cobj = Fuser.objects.all().exclude(un=request.user.username)
	curr = User.objects.get(username=request.user)
	resp['allFusers']=cobj
	resp['curu']=curr
	
	return render(request,'production/callmeet.html',resp)
	
def signin(request):
	response = {}
	if request.method == 'POST' :
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is None :
			return render(request,'login.html',response)
		else :
			login(request,user)
			return redirect('/index')
	return render(request,'login.html',response) #simply pressed login with no details redirect bakc
		
def logout_view(request):
    logout(request)
    return render(request,'login.html')		


def saveameet(request):

	
	if request.method == 'POST':
		
		datt = request.POST['date']
		venue = request.POST['venue']
		agenda = request.POST['agenda']
		#use_TZ=False
		
		x= request.POST.getlist('to[]')
		for c in x:
			call = CallMeet()
			call.cto = User.objects.get(username = c)
			call.dati = datt
			call.cfrom = request.user
			call.ven = venue
			call.agen = agenda
			call.save()

			
	return redirect('/index')

	
@login_required(login_url='/signin')	
def sentreq(request):
	resp ={}
	rp1={}
	rp2={}
	
	current_user = request.user.username
#	current_user = User.get_username()
	rp1 = Request.objects.filter(fromuser=current_user)

	rp2 = meetcheck(request)
	resp['one']=rp1
	resp['two']=rp2
	resp['name'] = current_user
	return render(request,'production/sentreq.html',resp)

def calldisp(request):

	resp ={}
	rp1={}
	rp2={}
	current_user = request.user.username
	obj = CallMeet.objects.get(cto=current_user)
	rp1 = dispreqno(request)
	rp2 = meetcheck(request)
	resp['one']=rp1
	resp['two']=rp2
#	resp['from']= User.objects.get(username=obj.cfrom)
	resp['objc']=obj
	return render(request,'production/callchk.html',resp)

def updmeet(request,fro):

	if request.method ==  'POST':
	
		res=request.POST['resp']
		obj=CallMeet.objects.filter(cto=request.user,cfrom=fro).update(rep=res,stat='seen')
		
	return redirect('/index')

