def updateeox():
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
