#-*- coding:utf-8 -*-

from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from xlutils.copy import copy
import xml.dom.minidom
import string,httplib,urllib,sys,time,datetime
import threading
import MySQLdb
import os
import xlrd
import xlwt
import webbrowser




ss_url  = "/pss/oss.aspire"
css_host ='10.12.3.213:21111'  
css_host_gd='10.12.3.201:48888'
#logfile = 'D:\WORK\lljzdh\log.txt'
logdir ='D:\\auto_test\\log'
basedir='D:\\auto_test'
tempdir='D:\\auto_test\\template'
#logdetailfile = r'D:\WORK\lljzdh\logdetail.txt'
Failed_Count = 0
Succeed_Count = 0
OPR=''


def initdata(paras):
    conn= MySQLdb.connect(
        host='10.12.9.161',
        port = 3306,
        charset='utf8',
        user='hub_pss',
        passwd='hub_pss',
        db ='hub_pss',
        client_flag=6
        )
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    #print str
   
    cur.execute(str(paras[0]).encode('utf8'))
    cur.close()
    conn.commit()
    conn.close()
    print "*------ִ执行initdata脚本-----------*"
    return 0

def initdata_nm(paras):
    conn= MySQLdb.connect(
        host='10.12.9.161',
        port = 3306,
        charset='utf8',
        user='nm_wap',
        passwd='nm_wap',
        db ='nm_wap',
        client_flag=6
        )
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    #print str
   
    cur.execute(str(paras[0]).encode('utf8'))
    cur.close()
    conn.commit()
    conn.close()
    print "*------ִ执行initdata脚本-----------*"
    return 0

def initdata_gd(paras):
    conn= MySQLdb.connect(
        host='10.12.9.161',
        port = 3306,
        charset='utf8',
        user='testpss',
        passwd='testpss',
        db ='gdpss',
        client_flag=6
        )
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(str(paras[0]).encode('utf8'))
    
    cur.close()
    conn.commit()
    conn.close()
    print "*------执行initdata脚本-----------*"
    return 0

def fresh_mem(paras):
    url=paras[0]
    webbrowser.open(url, new=0, autoraise=True)
    time.sleep(1)
    os.system("TASKKILL/F /IM chrome.exe") #关闭浏览器方式太过粗暴
    
def delay(paras):
    T=paras[0]
    T=float(T)
    print T
    time.sleep(T)
    
def checkdata(paras):
    conn= MySQLdb.connect(
        host='10.12.9.161',
        port = 3306,
        charset='utf8',
        user='hub_pss',
        passwd='hub_pss',
        db ='hub_pss'
        )
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(paras[0])
    rs =cur.fetchall()
    indx1=str(rs).find('(')
    indx2=str(rs).find(',)')
    rs1=str(rs)[indx1+1:indx2]
    rs1=rs1.replace('Decimal', '')
    rs1=rs1.replace('None','0')
    rs1=str(rs1)
    #dict=eval(rs1)
    #dict=dict['result']
    dict1=eval(rs1)['result']
    print float(dict1)
    print float(paras[1])
    print float(dict1)==float(paras[1])
    print "True 表示期望检查的数据正确，Flase表示数据错误"
    if float(dict1)==float(paras[1]):
#   if str(dict)==str(paras[1]):
        return 0    
    else:
        return 1

    cur.close()
    conn.commit()
    conn.close()  
    
def checkdata_nm(paras):
    conn= MySQLdb.connect(
        host='10.12.9.161',
        port = 3306,
        charset='utf8',
        user='nm_wap',
        passwd='nm_wap',
        db ='nm_wap'
        )
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(paras[0])
    rs =cur.fetchall()
    indx1=str(rs).find('(')
    indx2=str(rs).find(',)')
    rs1=str(rs)[indx1+1:indx2]
    rs1=rs1.replace('Decimal', '')
    rs1=rs1.replace('None','0')
    rs1=str(rs1)
    #dict=eval(rs1)
    #dict=dict['result']
    dict1=eval(rs1)['result']
    print float(dict1)
    print float(paras[1])
    print float(dict1)==float(paras[1])
    print "True 表示期望检查的数据正确，Flase表示数据错误"
    if float(dict1)==float(paras[1]):
#   if str(dict)==str(paras[1]):
        return 0    
    else:
        return 1

    cur.close()
    conn.commit()
    conn.close()  
    
def log(str1):
    filestr = open(logfile, 'a+' ) 
    starttime=time.time()
    #if type(str1) == type([]):
    #    str1 = [str(li) for li in str1]
    #log_str = '  '.join(str1)
    #print type(log_str),log_str.encode
  
    filestr.write(time.strftime(u'%Y-%m-%d %H:%M:%S',time.localtime(starttime))+'  '+str(str1))
    filestr.write('\n')
    filestr.close()
  
def logdetail(str2):
    filestr = open(logdetailfile, 'a+' ) 
    starttime=time.time()
    filestr.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(starttime))+'  '+str(str2))
    filestr.write('\n')
    filestr.write(str2)
    filestr.write('\n')
    filestr.close()      

def driver( xlsfile, sheetname,index):
    xls = xlrd.open_workbook( xlsfile, formatting_info=True )
    sheet = xls.sheet_by_name(sheetname)
    newWb = copy(xls);
    ws = newWb.get_sheet(int(index));
    
    ret=10
    
    font0= xlwt.Font()
    font0.name= 'Times New Roman'
    font0.colour_index= 3
    font0.bold= True
    style0= xlwt.XFStyle()
    style0.font= font0
    
    font1= xlwt.Font()
    font1.name= 'Times New Roman'
    font1.colour_index= 2
    font1.bold= True
    style1= xlwt.XFStyle()
    style1.font= font1
    
    #create db conn
    
    print sheetname
    
    for li in range( 1, sheet.nrows ):
        name = sheet.cell( li, 0 ).value
        paras=['']*14
        paras[0]=sheet.cell( li, 2 ).value
        paras[1]=sheet.cell( li, 3 ).value
        paras[2]=sheet.cell( li, 4 ).value
        paras[3]=sheet.cell( li, 5 ).value
        paras[4]=sheet.cell( li, 6 ).value
        paras[5]=sheet.cell( li, 7 ).value
        paras[6]=sheet.cell( li, 8 ).value
        paras[7]=sheet.cell( li, 9 ).value
        paras[8]=sheet.cell( li, 10).value
        paras[9]=sheet.cell( li, 11).value
        paras[10]=sheet.cell( li, 12).value
        paras[11]=sheet.cell( li, 13).value
        paras[12]=sheet.cell( li, 14).value
        paras[13]=sheet.cell( li, 15).value
        
        if  name=='shakeDraw':
            ret=shakeDraw(paras)
        elif name=='tigerDraw':
            ret=tigerDraw(paras)
        elif name=='queryProducts':
            ret=queryProducts(paras)
        elif name=='queryUserAcct':
            ret=queryUserAcct(paras)  
        elif name=='queryUserAcctDetails':
            ret=queryUserAcctDetails(paras) 
        elif name=='queryCompanyAcctDetails':
            ret=queryCompanyAcctDetails(paras)
        elif name=='queryCompanyAcct':
            ret=queryCompanyAcct(paras)
        elif name=='companyCreditHandsel':
            ret=companyCreditHandsel(paras)    
        elif name=='userCreditHandsel':
            ret=userCreditHandsel(paras)
        elif name=='companyCreditTransfer':
            ret=companyCreditTransfer(paras)
        elif name=='shakeLogin':
            ret=shakeLogin(paras)
        elif name=='queryLogin':
            ret=queryLogin(paras)
        elif name=='getOrUpdateNickName':
            ret=getOrUpdateNickName(paras)
        elif name=='getOrSetSound':
            ret=getOrSetSound(paras)
        elif name=='uploadPhonebook':
            ret=uploadPhonebook(paras)  
        elif name=='queryContacts':
            ret=queryContacts(paras) 
        elif name=='queryPhonebook':
            ret=queryPhonebook(paras)
        elif name=='queryPackage':
            ret=queryPackage(paras)
        elif name=='shakeQueryCredit':
            ret=shakeQueryCredit(paras)
        elif name=='queryCreditAccess':
            ret=queryCreditAccess(paras)
        elif name=='querCreditSum':
            ret=querCreditSum(paras)
        elif name=='shakeCreditRanking':
            ret= shakeCreditRanking(paras)
        elif name=='shakeQueryMyAssets':
            ret=shakeQueryMyAssets(paras)
        elif name=='prefixQuery':
            ret=prefixQuery(paras)
        elif name=='queryOrUpdateUserExtend':
            ret=queryOrUpdateUserExtend(paras)
        elif name=='queryActivityIsWin':   
            ret=queryActivityIsWin(paras) 
        elif name=='queryAcctPeriod':
            ret=queryAcctPeriod(paras)
        elif name=='shakeLoginPassword':
            ret=shakeLoginPassword(paras)
        elif name=='shakeCreditExchange':
            ret=shakeCreditExchange(paras) 
        elif name=='shakeRegester':
            ret=shakeRegester(paras)
        elif name=='drawCreditExchange':
            ret=drawCreditExchange(paras) 
        elif name=='queryCreditPrize':
            ret=queryCreditPrize(paras) 
        elif name=='queryCreditPrizeDetails':
            ret=queryCreditPrizeDetails(paras) 
        elif name=='queryExchangeList':
            ret=queryExchangeList(paras) 
        elif name=='queryRechargeList':
            ret=queryRechargeList(paras)
        elif name=='rechargeCredit':
            ret=rechargeCredit(paras)
        elif name=='creditHandles':
            ret=creditHandles(paras)
        elif name=='receiveHandlesCredit':
            ret=receiveHandlesCredit(paras)
        elif name=='receiveHandlesCredit2':
            ret=receiveHandlesCredit2(paras)
        elif name=='queryCreditHandlesInfo':
            ret=queryCreditHandlesInfo(paras)
        elif name=='queryOrderProductlist':
            ret=queryOrderProductlist(paras)
        elif name=='orderProduct':
            ret=orderProduct(paras)
        elif name=='queryNmCompOrderStatus':
            ret=queryNmCompOrderStatus(paras)
        elif name=='queryBuyProductlist':
            ret=queryBuyProductlist(paras)
        elif name=='buyProduct':
            ret=buyProduct(paras)
        elif name=='querySelectionProducts':
            ret=querySelectionProducts(paras)
        elif name=='queryBuyProductInfo':
            ret=queryBuyProductInfo(paras)
        elif name=='queryLikeProducts':
            ret=queryLikeProducts(paras)
        elif name=='queryBuyHistory':
            ret=queryBuyHistory(paras)
        elif name=='queryA5AdvertList':
            ret=queryA5AdvertList(paras)
        elif name=='queryA5NewActivityList':
            ret=queryA5NewActivityList(paras)
        elif name=='queryA5InviteInfo':
            ret=queryA5InviteInfo(paras)
        elif name=='queryInviteCode':
            ret=queryInviteCode(paras) 
        elif name=='queryLikeProducts_new':
            ret=queryLikeProducts_new(paras)
        elif name=='userCreditChange':
            ret=userCreditChange(paras)
        elif name=='queryPersonCreditExchangeResult':
            ret=queryPersonCreditExchangeResult(paras)
        elif name=='sendSms':
            ret=sendSms(paras) 
        elif name=='queryTopicSolution':
            ret=queryTopicSolution(paras)
        elif name=='shakeDrawCount':
            ret=shakeDrawCount(paras)
        elif name=='activityLabel':
            ret=activityLabel(paras) 
        elif name=='activityDetail':
            ret=activityDetail(paras) 
        elif name=='appActivityList':
            ret=appActivityList(paras)
        elif name=='appDownSuccessNotify':
            ret=appDownSuccessNotify(paras)
        elif name=='querySignMonopolyService':
            ret=querySignMonopolyService(paras)
        elif name=='signMonopolyService':
            ret=signMonopolyService(paras) 
        elif name=='shakeMonopolyService':
            ret=shakeMonopolyService(paras)  
        elif name=='queryBrpInfo':
            ret=queryBrpInfo(paras)
        elif name=='queryExcDetails':
            ret=queryExcDetails(paras) 
        elif name=='exchangeCodeGiveCredit':
            ret=exchangeCodeGiveCredit(paras)
        elif name=='queryScoopInInfo':
            ret=queryScoopInInfo(paras)
        elif name=='orderScoopInProduct':
            ret=orderScoopInProduct(paras)
        elif name=='queryMonthGameActWinScratch':
            ret=queryMonthGameActWinScratch(paras) 
        elif name=='scrathDraw':
            ret=scrathDraw(paras)
        elif name=='queryLuckyTimes':
            ret=queryLuckyTimes(paras)
        elif name=='luckyDraw':
            ret=luckyDraw(paras) 
        elif name=='addUserGuess':
            ret=addUserGuess(paras)
        elif name=='queryGuessActivity':
            ret=queryGuessActivity(paras)
        elif name=='queryGuess':
            ret=queryGuess(paras)
        elif name=='companyGuessActivityRegister':
            ret=companyGuessActivityRegister(paras)
        elif name=='addOrUpdateCompanyGuess':
            ret=addOrUpdateCompanyGuess(paras)
        elif name=='queryUserGuessList':
            ret=queryUserGuessList(paras)
                     
        elif name=='checkdata':
            ret=checkdata(paras)
        elif name=='initdata':
            ret=initdata(paras)
        elif name=='initdata_nm':
            ret=initdata_nm(paras)
        elif name=='checkdata_nm':
            ret=checkdata_nm(paras)
        elif name=='initdata_gd':
            ret=initdata_gd(paras)
        elif name=='fresh_mem':
            ret=fresh_mem(paras)
        elif name=='delay':
            ret=delay(paras)
       
        if  ret==0:
            ws.write(li, 1, 'OK',style0)
        elif ret==1:
            ws.write(li, 1, 'FAIL',style1) 
        ret=10              
    #newWb.save(xlsfile)
    return


def public(paras,paras1,OPR):
    global Succeed_Count
    global Failed_Count
    filestr =open(basedir+'\\template'+'\\'+'publicbody1.xml','r').readlines()
    body=''
    for tmp1 in filestr:
        body+=tmp1;
    body=body.replace('{0}',paras[0]) 
    #body+='<Operate>{01}</Operate>'
    body=body.replace('{01}',OPR)
    body=body+' '+'\n'
    #body+='<Params>'
    #body=body+' '+'\n'
    for i in range(int(paras[1])):
        tmp2='<Property name="{elements}">{parameters}</Property>'
        body+=tmp2
        body=body.replace('{elements}',paras1[i])
        body=body.replace('{parameters}',paras[int(i)+2])
        body=body+' '+'\n'
    filestr3 =open(basedir+'\\template'+'\\'+'publicbody3.xml','r').readlines()
    for tmp3 in filestr3:
        body+=tmp3;
    #print body  
    client = httplib.HTTPConnection(css_host)
    body=str(body).encode('utf8')
    logdetail('the request is:%s'%body)
    client.request("POST",ss_url,body)
    response=client.getresponse().read()
    logdetail('the response detail is:%s'%response)
    #print response
    index1=response.find('<hRet>')
    index2=response.find('</hRet>')
    rtncode=response[index1+6:index2]
    indx3=response.find('<ResultTotal>')
    indx4=response.find('</ResultTotal>')

    if indx3==-1:
        total=0
    else:
        total=response[indx3+13:indx4]
   
    if (rtncode==paras[int(paras[1])+2])&(int(total)>=int(paras[int(paras[1])+3])):
        paras.append(rtncode)
        paras.append(int(total))
        Succeed_Count+=1
        paras.append('sucessful')

        print str(paras).decode('raw_unicode_escape')
                          
        log(str(paras).decode('raw_unicode_escape'))
        return 0
    else:
        paras.append(rtncode)
        paras.append(int(total))
        paras.append('failed')
        #print paras
        print str(paras).decode('raw_unicode_escape')
        Failed_Count+=1
        log(str(paras).decode('raw_unicode_escape'))
        return 1
    return 
    client.close()

def shakeDraw(paras):
    paras1 =['msisdn','othersMsisdn']
    public(paras,paras1,OPR)
    
def tigerDraw(paras):
    paras1 =['msisdn','consumeCredit','times']
    public(paras,paras1,OPR)
    
def queryProducts(paras):
    paras1 =['catalog_type','type','product_type']
    public(paras,paras1,OPR)

def queryUserAcct(paras):
    paras1 =['msisdn']
    public(paras,paras1,OPR)

def queryUserAcctDetails(paras):
    paras1 =['msisdn','account_no','account_period','page_number']
    public(paras,paras1,OPR)        

def queryCompanyAcctDetails(paras):
    paras1 =['company_code','account_no','start_time','end_time','page_number','access_type','order_type']
    public(paras,paras1,OPR)  
    
def queryCompanyAcct(paras):
    paras1 =['company_code','acct_type']
    public(paras,paras1,OPR)  
    
def companyCreditHandsel(paras):
    paras1 =['company_code','credit','description','msisdn','oper_time']
    public(paras,paras1,OPR)  
    
def userCreditHandsel(paras):
    paras1 =['org_msisdn','dest_msisdn','credit','description','oper_time','transactionID']
    public(paras,paras1,OPR)  
    
def companyCreditTransfer(paras):
    paras1 =['org_company_code','credit','dest_company_code','description','transactionID']
    public(paras,paras1,OPR)  
    
def shakeLogin(paras):
    paras1 =['msisdn','inviteCode','type','imei']
    public(paras,paras1,OPR)  
    
def queryLogin(paras):
    paras1 =['msisdn','imei']
    public(paras,paras1,OPR)   
    
def getOrUpdateNickName(paras):
    paras1 =['msisdn','nickName']
    public(paras,paras1,OPR) 
    
def getOrSetSound(paras):
    paras1 =['msisdn','type','isSound']
    public(paras,paras1,OPR) 
    
def uploadPhonebook(paras):
    paras1 =['msisdn','friendMsisdns','imei','isfresh']
    public(paras,paras1,OPR)  
    
def queryContacts(paras):
    OPR='queryContacts'
    paras1 =['msisdn']
    public(paras,paras1,OPR)  
    
def queryPhonebook(paras):
    paras1 =['msisdn','type','accountTypeID']
    public(paras,paras1,OPR) 
    
def queryPackage(paras):
    paras1 =['msisdn']
    public(paras,paras1,OPR) 
    
def shakeQueryCredit(paras):
    paras1 =['msisdn']
    public(paras,paras1,OPR) 
    
def queryCreditAccess(paras):
    OPR='queryCreditAccess'
    paras1 =['msisdn','startTime','endTime','from','to']
    public(paras,paras1,OPR) 
    
def querCreditSum(paras):
    OPR='querCreditSum'
    paras1 =['msisdn','accountTypeID','startTime','endTime']
    public(paras,paras1,OPR) 
    
def shakeCreditRanking(paras):
    paras1 =['msisdn']
    public(paras,paras1,OPR) 
    
def shakeQueryMyAssets(paras):
    paras1 =['msisdn']
    public(paras,paras1,OPR) 
    
def prefixQuery(paras):
    paras1 =['msisdn']
    public(paras,paras1,OPR) 
    
def queryOrUpdateUserExtend(paras):
    paras1 =['msisdn','assetsVisible','birthday']
    public(paras,paras1,OPR) 
    
def queryActivityIsWin(paras):
    paras1 =['msisdn','activityId']
    public(paras,paras1,OPR) 
    
def queryAcctPeriod(paras):
    paras1 =['msisdn']
    public(paras,paras1,OPR) 
    
def shakeLoginPassword(paras):
    paras1 =['msisdn','password']
    public(paras,paras1,OPR) 
    
def shakeRegester(paras):
    paras1 =['msisdn','password']
    public(paras,paras1,OPR) 
    
def shakeCreditExchange(paras):
    paras1 =['msisdn','exchangeID']
    public(paras,paras1,OPR) 
    
def drawCreditExchange(paras):
    paras1 =['msisdn','exchangeID']
    public(paras,paras1,OPR) 
    
def queryCreditPrize(paras):
    OPR='queryCreditPrize'
    paras1 =['provinceID','productType','provider']
    public(paras,paras1,OPR) 
    
def queryCreditPrizeDetails(paras):
    OPR='queryCreditPrizeDetails'
    paras1 =['productID']
    public(paras,paras1,OPR) 
    
def queryExchangeList(paras):
    paras1 =['msisdn','product_area']
    public(paras,paras1,OPR) 
    
def mobileFeeExchange(paras):
    paras1 =['','','','','']
    public(paras,paras1,OPR) 
    
def queryA5MobileFeeExcRecord(paras):
    paras1 =['','','','','']
    public(paras,paras1,OPR) 
    
def queryRechargeList(paras):
    paras1 =['provinceID','isByChannel']
    public(paras,paras1,OPR) 
    
def rechargeCredit(paras):
    paras1 =['msisdn','productID']
    public(paras,paras1,OPR) 
    
def creditHandles(paras):
    paras1 =['msisdn','loginMsisdn','credit','content']
    public(paras,paras1,OPR) 
    
def receiveHandlesCredit(paras):
    paras1 =['msisdn']
    public(paras,paras1,OPR) 
    
def receiveHandlesCredit2(paras):
    paras1 =['loginMsisdn','msisdn','handselResult']
    public(paras,paras1,OPR) 
    
def queryCreditHandlesInfo(paras):
    paras1 =['msisdn','msisdnType','handselType']
    public(paras,paras1,OPR) 
    
def queryOrderProductlist(paras):
    OPR='queryOrderProductlist'
    paras1 =['status']
    public(paras,paras1,OPR) 
    
def orderProduct(paras):
    paras1 =['msisdn','productID']
    public(paras,paras1,OPR) 
    
def queryNmCompOrderStatus(paras):
    paras1 =['msisdn','productID']
    public(paras,paras1,OPR) 
    
def queryBuyProductlist(paras):
    OPR='queryBuyProductlist'
    paras1 =['provinceID','status']
    public(paras,paras1,OPR) 
    
def buyProduct(paras):
    paras1 =['msisdn','productID']
    public(paras,paras1,OPR) 
    
def querySelectionProducts(paras):
    paras1 =['provinceID','status','type']
    public(paras,paras1,OPR) 
    
def queryBuyProductInfo(paras):
    paras1 =['productID']
    public(paras,paras1,OPR)
    
def queryLikeProducts(paras):
    paras1 =['status','type']
    public(paras,paras1,OPR) 
    
def queryBuyHistory(paras):
    paras1 =['msisdn']
    public(paras,paras1,OPR) 
    
def queryA5AdvertList(paras):
    paras1 =['ad_type']
    public(paras,paras1,OPR) 
    
def queryA5NewActivityList(paras):
    OPR='queryA5NewActivityList'
    paras1 =['']
    public(paras,paras1,OPR) 
    
def queryA5InviteInfo(paras):
    paras1 =['msisdn']
    public(paras,paras1,OPR) 
    
def queryInviteCode(paras):
    OPR='queryInviteCode'
    paras1 =['msisdn']
    public(paras,paras1,OPR) 
    
def queryLikeProducts_new(paras):
    paras1 =['status','type']
    public(paras,paras1,OPR)
    
def userCreditChange(paras):
    paras1 =['fMsisdn','credit','type','operTypeID','transactionID']
    public(paras,paras1,OPR)
    
def queryPersonCreditExchangeResult(paras):
    paras1 =['msisdn','start_time','end_time','page_number','order_type','start_id','current_page']
    public(paras,paras1,OPR)

def sendSms(paras):
    paras1 =['msisdn','content']
    public(paras,paras1,OPR)

def queryTopicSolution(paras):
    paras1 =['omepag','topicType','activityId']
    public(paras,paras1,OPR)
    
def shakeDrawCount(paras):
    paras1 =['msisdn','othersMsisdn']
    public(paras,paras1,OPR)
    
def activityLabel(paras):
    paras1 =['']
    public(paras,paras1,OPR)
    
def activityDetail(paras):
    paras1 =['appId']
    public(paras,paras1,OPR)

def appActivityList(paras):
    paras1 =['msisdn','provinceID','category','sortBy','keyWord']
    public(paras,paras1,OPR)
    
def appDownSuccessNotify(paras):
    paras1 =['msisdn','appId','operType']
    public(paras,paras1,OPR)
    
def querySignMonopolyService(paras):
    paras1 =['msisdn']
    public(paras,paras1,OPR)
    
def signMonopolyService(paras):
    paras1 =['msisdn','signType']
    public(paras,paras1,OPR)

def shakeMonopolyService(paras):
    paras1 =['msisdn','signId','pointId']
    public(paras,paras1,OPR)    

def queryBrpInfo(paras):
    paras1 =['exchangeID']
    public(paras,paras1,OPR) 
    
def queryExcDetails(paras):
    paras1 =['msisdn','startId','pageNum']
    public(paras,paras1,OPR)   

def exchangeCodeGiveCredit(paras):
    paras1 =['exchange_code','msisdn','activityCode']
    public(paras,paras1,OPR) 
    
def queryScoopInInfo(paras):
    paras1 =['actId','mobile']
    public(paras,paras1,OPR)   
    
def orderScoopInProduct(paras):
    paras1 =['actId','orderNum','mobile']
    public(paras,paras1,OPR) 
    
def queryMonthGameActWinScratch(paras):
    paras1 =['msisdn']
    public(paras,paras1,OPR)
    
def scrathDraw(paras):
    paras1 =['msisdn']
    public(paras,paras1,OPR)
    
def queryLuckyTimes(paras):
    paras1 =['msisdn']
    public(paras,paras1,OPR)
    
def luckyDraw(paras):
    paras1 =['msisdn']
    public(paras,paras1,OPR)

def addUserGuess(paras):
    paras1 =['msisdn','credit','input','totalCredit','optionId','optionValue','guessId','activityId']
    public(paras,paras1,OPR)

def queryGuessActivity(paras):
    paras1 =['activityCode','page_number','current_page']
    public(paras,paras1,OPR)
    
def queryGuess(paras):
    paras1 =['guessId','mobile']
    public(paras,paras1,OPR)
    
def companyGuessActivityRegister(paras):
    paras1 =['activity_class','activity_detail']
    public(paras,paras1,OPR)

def addOrUpdateCompanyGuess(paras):
    paras1 =['activity_code','guess_detail']
    public(paras,paras1,OPR)  
    
def queryUserGuessList(paras):
    paras1 =['msisdn','page_number','current_page']
    public(paras,paras1,OPR)
  
def zdh():
    print 'input start'
    casefile = basedir+'\\testdata.xls'
 
    xls = xlrd.open_workbook(casefile)

    sheet = xls.sheet_by_name('Total')
  

    for li in range( 1, sheet.nrows ):
        
        flag = sheet.cell( li, 1 ).value
        interface=sheet.cell( li, 0 ).value
        index =sheet.cell( li, 2).value
        if  flag=='Y':
            driver(casefile,interface,index)
            #print 'NOT RUN'  

    print 'The toal case is:%d,The succed case is:%d,The failed case is:%d' %(Failed_Count+Succeed_Count,Succeed_Count,Failed_Count)
     
    return


if __name__ == "__main__":
    #log file
    starttime=time.time()
    logfile = basedir+'\\log'+'\\log'+time.strftime('%Y%m%d%H%M%S',time.localtime(starttime))+'.txt'
    logdetailfile = logdir+'\\logdetail'+time.strftime('%Y%m%d%H%M%S',time.localtime(starttime))+'.txt'

    
    
    #execute process
    zdh();
    
    #close db conn

    sys.exit()
    
