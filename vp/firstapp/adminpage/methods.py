import json
import re
import requests
from django.db import connection

def Version(url):
    f = open(url, "r")
    T=''

    for line in f:
        if 'show version' in line: 
            next(f)
            s=f.readline().split()
            print(s)
            i=s.index('Version')
            T=s[i+1]
            T=T.replace(',','')   
            break
    
    return T

def SerialS(url):
    T=[]
    S=''
    f = open(url, "r")
    for line in f:
        m = re.match("NAME: (.*?), DESCR: (.*?)",line)
        if m:
            try:
                name = m.group(1)
                if (len(name)==10 or len(name)==3 or "System" in name):
                    A=f.readline()
                    i=A.find("SN")
                    T.append(A[i+4:].replace('\n',''))
            except ValueError:
                pass # could 
    return T
    

def IP(url):
    ip=[]
    f = open(url, "r")
    for line in f:
        if 'Internet address is ' in line: 
            ip.append(line)
            break
    i=0
    str1 = ""  
    while i<len(ip):
        for ele in ip[i]:  
            str1 += ele  
        i=i+1 
    position=str1.find('is')+3
    return str1[position:len(str1)-1]
def name(url):
    
    f = open(url, "r")
    s=''
    l=''
    for line in f:
        if 'Key name:' in line:
            l=l+line.replace('Key name:','')
            break
        else:
            if  'hostname' in line:
                l=l+line.replace('hostname','')
                break
    for item in l:
        if item!='.':
             s=s+item
        else:
            break
    s.replace(" ","")
    s.replace('\n',"")
    return s
def Role(url):
    T=[]
    f = open(url, "r")
    for line in f:
        if 'Switch#' in line :
            next(f)
            S=f.readline().split()
            if S!=[]:
                T.append(S[1])
            S=f.readline().split()
            print(S)
            if S!=[]:

                T.append(S[1])
            break
        else :
            if 'Mod  Redundancy role     Operating mode      Redundancy status' in line :
                next(f)
                S=f.readline().split()
                if S!=[]:
                    T.append(S[1])
    
    return T
           
    

def Model(url):
    f = open(url, "r")
    T=[]
    S=''
    for line in f:
        if 'Model Number' in line :
            line=line.replace('Model Number','')
            line=line.replace(' ','')
            line=line.replace('\r\n','')
            line=line.replace('\n','')
            line=line.replace(':','')
            T.append(line)
        else:
            if 'Chassis Type' in line:
                line=line.replace('Chassis Type','')
                line=line.replace(' ','')
                line=line.replace('\r\n','')
                line=line.replace('\n','')
                line=line.replace(':','')
                T.append(line)
            else :
                if 'Chassis type' in line:
                    line=line.replace('Chassis type','')
                    line=line.replace(' ','')
                    line=line.replace('\r\n','')
                    line=line.replace('\n','')
                    line=line.replace(':','')
                    T.append(line)
                else:
                    if 'Model number' in line :
                        line=line.replace('Model number','')
                        line=line.replace(' ','')
                        line=line.replace('\r\n','')
                        line=line.replace('\n','')
                        line=line.replace(':','')
                        T.append(line) 
    
    
                
    return T

def module(url):
    f=open(url, "r")
    nom=[]
    pid=[]
    vid=[]
    SN=[]
    DESC=[]
    T=[]
    for line in f:
        if 'show inventory' in line:
            next(f)
            for line in f:
                if 'PID' in line :
                    line=line.split()
                    pid.append(line[1])
                    vid.append(line[4].replace(',',''))
                    SN.append(line[len(line)-1])
                else:
                    m = re.match("NAME: (.*?), DESCR: (.*?)",line)
                    if m:
                        try:
                            name = m.group(1)
                            nom.append(name)
                            e=line.find("DESCR")
                            s=line[e+8:len(line)-3]
                            DESC.append(s)
                        except ValueError:
                            pass # could 
                    if 'show region' in line:
                        break
    i=0 
    while i<len(nom):
        A=[nom[i],pid[i],vid[i],SN[i],DESC[i]]
        T.append(A)
        i=i+1
    return T
def mem(url):
    T=[]
    S=[]
    f = open(url, "r")
    for line in f:
        if 'show process memory' in line :
            next(f)
            for line in f:
                s=line.split()
                if 'System' in s:
                    T.append(s[3])
                    T.append(s[5])
                    T.append(s[7])
                else:
                    for line in f:
                        if 'Processor Pool Total' in line:
                            s=line.split()
                            i=s.index('Total:')
                            T.append(s[i+1])
                            i=s.index('Used:')
                            T.append(s[i+1])
                            i=s.index('Free:')
                            T.append(s[i+1])
    if len(T)>3:
        T=T[0:3]
    return T
        

def cpu(url):
    T=[]
    f=open(url, "r")
    for line in f:
        if 'show process cpu sorted detailed' in line :
            next(f)
            for line in f:
                if 'CPU utilization' in line :
                    i=line.find('five minutes:')
                    T.append(line[i+14:].replace('\n',''))
            else:
                break
        else :
            if 'show process cpu' in line :
                next(f)
                next(f)
                for line in f:
                    if 'CPU utilization' in line :
                        i=line.find('five minutes:')
                        T.append(line[i+14:].replace('\n',''))
                    else:
                        break
    return T

def fan(url):
    s=[]
    S=[]
    T=[]
    f=open(url,'r')
    for line in f:
        if 'show env' in line :
            next(f)
            for line in f:
                if ('Temperature' or 'TEMPERATURE'  not in line) :
                    s=line.split()
                    T.append(s)
                else:
                    break
    for item in T:
        if 'FAN' in item:
            if item[0]=='FAN':
                if len(item)>3:
                    S.append([item[1],1,item[3]])
                else:
                    S.append([item[0],1,item[2]])

            else:
                if len(item)>3:
                    S.append([item[1],item[3],item[5]])
    return S
def SerialR(url):
    f = open(url, "r")
    for line in f:
        if 'show inventory' in line :
            next(f)
            next(f)
            S=f.readline()
            S=S.split()
            serial=S[len(S)-1]
    return serial
def memR(url):
    T=[]
    S=[]
    f=open(url,'r')
    for line in f:
        if 'show process memory' in line :
            next(f)
            for line in f:
                s=line.split()
                if 'Processor' in s:
                    T.append(s[3])
                    T.append(s[5])
                    T.append(s[7])
                    break
    T=T[0:3]
    return T
def vulnerabilite(version):
    T=[]
    headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                }
    data = {
                    'client_id': 'h6gugu5c3bws6kdgykvm5u5t',
                    'client_secret': '4ApE9G67e98pnCSaKuuFKBNN',
                    'grant_type': 'client_credentials'
                    }
    response = requests.post('https://cloudsso.cisco.com/as/token.oauth2', headers=headers, data=data, verify=False)
    key=response.text
    key=json.loads(key)
    key=key['access_token']
    headers = {
                    'Accept': 'application/json',
                    'Authorization': 'Bearer'+' '+key,
                }
    params = (
                    ('version', version),
                    )
                
    response = requests.get('https://api.cisco.com/security/advisories/ios', headers=headers, params=params, verify=False)
    json_object=json.loads(response.text)
            
    try:
        for item in json_object['advisories']:
            T.append([item['advisoryTitle'],item['firstFixed'][0],item['firstPublished'],item['sir']])
    except Exception as e:
        print(e) 
        
    return T


def eoleos(serial):
    TT=[]
    headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                }
    data = {
                    'client_id': 'gq6wkuvetgj7w7fnyk4ggpjr',
                    'client_secret': 'KdGQCg9A7fRG4HsQsNWmjusn',
                    'grant_type': 'client_credentials'
                    }
    response = requests.post('https://cloudsso.cisco.com/as/token.oauth2', headers=headers, data=data, verify=False)
    key=response.text
    key=json.loads(key)
    key=key['access_token']
    headers = {
                'Accept': 'application/json',
                'Authorization': 'Bearer'+' '+key,
                }
    params = (
                    ('serialNumber', serial),
                    ('MigrationInformation')
                    )
    url='https://api.cisco.com/supporttools/eox/rest/5/EOXBySerialNumber/%s'%serial
    response = requests.get(url, headers=headers,verify=False)
    json_object=json.loads(response.text)
    try:
        for item in json_object["EOXRecord"]:
            TT.append([item['EndOfSaleDate']['value'],item['EndOfServiceContractRenewal']['value'],item['EndOfSWMaintenanceReleases']['value'],item['EndOfSvcAttachDate']['value'],item['EOXExternalAnnouncementDate']['value'],item['EOXMigrationDetails']['MigrationProductId']])
            
    except Exception as e:
        print(e) 
    return TT
def liste_equ(s):
    T=[]
    with connection.cursor() as cursor:
        mysql="Select * from equipment where HostName=%s"
        try:
            cursor.execute(mysql,(s,))
            for item in cursor:
                T.append(item)
        except Exception as e:
            print(e)
    return T
def liste_mod(s):
    T=[]
    with connection.cursor() as cursor:
        mysql="Select * from modules where HostName=%s"
        try:
            cursor.execute(mysql,(s,))
            for item in cursor:
                T.append(item)
        except Exception as e:
            print(e)
    return T
def liste_RAM(s):
    T=[]
    with connection.cursor() as cursor:
        mysql="Select * from RAM where HostName=%s"
        try:
            cursor.execute(mysql,(s,))
            for item in cursor:
                T.append(item)
        except Exception as e:
            print(e)
    return T
def liste_FAN(s):
    T=[]
    with connection.cursor() as cursor:
        mysql="Select * from FAN where HostName=%s"
        try:
            cursor.execute(mysql,(s,))
            for item in cursor:
                T.append(item)
        except Exception as e:
            print(e)
    return T
def list_vul(s):
    T=[]
    with connection.cursor() as cursor:
        mysql2="Select *  from vul where HostName=%s"
        try:
            cursor.execute(mysql2,(s,))
            
            for row in cursor:
                T.append(row)

        except Exception as e:
            print(e)
        
    return T
def list_eox(s):
    T=[]
    with connection.cursor() as cursor:
        mysql2="Select * from eox where HostName=%s"
        try:
            cursor.execute(mysql2,(s,))
            for row in cursor:
                T.append(row)
        except Exception as e:
            print(e)

        
    return T
