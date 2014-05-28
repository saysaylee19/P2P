import SocketServer
import socket
import threading
import sys
import os
import shlex
import copy
HOST, PORT = '', 7734

count = 0
class RFCList:  #List of Available RFCS
    def __init__(self, rfcno=-1,rfcTitle=None):
        self.rfcno = rfcno
        self.rfcTitle = rfcTitle
        
    def __str__(self):
        return str(self.rfcno) + ' ' + str(self.rfcTitle)

    def getrfcno(self):
        return self.rfcno
#Creating O=Index and Peer Lists
pl=list()
y=list()
il=list()
rl=list()
#Initialiizing Lock
x_lock = threading.Lock()

#Temporary Methods to Populate pl and il for testing
def createPeerList():
    pl.append(PeerRecord('localhost', 123, 1))
    pl.append(PeerRecord('localhost', 234, 1))
    pl.append(PeerRecord('localhost', 345, 1))
    pl.append(PeerRecord('localhost', 456, 2))
    pl.append(PeerRecord('localhost', 567, 2))
    pl.append(PeerRecord('unique',999,3))

def createIndexList():
    il.append(IndexRecord(1, 'first','localhost', 1))
    il.append(IndexRecord(2, 'second','localhost', 1))
    il.append(IndexRecord(3, 'third','localhost', 1))
    il.append(IndexRecord(2, 'second','localhost', 2))
    il.append(IndexRecord(3, 'third','localhost', 2))
    il.append(IndexRecord(4,'fourth','unique',3))

#Method to List all the RFC's available at the Server    
def listAll():
    global statusCode
    statusCode=0
    global statusPhrase
    statusPhrase=''
    #createPeerList();
    
    #for i in pl:
        #print i
    
    temp=list() 
    
    if not il:
        #print "in if"
        statusCode=404
        statusPhrase='BAD REQUEST'
    else:
        #print "In else"
        for pr in il:
            temp.append(IndexRecord(pr.rfcno,pr.rfcTitle,pr.peerHostname,pr.peerid))
            statusCode=200
            #print statusCode
            statusPhrase='OK'
            #print statusPhrase
    return temp,statusCode,statusPhrase

#def checkStatusCode():
    

def lookup(rfc):
    #print "Inlookup"
    #print rfc
    temp=list()
    #createPeerList()
    #peerid = rfc
    #print peerid
    
    for pr in il:
        #print "In for loop"
        #print pr.peerid
        if int(pr.rfcno) == int(rfc):
            #print "match"
            #print pr.peerHostname
            #print pr.peerPortNo
            #print pr.peerid
            temp.append(IndexRecord(pr.rfcno,pr.rfcTitle,pr.peerHostname,pr.peerid))
            statusCode=200
            statusPhrase='OK'
        else:
            statusCode=404
            statusPhrase='FILE_NOT_FOUND'  
              
    #for i in temp:
    return temp,statusCode,statusPhrase
    
def AddPeertoList(self,req):
    #print "In Add Peer"
    global count
    count=count+1
    #print count
    
    #print "Printinggg"
    reqlist=shlex.split(req)
    #print reqlist
    
    #print reqlist[6]
    temp=list()
    even=list()
    odd=list()
    #rfclist=shlex.split(reqlist[7])
    rfclist=str(req).rsplit(':',1)
    #y = rfclist[1]
    y=shlex.split(rfclist[1])
    
    #print "Printing",y
    
    #for i,j in zip(y[::2],y[1::2]):
        #print "y u do dis",i
        #temp.append(i)
        #il.insert(0,IndexRecord())
    #print "Printttiiinngggg"    
    #for i in temp:
        #print i
   
    with x_lock:
        
        pl.insert(0,PeerRecord(reqlist[3],reqlist[5],count))
        for i,j in zip(y[::2],y[1::2]):
            il.insert(0,IndexRecord(i,j,reqlist[3],count))
    return count        
        
    #print "Releasing lock"
    #for pr in il:
        #print pr
    #for pr in pl:
        #print prxs        
    
def RemovePeerfromList(self,reqlist,count):
    #print "Tesing"
    #print self.server_address
    global peerhost
    templ=list()
    temil=list()
    phostname=reqlist[3]
    peerport=reqlist[5]
    
    
    for pr in pl:
        if pr.peerPortNo==peerport:
            #print 'match'
            peerhost=pr.peerHostname
            #print "Peer hostname is",peerhost
            idx2=[x for x,y in enumerate(il) if y.peerHostname==str(peerhost)]
            #print "Index in il is",idx2
            for i in sorted(idx2, reverse=True):
                #print il[i]
                del il[i]
    #print "Index entry deleted"    
    
    
    idx=[x for x,y in enumerate(pl) if y.peerPortNo==peerport]
    #print "Index is",idx
    for i in idx:
        del pl[i]
    #print "Peer deleted"
    
    
  

def addRFCtoIndex(rfc,reqlist,count):
    #print "In add"
    #createIndexList()
    #for pr in il:
        #print pr
    #addtemp=[rfc,'new','localhost',1]
    #print reqlist
    #print "----------"
    with x_lock:
        il.insert(0,IndexRecord(rfc,reqlist[8],reqlist[4],count))
        for pr in il:
            #print pr
            statusCode=200
            statusPhrase='OK'
    #print "----------"
    return il,statusCode,statusPhrase

def handlePeer(self,req):
    #print "In handle peer"
    #count=0
    global count
    print "******************************"
    print "Request recieved from Client :"
    print req
    print "******************************"
    reqlist=shlex.split(req)
    if reqlist[0] == 'REGISTER':
        count=AddPeertoList(self,req)
        regres="Thank u for registering"
        self.request.send(regres)
    elif reqlist[0] == 'LIST_ALL':
        reply,statusCode,statusPhrase=listAll()
        response="P2P-CI/1.0 "+str(statusCode)+" "+ str(statusPhrase)+"\n"
        for i in reply:
            #print i
            replylist=shlex.split(str(i))
            #print replylist[0],replylist[1],replylist[2]
            response=response+str(replylist[0])+" "+replylist[1]+" "+replylist[2]+" "+str(replylist[3])+"\n"
        #print response
            #print "------------"
        self.request.send(response)
    elif reqlist[0] == 'LOOKUP':
        reply,statusCode,statusPhrase=lookup(reqlist[1])
        response="P2P-CI/1.0 "+str(statusCode)+" "+ str(statusPhrase)+"\n"
        for i in reply:
            replylist=shlex.split(str(i))
            response=response+str(replylist[0])+" "+replylist[1]+" "+replylist[2]+" "+str(replylist[3])+"\n"
        self.request.send(response) 
    elif reqlist[0] == 'ADD':
        reply,statusCode,statusPhrase=addRFCtoIndex(reqlist[1],reqlist,count)
        #print "==========="
        lines=req.splitlines()
        #print lines[3]
        title=lines[3].split(":")
        #print title
        #print "============"
        response="P2P-CI/1.0 "+str(statusCode)+" "+ str(statusPhrase)+"\n"
        response=response+"RFC "+reqlist[1]+" "+title[1]+" "+reqlist[4]+" "+reqlist[6]
        self.request.send(response)
        #for i in reply:
            #self.request.send(str(i))
    elif reqlist[0] == 'DEREGISTER':
        RemovePeerfromList(self,reqlist,count)
        dereg="Buh Bye!!" 
        self.request.send(dereg)   
        self.request.close()
    #RemovePeerfromList(self)
        #print "This Client exited:{}".format(self.client_address[0])    
            

class IndexRecord:  #List of Available RFCS
    def __init__(self, rfcno=-1, rfcTitle='None', peerHostname='None', peerid=-1):
        self.rfcno = rfcno
        self.rfcTitle = rfcTitle
        self.peerHostname = peerHostname
        self.peerid = peerid

    def __str__(self):
        return str(self.rfcno) + ' ' + str(self.rfcTitle) + ' ' + str(self.peerHostname) + ' ' + str(self.peerid)

    def getpeerid(self):
        return self.peerid

class PeerRecord:   #List of Active Peers
    def __init__(self, peerHostname='None',peerPortNo=10000, peerid=-1):
        self.peerHostname = peerHostname
        self.peerPortNo = peerPortNo
        self.peerid = peerid

    def __str__(self):
        return str(self.peerHostname) + ' ' + str(self.peerPortNo) + ' ' + str(self.peerid)

    def getpeerid(self):
        return self.peerid    

class NewTCPHandler(SocketServer.BaseRequestHandler):
    "One instance per connection.  Override handle(self) to customize action."
    def handle(self):
        #print "In handle()"
        data=self.request.recv(1024)
        #print "here"
        cur_thread=threading.current_thread()
        reply="{}:{}".format(cur_thread.name,data)
        handlePeer(self,data)
        #print reply thread numbers        

class Server(SocketServer.ThreadingMixIn,SocketServer.TCPServer):
    daemon_threads=True
    allow_reuse_address=True
    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)
        #print "Keep listening baba"
        
'''class mThread(threading.Thread):
    def __init__(self,tID,name,count):
        threading.Thread.__init__(self)
        self.tID=tID
        self.name=name
        self.count=count
    def run(self):
        #print "Starting "+self.name
        m_server(self)
        #print "Exiting "+self.name
'''


if __name__ == "__main__": 
    HOST,PORT=raw_input("Enter the IP address and Port").split(" ")
    
    server=Server((HOST,int(PORT)),NewTCPHandler)
    ip,port=server.server_address
    try:
        print "Server Listening on",ip,port
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
    
