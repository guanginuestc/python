#coding: utf-8
import Tkinter as Tk
import RSA
import tkMessageBox
r=RSA.RSA()
r.forinit()
#en = r.Encrypt(a)
#de = r.Decrypt(en)
root=Tk.Tk()
root.title('RSA')
root.geometry("800x250")
root.resizable(width=True,height=True)

def en():
	try:
		temp=int(t1.get('0.0',Tk.END))
	except Exception,e:
		tkMessageBox.showinfo('ERROR', u'暂时不支持汉字加密')
		return
	en=r.Encrypt(temp)
	t2.delete('0.0',Tk.END)
	t2.insert(Tk.END,en)
    #t1.insert(Tk.END,type(int(t2.get('0.0',Tk.END))))
def de():
	temp=int(t2.get('0.0',Tk.END))
	en=r.Decrypt(temp)
	t1.delete('0.0',Tk.END)
	t1.insert(Tk.END,en)
def cl():
	t1.delete('0.0',Tk.END)
	t2.delete('0.0',Tk.END)
def set():
	q=int(q_e.get())
	if r.isp(q)==False:
		tkMessageBox.showinfo('ERROR', u'q不是素数')
		return
	p=int(p_e.get())
	if r.isp(p)==False:
		tkMessageBox.showinfo('ERROR', u'p不是素数')
		return
	e=int(e_e.get())
	n1=(q-1)*(p-1)
	r.ex_Eulid(n1,e)
	if r.qq!=1:
		tkMessageBox.showinfo('ERROR', u'e非法')
		return
	r.q=q
	r.p=p
	r.e=e
	r.n=p*q
	r.n1=n1
	if r.y<0:
		r.y+=r.n1
	r.d=r.y
	d_e.delete(0,Tk.END)
	d_e.insert(0,r.d)
def retry():
	r.forinit()
	p_e.delete(0,Tk.END)
	p_e.insert(0,r.p)
	q_e.delete(0,Tk.END)
	q_e.insert(0,r.q)
	e_e.delete(0,Tk.END)
	e_e.insert(0,r.e)
	d_e.delete(0,Tk.END)
	d_e.insert(0,r.d)
	
#print r.q
#Tk.Label(root,text='p=%s,q=%s,e=%s,n=%s,d=%s'%(r.p,r.q,r.e,r.n,r.d),font=("Arial",12)).grid(row=0,column=0,rowspan=1,columnspan=4,sticky=Tk.W)
Tk.Label(root,text='p',font=("Arial",12)).grid(row=0,column=0)
p_e=Tk.Entry(root,width=30)
p_e.insert(0,r.p)
p_e.grid(row=0,column=1)

Tk.Label(root,text='q',font=("Arial",12)).grid(row=0,column=2)
q_e=Tk.Entry(root,width=30)
q_e.insert(0,r.q)
q_e.grid(row=0,column=3)
Tk.Label(root,text='e',font=("Arial",12)).grid(row=1,column=0)
e_e=Tk.Entry(root,width=30)
e_e.insert(0,r.e)
e_e.grid(row=1,column=1)
Tk.Label(root,text='d',font=("Arial",12)).grid(row=1,column=2)
d_e=Tk.Entry(root,width=30)
d_e.insert(0,r.d)
d_e.grid(row=1,column=3)
Tk.Label(root,text=u'明文',font=("Arial",12)).grid(row=2,column=0,sticky=Tk.W)
t1=Tk.Text(root,width=100,height=5)
t1.insert(Tk.END,'')
t1.grid(row=2,column=1,columnspan=3,rowspan=1)
Tk.Label(root,text=u'密文',font=("Arial",12)).grid(row=3,sticky=Tk.W)
t2=Tk.Text(root,width=100,height=5)
t2.insert(Tk.END,'')
t2.grid(row=3,column=1,columnspan=3,rowspan=1)
Tk.Button(root, text=u"加密", command=en).grid(row=4,column=0)
Tk.Button(root, text=u"解密", command=de).grid(row=4,column=1)
Tk.Button(root, text=u"清空", command=cl).grid(row=4,column=2)
Tk.Button(root, text=u'设定p,q,e',command=set).grid(row=4,column=3,sticky=Tk.W)
Tk.Button(root,text=u'再次随机一组公私钥',command=retry).grid(row=4,column=3,sticky=Tk.E)
root.mainloop()