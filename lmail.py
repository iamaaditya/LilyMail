import sys
import string
import smtplib
from re import *


pat=compile('([A-Z]*[a-z]*[0-9]*)+@([A-Z]*[a-z]*[0-9]*)+.([A-Z]*[a-z]*[0-9]*)')


def ask(question):
	print "\r%s" %question,
	return sys.stdin.readline().strip()

def isGoodEmail(addr):
	return pat.search(addr)

def getSender():
	sender=ask('From: ')
	if isGoodEmail(sender): 
		return sender
	else:
		print 'Invalid email address, try again:'
		return getSender()

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

def getMessage():
	message=ask('Message: ')
	return message

def sendMail(FROM,TO,SUBJECT,TEXT,PWD):
	BODY = string.join((
        	"From: %s" % FROM,
        	"To: %s" % TO,
       		 "Subject: %s" % SUBJECT ,
       		 "",
       		 TEXT
      		  ), "\r\n")
	USERID=FROM[0:FROM.find('@')]
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(USERID,PWD)
	server.sendmail(FROM, TO, BODY)
	server.quit()
	#do sth here

def writeMail():
	sender=getSender()
	receiver=getReceiver()
	subject=getSubject()
	message=getMessage()
	ans= ask('Ready to send?(Y/N)')
	if ans=='Y' or ans=='y':
		password=ask('Please provide password for account %s:'% sender)
		sendMail(sender,receiver,subject,message,password)
		print 'email sent to ',receiver,' successfully!'
		#print sender, receiver, subject,message
	else:
		print 'Message abandoned'

def getAction():
	action=ask('command: ')
	if action=='new':
		print 'composing a new email...'
		writeMail()
	elif action=='quit':
		sys.exit(0)
	elif action=='read':
		print 'under dev..'
		getAction()
	else:
		print 'invalid command'
		getAction()

if __name__=='__main__':
	print '\nLiLyMail'
	print '[avaliable options: read, new, quit..]\n'
	getAction()

