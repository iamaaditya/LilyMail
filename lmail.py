import sys, shelve, getpass, string, email
import smtplib, poplib
from email import parser
from re import *


pat=compile('([A-Z]*[a-z]*[0-9]*)+@([A-Z]*[a-z]*[0-9]*)+.([A-Z]*[a-z]*[0-9]*)')


def ask(question):
	print "\r%s" %question,
	return sys.stdin.readline().strip()

def isGoodEmail(addr):
	return pat.search(addr)

def getUser():
	user=ask('Your email address: ')
	if isGoodEmail(user): 
		return user
	else:
		print 'Invalid email address, try again:'
		return getUser()

def getReceiver():
	receiver=ask('To: ')
	if isGoodEmail(receiver): 
		return receiver
	else:
		print 'Invalid email address, try again:'
		return getReceiver()

def getSubject():
	subject=ask('Subject: ')
	if len(subject)>0: return subject
	else:
		ans= ask('Proceed without subject?(Y/N) ')
		if ans=='N' or ans=='n':return getSubject()
		else: return '[No subject]'

def getPassword(user):
	password= getpass.getpass('enter password for account %s: '%user)
	return password

def sendMail(sender,receiver,subject,text,pwd):
	msgBody = string.join((
        	"From: %s" % sender,
        	"To: %s" % receiver,
       		 "Subject: %s" % subject ,
       		 "",
       		 text
      		  ), "\r\n")
	user=sender[0:sender.find('@')] #get string before '@'
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(user,pwd)
	server.sendmail(sender, receiver, msgBody)
	server.quit()

def connect(uid,pwd):
	print 'Connecting...'
	pop_conn=poplib.POP3_SSL('pop.gmail.com')
	pop_conn.user(userid)
	pop_conn.pass_(password)
	print pop_conn.getwelcome()
	return pop_conn

def composeMail(sender,password):
	print 'composing a new message...'
	sender=userid
	receiver=getReceiver()
	subject=getSubject()
	message=ask('Message: ')
	ans= ask('Ready to send?(Y/N)')
	if ans=='Y' or ans=='y':
		print 'sending...'
		sendMail(sender,receiver,subject,message,password)
		print 'email sent to ',receiver,' successfully!'
	else:
		print 'Message abandoned'


def extractMessageBody(msg):
	for part in msg.walk():
		if part.get_content_type()=='text/plain':
			return part.get_payload()

def getInsideAction(messages):
	global userid,password
	action=ask('command: ')
	if action=='ls':
		print 'Messages in Inbox:'
		i=0
		while i<len(messages): 
			print '[',i+1,'] :',messages[i]['subject']
			i=i+1
		getInsideAction(messages)
	elif action=='quit':	
		#pop_conn.quit()
		userid='' #clear the data
		password=''
		print 'You are logged out'
		print '[Options: login, quit...]\n'
		getAction()
	elif action=='new':
		composeMail(userid,password)
		getInsideAction(messages)
	elif action=='open':
		index=int(ask("please specify the mail number: "))
		#print index
		print extractMessageBody(messages[index-1])
		getInsideAction(messages)
	elif action=='help':
		print '[quit] exit login \n [new] compose new email\n [ls] list out mails in mailbox\n [open] open an email'
		getInsideAction(messages)
	else:
		print 'invalid command'
		getInsideAction(messages)

def readMail(pop_conn):
	#get msg from server
	msgs= [pop_conn.retr(i) for i in range(1,len(pop_conn.list()[1])+1)  ]
	msgs=['\n'.join(m[1]) for m in msgs]
	msgs= [parser.Parser().parsestr(m) for m in msgs]
	pop_conn.quit() #maybe later?
	return msgs


def login():
	global userid, password  #### maybe global is not a good solution?
	userid=getUser()
	password=getPassword(userid)
	connection = connect(userid,password)

	messages=readMail(connection)
	print '[Options: ls, open, new, quit...]\n'
	getInsideAction(messages)



def getAction():
	action=ask('command: ')
	if action=='quit':
		sys.exit(0)
	elif action=='login':
		print 'Please verify your identity '
		login()
	elif action=='help':
		print '[login] start a login session\n [quit] exit program'	
	else:
		print 'invalid command'

if __name__=='__main__':
	print '\nLilyMail'
	print '[Options: login, quit...]\n'
	userid=''
	password=''
	while True:
		getAction()

