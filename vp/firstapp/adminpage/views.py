from django.template import loader
import xlsxwriter

from django.contrib.auth.decorators import login_required

from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import *
from django.db import connection
from django.views.generic import TemplateView
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from math import floor
import requests
import json
import csv
from django.urls import reverse
from django.utils.encoding import smart_str
import mimetypes
from pathlib import Path
from django.core.exceptions import ValidationError
from .methods import *

# Create your views here.
def home(request): 
      
    # render function takes argument  - request 
    # and return HTML as response 
    

    return render(request, "index.html") 

def login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            # with connection.cursor() as cursor:
            #     cursor.execute('SELECT MAX(EquipID) FROM equipment')
            #     for row in cursor:
            #         id=row[0]
            return redirect("/menu")
        else:
            messages.info(request,'invalid credentials')
            return redirect("/")
@login_required(login_url='/')
def menu(request): 
    context={}
    nom=''
    IP_Adress=''
    Versionn=''
    hostname=''
    desc=''
    pid=''
    vid=''
    serialno=''
    ida=''

    if request.method=='POST':
        network = request.POST.get('name')
        typee = request.POST.get("type")
        uploaded_file=request.FILES['document']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        context['url']=fs.url(filename) 
        print(fs.url(filename))  
        file_name, file_extension = os.path.splitext(fs.url(filename))
        print(file_extension)
        if (file_extension=='.log' or file_extension==''):
            model=Model('/Users/mac/vp/firstapp'+fs.url(filename).replace("%20", " "))
            nom=name('/Users/mac/vp/firstapp'+fs.url(filename).replace("%20", " ")).replace(" ","")
            nom=nom.replace("\n","")
            nom=nom.replace("\r","")
            print(nom)
            IP_Adress=IP('/Users/mac/vp/firstapp'+fs.url(filename).replace("%20", " "))
            Versionn=Version('/Users/mac/vp/firstapp'+fs.url(filename).replace("%20", " "))
            role=Role('/Users/mac/vp/firstapp'+fs.url(filename).replace("%20", " "))
            Tableau=module('/Users/mac/vp/firstapp'+fs.url(filename).replace("%20", " "))
            Vul=vulnerabilite(Versionn)
            CPU=cpu('/Users/mac/vp/firstapp'+fs.url(filename).replace("%20", " "))
        
            if typee=='1':
                FAN=fan('/Users/mac/vp/firstapp'+fs.url(filename).replace("%20", " "))
                print(FAN)
                RAM=mem('/Users/mac/vp/firstapp'+fs.url(filename).replace("%20", " "))
                print('RAM='+str(RAM))
                SNS=SerialS('/Users/mac/vp/firstapp'+fs.url(filename).replace("%20", " "))
                with connection.cursor() as cursor:
                    mySql_insert_query = """INSERT INTO equipment (HostName, IPAddress,type, Version,EquipSN,Rolee,Model,CPU,network) 
                                VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s) """
                    i=0
                    C=[0]*len(SNS)
                    while i<len(CPU):
                        C.insert(i,CPU[i])
                        i=i+1
                    i=0   
                    r=['null']*len(SNS)
                    while i<len(role):
                        r.insert(i,role[i])
                        i=i+1
                    i=0
                    while i<len(SNS):
                        recordTuple = (nom,IP_Adress,'Switch',Versionn,SNS[i],r[i],model[i],C[i],network)
                        try:
                            cursor.execute(mySql_insert_query, recordTuple)
                        except Exception as e:
                            print(e)
                        i=i+1
                    mySql_insert_query = """INSERT INTO RAM (EquipSN,HostName,network,total,used,free) 
                                VALUES (%s, %s, %s,%s,%s,%s) """
                    i=0
                    while i<len(SNS):
                        recordTuple = (SNS[i],nom,network,RAM[0].strip(""),RAM[1].strip(""),RAM[2].strip(""))
                        try:
                            cursor.execute(mySql_insert_query, recordTuple)
                    
                        except Exception as e:
                            print(e)
                        i=i+1
                    
                    # ////EOX///////
                    i=0
                    while i<len(SNS):
                        
                        TT=eoleos(SNS[i])
                        mysql="""INSERT INTO eox (hostName,serialno,network,EndOfSaleDate,EndOfServiceContractRenewal,EndOfSWMaintenanceReleases,EndOfSvcAttachDate,EOXExternalAnnouncementDate,EOXMigrationDetails) 
                                VALUES (%s,%s, %s, %s,%s,%s,%s,%s,%s) """
                        for item in TT:
                            recordTuple = (nom,SNS[i],network,item[0],item[1],item[2],item[3],item[4],item[5])
                            try:
                                cursor.execute(mysql, recordTuple)
                            except Exception as e:
                                print(e)
                        i=i+1


                    # ///////////RAM
                    mySql_insert_query = """INSERT INTO RAM (EquipSN,HostName,network,total,used,free) 
                                VALUES (%s, %s, %s,%s,%s,%s) """
                    mySql_insert_query_module = """INSERT INTO modules (HostName,Modname,DESCRI, PID, VID,EquipSN) 
                                VALUES (%s,%s, %s, %s,%s,%s) """
                    i=0
                    while i<len(Tableau):
                        try:
                            recordTuple = (nom,Tableau[i][0],Tableau[i][4],Tableau[i][1],Tableau[i][2],Tableau[i][3])
                            cursor.execute(mySql_insert_query_module, recordTuple) 
                        except Exception as e:
                            print(e)
                        i=i+1
                    mySql_insert_query = """INSERT INTO FAN (HostName,module,FANNo,network,state) 
                                VALUES (%s,%s, %s, %s,%s) """
                    for item in FAN:
                        if item!=[]:
                            try:
                                recordTuple = (nom,str(item[0]).strip(""),str(item[1]).strip(""),network,str(item[2]).strip(""))
                                cursor.execute(mySql_insert_query, recordTuple) 
                            except Exception as e:
                                print(e)
            else:
                if typee=='2':
                    RAM=memR('/Users/mac/vp/firstapp'+fs.url(filename).replace("%20", " "))
                    SNR=SerialR('/Users/mac/vp/firstapp'+fs.url(filename).replace("%20", " "))
                    with connection.cursor() as cursor:
                        mySql_insert_query = """INSERT INTO equipment (HostName, IPAddress,type,Rolee, Version,EquipSN,Model,CPU,network) 
                                VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s) """
                        
                        
                        recordTuple = (nom,IP_Adress,'Routeur','',Versionn,SNR,model[0],CPU[0],network)
                        try:
                            cursor.execute(mySql_insert_query, recordTuple)
                        except Exception as e:
                            print(e)
                        mySql_insert_query = """INSERT INTO RAM (EquipSN,HostName,network,total,used,free) 
                                VALUES (%s, %s, %s,%s,%s,%s) """
                        recordTuple = (SNR,nom,network,RAM[0].strip(""),RAM[1].strip(""),RAM[2].strip(""))
                        try:
                            cursor.execute(mySql_insert_query, recordTuple)
                        except Exception as e:
                            print(e)
                        mySql_insert_query_module = """INSERT INTO modules (HostName,Modname,DESCRI, PID, VID,EquipSN) 
                                VALUES (%s,%s, %s, %s,%s,%s) """
                        i=0
                        while i<len(Tableau):
                            try:
                                recordTuple = (nom,Tableau[i][0],Tableau[i][4],Tableau[i][1],Tableau[i][2],Tableau[i][3])
                                cursor.execute(mySql_insert_query_module, recordTuple) 
                            except Exception as e:
                                print(e)
                            i=i+1
                        # /////////////////EOX ROUTEUR
                        TT=eoleos(SNR)
                        mysql="""INSERT INTO eox (hostName,serialno,network,EndOfSaleDate,EndOfServiceContractRenewal,EndOfSWMaintenanceReleases,EndOfSvcAttachDate,EOXExternalAnnouncementDate,EOXMigrationDetails) 
                                VALUES (%s,%s, %s, %s,%s,%s,%s,%s,%s) """
                        for item in TT:
                            recordTuple = (nom,SNR,network,item[0],item[1],item[2],item[3],item[4],item[5])
                            try:
                                cursor.execute(mysql, recordTuple)
                            except Exception as e:
                                print(e)
                        

                        
                
            mySql_insert_query = """INSERT INTO vul (hostName,version,network,titre,publicationdate,impact,firstfixed) 
                                VALUES (%s,%s, %s, %s,%s,%s,%s) """
            with connection.cursor() as cursor:
                for item in Vul:
                    recordTuple = (nom,Versionn,network,item[0],item[1],item[2],item[3])
                    try:
                        cursor.execute(mySql_insert_query, recordTuple)
                    except Exception as e:
                        print(e)
    return render(request, "index2.html",context) 




@login_required(login_url='/')

def element(request):
    
    T=[]
    
   
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM equipment order by date_added desc')
        for row in cursor:
            T.append(row)
            
    return render(request,"element.html",{'T':T})

def download(request):
    T= [['SerialNo','Role','Model','IPAddress','HostName','Version','CPU','client']]
    with connection.cursor() as cursor:
        cursor.execute("Select * from equipment")
        for item in cursor:
            T.append(item)
        
    with open('media/Equipements.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for item in T:                        
            filewriter.writerow(item)
    

    return HttpResponseRedirect('/media/Equipements.csv')
def upload(request):
    if request.method == 'POST':
        mylist=request.POST.getlist('input')
        print(mylist)

    if mylist!=False:
        T= [['HostName','IPAddress','Model','Version','SerialNo','type','Role','CPU','client']]
        M=[['HostName','Modname','DESCRI','PID','VID','EquipSN']]
        R=[['EquipSN','HostName','network','total','used','free']]
        F=[['HostName','Switch/PS','FANNo','network','state']]
        V= [['HostName','Version','Network','titre','impact','first fixed','Publication Date']]
        E= [['HostName','SerialNo','Network','EndOfSaleDate','EndOfServiceContractRenewal','EndOfSWMaintenanceReleases','EndOfSvcAttachDate','EOXExternalAnnouncementDate','EOXMigrationDetails']]


        for item in mylist:
            for row in liste_equ(item):
                T.append(row)

            for row in liste_mod(item):
                M.append(row)
            for row in liste_RAM(item):
                R.append(row)
            for row in liste_FAN(item):
                F.append(row)
            
            for row in list_vul(item):
                V.append(row)
            for row in list_eox(item):
                E.append(row)
            
        
        
        with open('media/Equipements.csv', 'w') as csvfile:
            csvfile.write('Equipements :')
            csvfile.write('\n\n')
            
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for item in T:                        
                filewriter.writerow(item)
            csvfile.write('\n\n')
            csvfile.write('Modules :')
            csvfile.write('\n\n')
            for item in M:                        
                filewriter.writerow(item)
                        
            csvfile.write('\n\n')
            csvfile.write('RAM/CPU :')
            csvfile.write('\n\n')
            for item in R:                        
                filewriter.writerow(item)
            csvfile.write('\n\n')
            csvfile.write('FAN :')
            csvfile.write('\n\n')
            for item in F:                        
                filewriter.writerow(item)
            csvfile.write('\n\n')
            csvfile.write('Vulnerabilites :')
            csvfile.write('\n\n')
            for item in V:                        
                filewriter.writerow(item)
            csvfile.write('\n\n')
            csvfile.write('EOX :')
            csvfile.write('\n\n')
            for item in E:                        
                filewriter.writerow(item)
        return HttpResponseRedirect('/media/Equipements.csv')

    else:
        return render(request, "element.html") 
def uploadram(request):
    if request.method == 'POST':
        mylist=request.POST.getlist('input')
        print(mylist)
    if mylist!=False:
        T= [['HostName','SerialNo','type','cpu','client','total','used','free']]
        with connection.cursor() as cursor:
            
            for item in mylist:
                mysql="Select R.Hostname,R.EquipSN,type,e.cpu,R.network,total,used,free from equipment e,RAM R where R.EquipSN=e.EquipSN and R.EquipSN=%s order by date_added desc"
                try:
                    cursor.execute(mysql,(item,))
                    for item in cursor:
                        T.append(item)
                except Exception as e:
                    print(e)
                
                
            
        with open('media/RAM.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for item in T:                        
                filewriter.writerow(item)
        return HttpResponseRedirect('/media/RAM.csv')

    else:
        return render(request, "ramcpu.html") 



def downloadmod(request):

    if request.method == 'POST':
        ida= request.POST['id']
        print('id='+ida)
        T=[['Modname','Hostname','DESCRI','PID','VID','EquipSN','EquipID']]
        with connection.cursor() as cursor:
            mySql_insert_query ="Select * from modules where HostName=%s order by date_added desc"
            
            try:
                cursor.execute(mySql_insert_query,(ida,))
                for item in cursor:
                    T.append(item)
                url='media/Module+%s.csv'%(ida)
                with open(url, 'w') as csvfile:
                    filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                    for item in T:                        
                        filewriter.writerow(item)
                return HttpResponseRedirect(url)
            except Exception as e:
                print(e)
            
        
    
def RAMCPU(request):
    T=[]
    
   
    with connection.cursor() as cursor:
        cursor.execute('SELECT R.hostname,R.EquipSN,R.network,e.type,cpu,total,used,free FROM equipment e,RAM R where R.EquipSN=e.EquipSN')
        for row in cursor:
            T.append(row)
    


    
    
    

    return render(request,"ramcpu.html",{'T':T})
    
def downloadram(request):
    S= [['HostName','SerialNo','CPU','SerialNo','CPU','Total RAM','Used RAM','Free RAM']]
    with connection.cursor() as cursor:
        cursor.execute('SELECT distinct HostName FROM equipment order by date_added desc')
        rows = cursor.fetchall()
        for row in rows:
            T=[]
            host=str(row[0]).replace(" ","")
            host=host.replace("\n","")
            host=host.replace("\r","")
            print(host)
            T.append(host)
            mysql="Select EquipSN,cpu FROM equipment where HostName=%s order by date_added desc"
            cursor.execute(mysql,(host,))
            rowss = cursor.fetchall()
            for row in rowss:
                T.append(str(row[0]))
                T.append(str(row[1]))
            mysql="Select DISTINCT total,used,free from RAM where HostName=%s order by date_added desc"
            cursor.execute(mysql,(host,))
            rowsss = cursor.fetchall()
            for row in rowsss:
                total=str(row[0]).replace("K","000")
                used=str(row[1]).replace("K","000")
                free=str(row[2]).replace("K","000")
                T.append(total)
                T.append(used)
                T.append(free)
            S.append(T)
                
             
    print(S)
        
    with open('media/RAMCPU.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for item in S:                        
            filewriter.writerow(item)
    

    return HttpResponseRedirect('/media/RAMCPU.csv')
    

def FAN(request):
    
    T=[]
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM FAN order by date_added desc')
        for row in cursor:
            T.append(row)
      
    print(T)

    return render(request,"fan.html",{'T':T})

def vul(request):
    
    T=[]    
    with connection.cursor() as cursor:
        cursor.execute('SELECT * from vul order by date_added desc')
        for row in cursor:
            T.append(row)
        
    
        
    

    
    return render(request,"vul.html",{'T':T})
                




def updatevul(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT Distinct version from vul')
        row = cursor.fetchall()
        for item in row:
            version=item
            T=vulnerabilite(item)
            for item in T:
                mysql='update vul set titre=%s,firstfixed=%s,publicationdate=%s,impact=%s where version=%s'
                recordTuple = (item[0],item[1],item[2],item[3],version)
                try:
                    cursor.execute(mysql,recordTuple)
                except Exception as e:
                    print(e)
    return render(request, "vul.html")



    
    
                

def eox(request):
    
    T=[]
    
   
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM eox order by date_added desc')
        for row in cursor:
            T.append(row)
    
    
    return render(request,"eox.html",{'T':T})


def uploadvul(request):
    if request.method == 'POST':
        mylist=request.POST.getlist('input')
        print(mylist)

    if mylist!=False:
        T= [['Version','Network','titre','Publication Date','impact','first fixed']]
        with connection.cursor() as cursor:
            
            for item in mylist:
                mysql="Select * from vul where version=%s order by date_added desc"
                try:
                    cursor.execute(mysql,(item,))
                    for item in cursor:
                        T.append(item)
                except Exception as e:
                    print(e)
                
                
            
        with open('media/Vulnerabilites.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for item in T:                        
                filewriter.writerow(item)
        return HttpResponseRedirect('/media/Vulnerabilites.csv')

    else:
        return render(request, "vul.html") 
    
def updateeox(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT Distinct serialno from eox')
        row = cursor.fetchall()
        for item in row:
            serial=item
            T=eoleos(item)
            for item in T:
                mysql='update eox set EndOfSaleDate=%s,EndOfServiceContractRenewal=%s,EndOfSWMaintenanceReleases=%s,EndOfSvcAttachDate=%s,EOXExternalAnnouncementDate=%s,EOXMigrationDetails=%s where serialno=%s'
                recordTuple = (item[0],item[1],item[2],item[3],item[4],item[5],serial)
                try:
                    cursor.execute(mysql,recordTuple)
                except Exception as e:
                    print(e)
    return render(request, "eox.html")


def uploadeox(request):
    if request.method == 'POST':
        mylist=request.POST.getlist('input')
        print(mylist)

    if mylist!=False:
        T= [['SerialNo','Network','EndOfSaleDate','EndOfServiceContractRenewal','EndOfSWMaintenanceReleases','EndOfSvcAttachDate','EOXExternalAnnouncementDate','EOXMigrationDetails']]
        with connection.cursor() as cursor:
            
            for item in mylist:
                mysql="Select * from eox where serialno=%s order by date_added desc"
                try:
                    cursor.execute(mysql,(item,))
                    for item in cursor:
                        T.append(item)
                except Exception as e:
                    print(e)
                
                
            
        with open('media/EOX.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for item in T:                        
                filewriter.writerow(item)
        return HttpResponseRedirect('/media/EOX.csv')

    else:
        return render(request, "eox.html") 
def logout(request):
    auth.logout(request)
    return redirect("/")