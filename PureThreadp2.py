#Peer 2
import SocketServer
import socket
import threading
import sys
import os
import shlex
import subprocess
import Queue

HOST, PORT = 'peer2', 8888
port='8888'

rlist=list()
rfctitle=list()
o=list()

status=1
class RFCList:  #List of Available RFCS
    def __init__(self, rfcno=-1,rfcTitle='None'):
        self.rfcno = rfcno
        self.rfcTitle = rfcTitle
        
    def __str__(self):
        return str(self.rfcno) + ' ' + str(self.rfcTitle)

    def getrfcno(self):
        return self.rfcno

        
def requestRFC(msg,RFC_NO,PeerHname,PeerPort):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((PeerHname,int(PeerPort)))
        print "Client connected"
        s.send(msg)
        reply = s.recv(1024)  # limit reply to 16K
        m='1'
        s.send(m)
        exist=shlex.split(reply)
        fname=RFC_NO+".pdf"
        #fname=RFC_NO+".txt"
        if str(exist[1])=='200':
            f=open("/Users/sayleemhatre/Desktop/IPFINAL/P2P/rfc/"+fname,'wb')
            #l=s.recv(1024)
            while True:
                l=s.recv(1024)
                if l:
                    f.write(l)
                    #print "Recieving: {}".format(l)
                    #l=s.recv(1024)
                    break
                else:
                    f.close()
                    break
            #updateRFC(RFC_NO,RFC_TITLE)            
            #print "Data recieved"
        else:
            print "Is this the File not found"
        #print "Data Got it bro"
        s.close()
        
 
def updateRFC(RFC_NO,RFC_TITLE):
    #listrfc=shlex.split(msg)
    rlist.insert(0,RFCList(RFC_NO,RFC_TITLE))
    
def listalllre():
    #os.chdir("/mydir")
    for files in os.listdir("."):
        if files.endswith(".txt"):
            x=files.split('.',1)
            #print x
            o.append(x[0])
            
    #print o       
           
               

def createList():
    c1=['ls','-lrt']
    c2=['grep','-v','.py']
    c3=['tr','-s','" "']
    c4=['awk','{print $9}']
    #c5=['awk','BEGIN {FS="."}','{print $1}']
    c5=['cut','-d','.','-f1']
    p1=subprocess.Popen(c1,stdout=subprocess.PIPE)
    p2=subprocess.Popen(c2,stdin=p1.stdout,stdout=subprocess.PIPE)
    p3=subprocess.Popen(c3,stdin=p2.stdout,stdout=subprocess.PIPE)
    p4=subprocess.Popen(c4,stdin=p3.stdout,stdout=subprocess.PIPE)
    p5=subprocess.Popen(c5,stdin=p4.stdout,stdout=subprocess.PIPE)
    p4.stdout.close()
    op=p5.communicate()
    #print op
    op=str(op).strip()
    #print op
    
    for i in op:
        if i is not None:
            rlist.append(str(i))       
    #for i in rlist:
        #print i        
            

def giveFile(self):
    reque=self.recv(1024)
    print reque
    rfcno=shlex.split(reque)
    fname=rfcno[2]+".txt"
    #print "Printlin rlist contains"
        #for i in rlist:
            #print i
        
    if str(rfcno[2]) not in o:
        print "File not found"
        fdata="P2P-CI/1.0 404 FILE NOT FOUND"+"\n"
    else:
        #print "In else of give File"
        date=subprocess.check_output(['date'])
        uname=subprocess.check_output(['uname'])
        c1=['ls','-lrt']
        c2=['grep','-w',fname]
        c3=['tr','-s','" "']
        c4=['awk','{print $6,$7,$8}']
        c12=['ls','-lrt']
        c22=['grep','-w',fname]
        c32=['tr','-s','" "']
        c42=['awk','{print $5}']
        p1=subprocess.Popen(c1,stdout=subprocess.PIPE)
        p2=subprocess.Popen(c2,stdin=p1.stdout,stdout=subprocess.PIPE)
        p3=subprocess.Popen(c3,stdin=p2.stdout,stdout=subprocess.PIPE)
        p4=subprocess.Popen(c4,stdin=p3.stdout,stdout=subprocess.PIPE)
        p3.stdout.close()
        lastupddate=p4.communicate()
        print lastupddate
    
        p12=subprocess.Popen(c12,stdout=subprocess.PIPE)
        p22=subprocess.Popen(c22,stdin=p12.stdout,stdout=subprocess.PIPE)
        p32=subprocess.Popen(c32,stdin=p22.stdout,stdout=subprocess.PIPE)
        p42=subprocess.Popen(c42,stdin=p32.stdout,stdout=subprocess.PIPE)
        p32.stdout.close()
        fsize=p42.communicate()
        print fsize
        
        #lastupddate='last upddte'
        #fsize=5
        f=open(fname,'r')
        fdata="P2P-CI/1.0 200 OK"+"\n"+"Date: "+str(date)+"\n"+"OS: "+uname+"\n"+"Last-Modified: "+lastupddate[0]+"\n"+"Content-Length: "+str(fsize[0])+"\n"+"Content-Type: text/text"+"\n"
        self.send(fdata)
        
        stat=self.recv(1)
        #print "Ack recvd from peer2",stat
        
        while True:
            #print "In while"
            line=f.read(1024)
            self.send(line)
            fdata+=line
            if not len(line):
                break;
            #fdata+=line
        
        
        f.close()
        #print "Data read"
        #self.send(fdata)
    return 0
        
q = Queue.Queue()            

def m_server():
       
        s=socket.socket()
        
        ip='127.0.0.1'
        port=8888
        s.bind((ip,port))
        s.listen(5)
        
        cur_thread=threading.current_thread()
        while True:
            
            (c,addr)=s.accept()
            print 'Connected to',addr
            thread3=threading.Thread(target=giveFile(c))
            thread3.start()
            thread3.join()
            
        s.close()
        return
        
def getAllRFC():
    resp=''
    for i in rlist:
        
        replylist=shlex.split(str(i))
        resp+=replylist[0]+" "+replylist[1]+"\n"
    #allrfc = ''.join(str(e) for e in rlist)
    return resp        
        
def menu():
    #try:
        global status
        status = 1
        CIServIp,CIServPort=raw_input("Enter The Ip and port of the Centralised Server").split(" ")
        while (status==1):
            print "Menu"
            print "0.Register to Server"
            print "1.List all the available RFC's"
            print "2.Lookup for a particular item at Server"
            print "3.Add particular item at Server"
            print "4.Deregister"
            print "5.Request for RFC"
            
            i = raw_input()
            if i=='0':
                #allRFC=getAllRFC()
                msg="REGISTER P2P-CI/1.0 Host: "+HOST+" Port: "+port+"\n"
                #+" List_of_rfc: "+allRFC
                client(msg,CIServIp,CIServPort)
    
            if i=='1':
                msg="LIST_ALL P2P-CI/1.0"+"\n"+"Host: "+HOST+"\n"+" Port: "+port
                client(msg,CIServIp,CIServPort)
                
            if i=='2':
                RFC_NO=raw_input("Enter RFC number")
                TITLE="random stuff"
                msg="LOOKUP"+" "+RFC_NO+" P2P-CI/1.0"+"\n"+"Host: "+HOST+"\n"+"Port: "+port+"\n"+"Title:"+TITLE
                client(msg,CIServIp,CIServPort)
                
            if i=='3':
                RFC_NO=raw_input("Enter RFC number")
                TITLE=raw_input("Enter the title for the RFC")
                msg="ADD"+" "+RFC_NO+" P2P-CI/1.0"+"\n"+" Host: "+HOST+"\n"+" Port: "+port+"\n"+" Title: "+TITLE
                client(msg,CIServIp,CIServPort)
    
            if i=='4':
                msg="DEREGISTER P2P-CI/1.0 Host: "+HOST+" Port: "+port
                client(msg,CIServIp,CIServPort)
                status=0
                os._exit(1)
                
            if i=='5':
                RFC_NO,PeerHname,PeerPort=raw_input("Enter the RFC No,Peer Hostname and port(Space Seperated)").split(" ")
                msg="GET RFC"+" "+RFC_NO+" "+"P2P-CI/1.0"+"\n"+"Host: "+PeerHname+"\n"+"OS: Mac OS"
                requestRFC(msg,RFC_NO,PeerHname,PeerPort)
        return            
 
def client(string,CIServIp,CIServPort):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((CIServIp,int(CIServPort)))
    sock.send(string)
    reply = sock.recv(16384)  # limit reply to 16K
    print "*********************************"
    print "Response recieved from Server:"
    print reply
    print "*********************************"
    sock.close()

def main():
    #createList()
    listalllre()
    ServHost,ServPort="localhost",9998
    try:
        thread1=threading.Thread(target=m_server)
        thread2=threading.Thread(target=menu)
        thread1.daemon=True
        thread2.daemon=True
        thread1.start()
        thread2.start()
        
        thread1.join()
        thread2.join()
        
    except KeyboardInterrupt:
        sys.exit(0)


if __name__=="__main__":
	main()

peer2