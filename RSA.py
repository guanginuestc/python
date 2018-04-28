#coding: utf-8

import math
import binascii
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class RSA():
	def __init__(self):
		'''if basep%2==0:
			basep+=1
		if baseq%2==0:
			baseq+=1
		
		self.basep=basep
		self.baseq=baseq
		'''
		self.Create_Primary()
		self.p=self.basep
		self.q=self.baseq
		self.n=self.p*self.q
		self.n1=(self.q-1)*(self.p-1)
		self.Create_e_d()
	def ex_Eulid(self,a,b):
		if a<b:
			temp=a
			a=b
			b=temp
		if b==0:
			self.x=1
			self.y=0
			self.qq=a
		else:
			self.ex_Eulid(b,a%b)
			temp=self.x
			self.x=self.y
			self.y=temp-a/b*self.y

	def Create_e_d(self):
		self.e=random.randrange(100000000000000,90000000000000000000)
		while True:
			self.ex_Eulid(self.n1,self.e)
			if self.qq==1:
				break
			else:
				self.e+=1
		if self.y<0:
			self.y+=self.n1
		self.d=self.y
		#print '\t123\t'+repr(pow(self.e*self.d,1,self.n1))
		#print self.p
		#print self.q
		#ass=pow(123,self.e,self.n)
		#print ass
		#print pow(ass,self.d,self.n)
	def Encrypt(self,message):
		return pow(message,self.d,self.n)
	def Decrypt(self,message):
		return pow(message,self.e,self.n)

	def isp(self,num):
		for i in range(50):
			a=random.randrange(2,num)
			if pow(a,num-1,num)!=1:
				return False
		return True

	def Create_Primary(self):
		self.basep=random.randrange(100000000000000,90000000000000000000)
		self.baseq=random.randrange(100000000000000,90000000000000000000)
		while self.basep==self.baseq:
			self.basep=random.randrange(100000000000000,90000000000000000000)
		print 'creating p'
		while(self.isp(self.basep)==False):
			self.basep+=1
		print 'creating q'
		while(self.isp(self.baseq)==False):
			self.baseq+=1
	
if __name__=='__main__':
	r=RSA()
	a=raw_input("input message:").decode('gbk').encode('utf8')
	#print isinstance(a,unicode)
	#a=binascii.b2a_hex(a.encode('utf8')).decode('hex')
	a=int(a)
	'''
	en_temp=[r.Encrypt(ord(x)) for x in a]
	de_temp=[r.Decrypt(x) for x in en_temp]
	en=""
	de=""
	for x in de_temp:
		de+=chr(x)
	print de
	de=binascii.a2b_hex(de).decode('utf-8')
	#print de
	for x in en_temp:
		en+=str(x)+','
	en_temp=r.Encrypt(a)
	'''
	en = r.Encrypt(a)
	de = r.Decrypt(en)
	print 'q:'+repr(r.q)
	print 'p:'+repr(r.p)
	print 'n:'+repr(r.n)
	print 'e:'+repr(r.e)
	print u'加密后的结果为:'+repr(en)
	print u'解密后的结果为:'+repr(de)
	'''
	a=ord(a)
	print a
	mm = r.Encrypt(a)
	mmm=r.Decrypt(mm)
	print mm
	print chr(mmm)
	'''