from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
import random
import datetime
from django.db.models import Sum
# for redirect them get url
from django.urls import reverse
from django.http import HttpResponse
import requests
# from django.contrib.auth.models import User
# for sms send import client in twilio.rest
# from django.http import JsonResponse
from twilio.rest import Client
import vonage
from django.contrib.auth.decorators import login_required
# from django.db.models import F 
# from datetime import datetime, timedelta
# from django.db.models import DurationField, ExpressionWrapper

# Create your views here.
# def index(request):
#     return render(request, 'app/index.html')
@login_required
def home(request):
    last = customer.objects.filter(verifystatus = '1').order_by('id')
    c_user= customer.objects.filter(verifystatus = '1').count()
    c_fetch= product.objects.filter( released = '0').count()
    tot = product.objects.filter( released = '0').aggregate(Sum('principal'))
    nt = product.objects.filter( released = '0', transfer='0').count()
    trf = product.objects.filter( released = '0', transfer='1').count()

    # gold and silver rate api
    jsi='https://www.goldapi.io/api/XAU/INR'
    jsj='https://www.goldapi.io/api/XAG/INR'
    headers = {
    # "x-access-token": "goldapi-4bxdrrlnu99py7-io",
    "x-access-token": "goldapi-19rvkrrlo1djj6s-io",
    "Content-Type": "application/json"
    }

    # gold xau
    re=requests.get(jsi,headers=headers).json()
    # print(re)
    try:
        g=re['price_gram_24k']
        gs=g*6.6/100
        gl=g+gs
        # print(gl)
             # print(sl)
    except:
        gl='check a Monthly pack' 
    
    # silver xag
    ren=requests.get(jsj,headers=headers).json()
    # print(ren)
    try:
        s=ren['price_gram_24k']
        ss=s*26/100
        sl=s+ss
             # print(sl)
    except:
        sl='check a Monthly pack'

    
    return render(request,'app/home.html', { 'last': last, 'user':c_user, 'fetch':c_fetch, 'tot':tot ,'gold':gl ,'silver':sl ,'ntrans':nt , 'trans':trf } )

@login_required
def newregister(request):
    return render(request,'app/newregister.html')

@login_required
def newfeatch(request):
    inst = customer.objects.filter(verifystatus = '1').order_by('-id')
    return render(request,'app/newfeatch.html', {'data': inst} )


def sms(mssg,number):
    # print(mssg,number)
    #tiwilio start this 
    # account_sid = 'AC0f36c1cb50bae7fabbc54e01dcc27bb7'
    # auth_token = '8bf1f913729105d54493577b25ea2257'
    # client = Client(account_sid, auth_token)
    # message = client.messages.create(
    #     from_='+12055060846',
    #     body= mssg ,
    #     # use to as a number but here not pay so one varify number only use so when we pay then to =number ;put there 
    #     # to='+91'+str(number)
    #     to='+919488625124'
    # )tiwilio end
    client = vonage.Client(key="a26edf0e", secret="KDvGERw0QVJYrVnF")
    sms = vonage.Sms(client)
    # responseData = 
    sms.send_message(
    {
        "from": "Vonage APIs",
        "to": "916374186124",
        "text": mssg,
    }
    )
    # if responseData["messages"][0]["status"] == "0":
    #     print("Message sent successfully.")
    # else:
    #     print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
    print(mssg,number)
    # print(message.sid)
    #twilio measese give it return HttpResponse('SMS sent successfully!')
    # range = regiverfy.objects.create(number=number,verifyid=ran)

@login_required
def register(request):
        if request.method == 'POST':
#  if request.header.get('x-requested-with')=='XMLHt
            name= request.POST['name']
            fname= request.POST['fname']
            aadhar= request.POST['aadhar']
            number= request.POST['number']
            adress= request.POST['adress']
            img = request.FILES['photo']   
            ran = random.randint(1000,9999)
            cust = customer.objects.filter(aadhar=aadhar,verifystatus='1')
            if cust:
                messages.warning(request,"USER in Already Exists For this Aadhar Number")
                return redirect('newregister') 
            else:
                inst = customer.objects.create(name=name , fname=fname, aadhar =aadhar, contact=number , adress=adress , userimg=img, verifyotp=ran)
                if inst: 
                    mssg='your OTP for a registration in Sri AMBAL BANKERS is:'+ str(ran)
                    sms(mssg,number)
                    messages.success(request,"Send OTP to the Registered mobile Number ")
                    return render(request,'app/otpverifyuser.html' , {'number': number} ) 

@login_required
def otpverifyuser(request):     
    return render(request,'app/otpverifyuser.html')

@login_required
def verify67(request):
        if request.method == 'POST':
            otp= request.POST['otp']
            number= request.POST['number']
            resu = customer.objects.filter(contact=number , verifystatus='0', verifyotp=otp)
            if resu:
                rasu = customer.objects.filter(contact=number , verifystatus='0', verifyotp=otp).latest('id')
                resk=customer.objects.get(id=rasu.id)
                resk.verifystatus = '1'
                resk.save()
                messages.success(request,"User Successfully Registared")
                return redirect('home')
            
@login_required
def featchsearch(request):
       if request.method == 'POST':
        number= request.POST['num']
        search=  customer.objects.all().filter(contact = number  , verifystatus = '1')
        # search = customer.objects.filter(contact = number  , verifystatus='1')
        if search:
             return render(request,'app/featchsearch.html', {'data': search})
        else:
            messages.success(request,"Non of the Result is Exits")
            return redirect('newfeatch')
        
@login_required
def featchpage(request,pk):
    get_data = customer.objects.get(id=pk)
    if get_data:
        return render(request, "app/featchpage.html" , {'data': get_data} )

@login_required
def fetch(request):
    # return render(request, "app/fetchprint.html")
    if request.method == 'POST':
        custid= request.POST['userid']
        princ= request.POST['princ']
        rate= request.POST['rat_int']
        gm= request.POST['gm']
        pro_detail= request.POST['pro_detail']
        tot_rate= request.POST['tot_rate']
        re_date= request.POST['re_date']
        img = request.FILES['photo']   
        get_data = customer.objects.get(id=custid)

        inst = product.objects.create(principal=princ , rate=rate, gm = gm, productdetail=pro_detail , productprice=tot_rate , returndue=re_date ,fleatchdate=datetime , productimg=img, customer=get_data, intrest='0')
        if inst:
            number= inst.customer.contact
            prid = inst.id
            n=inst.customer.name
            fn=inst.customer.fname
            p=inst.principal
            rd=inst.returndue
            mssg = 'Mr/Mrs ' + str(n) + ' ' + str(fn) + ',  Your Featch is Successfully Entered. Your Featch id is : '+ str(prid) + '  Principal Amount is : '+ str(p) +' Please Return Within '+ str(rd)
            sms( mssg , number )
            messages.success(request,"Successfully Enter the this featch products")
            return render(request, "app/fetchprint.html" , {'data': inst} )
        else:
            messages.success(request,"Something want to error so ReEnter this Products")
            return redirect('newfeatch')

@login_required
def custview(request, pk):
    get_data = customer.objects.get(id=pk)
    data = product.objects.filter(customer=pk).order_by('fleatchdate')
    data_c = product.objects.filter(customer=pk).count()
    if get_data or  data:
        return render(request, "app/custview.html" , {'cust': get_data , 'prod' : data , 'totcot': data_c} )

@login_required
def relese1(request):
    if request.method == 'POST':
        pk = request.POST['proid']
        rest =product.objects.filter(id=pk,transfer='0', released='0')
        reson =product.objects.filter(id=pk , transfer='1')
        rel = product.objects.filter(id=pk, transfer='0' , released='1')
        if reson:
            messages.success(request,"In this item is transfered to any other bankes")
            return redirect('relese1')
        elif rel:
            messages.success(request,"In this item is already relesed")
            return redirect('relese1')
        elif rest:
            res =product.objects.get(id=pk,transfer='0', released='0')
            return render(request, "app/relese2.html" , {'data': res})
        else:
            messages.success(request,"In this item ID is wrong")
            return redirect('relese1')
    return render(request, "app/relese1.html" )

@login_required
def relese2(request,im):
    get_data = product.objects.get(id=im,transfer='0', released='0')
    if get_data:
        return render(request, "app/relese2.html" , {'data': get_data})
    else:
        messages.success(request,"In this item ID is Wrong")
        return redirect('relese1')
    
@login_required
def sionly(request):
    if request.method == 'POST':
        pn = request.POST['proid']
        si = request.POST['intrest']
        if si == '0' or si <= '0' :
            messages.success(request,"In this intrest is already payed (or) intrest is non...")
            # return redirect('relese1') 
            return redirect(reverse('relese2', kwargs={'im':pn}))
        else:
            get_data = product.objects.get(id=pn ,transfer='0', released='0')
            i=get_data.intrest
            k= int(si) + int(i) 
            sh=product.objects.get(id=pn)
            sh.intrest = k
            sh.save()
            result=sh
            # print(result)
            if result:
                n= result.customer.name
                number= result.customer.contact
                fn=result.customer.fname
                h = result.intrest
                pid = result.id
                mssg = 'Mr/Mrs ' + str(n) + ' ' + str(fn) + ',  Your Intrest is Successfully payed for a Featch id  : '+ str(pid) + '  Payed Amount is : '+ str(si) +'  Thankyou!!!'
                sms( mssg , number )
                messages.success(request,"Successfully Payed the intrest")
                return render(request, "app/sionlyprint.html" , {'data': result, 'iny': si } )
        

@login_required
def closefetch(request):
    # return HttpResponse("hii its from the closefetch")
    if request.method == 'POST':
        pn = request.POST['proid']
        si = request.POST['intrest']
        get_data = product.objects.get(id=pn ,transfer='0', released='0')  
        i=get_data.intrest
        k= int(si) + int(i) 
        sh=product.objects.get(id=pn)
        sh.intrest = k
        sh.releasedate = datetime.datetime.now()
        sh.released= '1' 
        sh.save()
        result=sh
        if result:
            n= result.customer.name
            number= result.customer.contact
            fn=result.customer.fname
            h = result.principal
            sn=int(h)+int(si)
            pid = result.id
            mssg = 'Mr/Mrs ' + str(n) + ' ' + str(fn) + ',  Your Featch is Successfully Closed for a Featch id  : '+ str(pid) + '  Payed Amount is : '+ str(sn) +'  Thankyou!!!'
            sms( mssg , number )
            messages.success(request,"Successfully Enter the this featch products")
            return render(request, "app/sionlyprint.html" , {'daa': result, 'ine': sn} )
        





















