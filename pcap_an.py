#!/usr/bin/python
#coding: utf-8
#from __future__ import division
__author__ = 'Guang'
__date__ = "2016-12-30"

#from scapy import *

import scapy.all as scapy
import sys
import os
import gc
import getopt
import xlrd
import xlwt
'''
class icmp():
	def __init__():
		self.dict
		'icmp_time':[],#icmp时间间隔
		'icmp_last':0,#上个echorequest时间
		'icmp_success':0,#成功数据包数
		'icmp_all':0#数据包总量
'''
#import time
class pcap_a():
	def __init__(self,path_write):
		self.path_write=path_write
		self.mydict={}#dic for sheet1
		self.wb=xlwt.Workbook()
		self.ws=self.wb.add_sheet('sbluSheet')#,cell_overwrite_ok=True)
		self.ws2=self.wb.add_sheet('sheet2')#,cell_overwrite_ok=True)
		self.row_sheet2=1
		self.ws3=self.wb.add_sheet('sheet3')#,cell_overwrite_ok=True)
		self.row_sheet3 = 0
		self.ws4=self.wb.add_sheet('sheet4')
		self.row_sheet4 = 1

		self.fon=xlwt.Font()
		self.fon.name='Times New Roman'
		#self.fon.bold=True
		self.style0=xlwt.XFStyle()
		self.style0.font=self.fon

		a=u'DataSet,SrcIP,DstIP,proto,src_port,dst_port,up_pkts,dw_pkts,up_pl_pkts,dw_pl_pkts,\
		up_pl_bytes,dw_pl_bytes,duration,up_min_ipt,dw_min_ipt,up_max_ipt,dw_max_ipt,\
		up_avg_plsize,dw_avg_plsize,up_min_plsize,dw_min_plsize,up_max_plsize,dw_max_plsize,\
		up_stdev_plsize,dw_stdev_plsize,up_avg_ipt,dw_avg_ipt,up_stdev_ipt,dw_stdev_ipt,avg_ttl,up_avg_plsize/duration,num_dns,\
		上行流速率大小,下行流速率大小,TCP握手是否正常(-1-没有握手;0-正常;1-源ipSYN为1；2-目的IPSYN=1、ACK=1；3-目的IP多次回应ACK=1),\
		0-正常；1-ACK=1、URG、FIN、RST同时=1；2-SYN、FIN同时=1；3-ACK、FIN同时=1,up_rst,dw_rst'
		a=a.split(',')
		for i in range(len(a)):
			self.ws.write(0,i,a[i],self.style0)
		self.row=1
		a=u'数据集名称+IP对+对应流的个数+每条流持续时间平均值+上行载荷总量平均值+上行载荷总量是否平均+每条流持续时间是否平均+\
		上行数据包时间间隔平均值是否很小+下行数据包时间间隔平均值是否很小+上行数据\
		包时间间隔平均值是否为0+下行数据包时间间隔平均值是否为0+上行最大时间间隔是否\
		为0+下行数据包最大时间间隔是否为0+上行最大时间间隔是否一样+下行最大时间间隔\
		是否一样+上行平均时间间隔是否一样+下行平均时间间隔是否一样'
		a=a.split('+')
		for i in range(len(a)):
			self.ws2.write(0,i,a[i],self.style0)
		a='ip,success_rate,time'
		a = a.split(',')
		for i in range(len(a)):
			self.ws4.write(0,i,a[i],self.style0)
		self.wb.save(self.path_write)
		self.sheet2_dic = {}#sheet for sheet2
		self.sheet3_dic = {}#sheet for sheet3
		self.sheet4_dic = {}#sheet for sheet4


	def icmp_sheet4(self,x):
		#传入icmp数据包x,并将数据写入sheet4
		if x.payload.payload.type == 8:
			temp_key= x.payload.src+'_'+x.payload.dst
			if self.sheet4_dic.get(temp_key,False):
				#temp_key1在字典中
				self.sheet4_dic[temp_key]['icmp_time'].append(x.time-self.sheet4_dic[temp_key]['icmp_last'])
				self.sheet4_dic[temp_key]['icmp_last']=x.time
				self.sheet4_dic[temp_key]['icmp_all']+=1
			else:
				#不在字典中
				temp_add = {
				temp_key:{
				'icmp_time':[],#icmp时间间隔
				'icmp_last':x.time,#上个echorequest时间
				'icmp_success':0,#成功数据包数
				'icmp_all':1#数据包总量
				}
				}
				self.sheet4_dic.update(temp_add)
		elif x.payload.payload.type == 0:
			####
			temp_key= x.payload.dst+'_'+x.payload.src
			self.sheet4_dic[temp_key]['icmp_success']+=1
			self.sheet4_dic[temp_key]['icmp_all']+=1



	def setname(self,name):
		self.datasetname=name

	def Feature_DataSet(self,key):
		#sheet2z的code,传入参数为源目的ip对应的一系列特征
		temp_key1 = self.mydict[key]['SrcIP']+'_'+self.mydict[key]['DstIP']
		temp_key2 = self.mydict[key]['DstIP']+'_'+self.mydict[key]['SrcIP']
		if self.sheet2_dic.get(temp_key1,False):
			#s_d ip 在sheet2_dic中
			tem_key = temp_key1
		elif self.sheet2_dic.get(temp_key2,False):
			#d_s ip 在sheet2中
			tem_key = temp_key2
		else:
			#没有此键添加key:value
			key_add={
			temp_key1:{
			'num_flows':0,#流的个数
			#下几个用list？
			'up_size':[],#上载总量
			'duration':[],#流持续时间

			'up_max_ipt':[],#//上行最大时间间隔
			'dw_max_ipt':[],#//下行最大时间间隔
			'up_avg_ipt':[],#上行数据包时间间隔平均值
			'dw_avg_ipt':[],#下行数据包时间间隔平均值
			}
			}
			self.sheet2_dic.update(key_add)
			tem_key = temp_key1
		self.sheet2_dic[tem_key]['num_flows'] += 1
		self.sheet2_dic[tem_key]['up_size'].append(self.mydict[key]['up_pl_bytes'])
		self.sheet2_dic[tem_key]['duration'].append(self.mydict[key]['duration'])
		self.sheet2_dic[tem_key]['up_max_ipt'].append(self.mydict[key]['up_max_ipt'])
		self.sheet2_dic[tem_key]['dw_max_ipt'].append(self.mydict[key]['dw_max_ipt'])
		self.sheet2_dic[tem_key]['up_avg_ipt'].append(self.mydict[key]['up_avg_ipt'])
		self.sheet2_dic[tem_key]['dw_avg_ipt'].append(self.mydict[key]['dw_avg_ipt'])
		

		#sheet3资源
		if self.sheet3_dic.get(temp_key1,False):
			temp_sheet3 = temp_key1
		elif self.sheet3_dic.get(temp_key2,False):
			temp_sheet3 = temp_key2
		else:
			key_sheet3_add = {
			temp_key1:[0]#用于存放数据集名称
			}
			self.sheet3_dic.update(key_sheet3_add)
			temp_sheet3 = temp_key1
		if self.datasetname in self.sheet3_dic[temp_sheet3]:
			pass
		else:
			self.sheet3_dic[temp_sheet3].append(self.datasetname)
		self.sheet3_dic[temp_sheet3][0]+=1

	def is_avg(self,a):
		#测试是否正负0.2
		temp = 0
		if a[-1] == 0:
			return 0
		for k in range(len(a)-1):
			if (abs(a[k]-a[-1])<(a[-1]*0.8)):
				temp+=1
		if (float(temp) / (len(a)-1)) > 0.8:
			return float(temp) /(len(a)-1)
		else:
			return 0

	#计算sheet2中的特征并输出
	def com_sheet2(self):
		self.com_wr_sheet2()#数据集名
		temp = 0
		for k in self.sheet2_dic:
			self.ws2.write(self.row_sheet2,1,k)
			self.ws2.write(self.row_sheet2,2,self.sheet2_dic[k]['num_flows'])
			if self.sheet2_dic[k]['num_flows'] == 1:
				self.row_sheet2+=1
				continue
			for v in self.sheet2_dic[k]['up_size']:
				temp += v
			self.sheet2_dic[k]['up_size'].append(temp/len(self.sheet2_dic[k]['up_size']))
			self.ws2.write(self.row_sheet2,4,self.sheet2_dic[k]['up_size'][-1])
			self.sheet2_dic[k]['up_size']= self.is_avg(self.sheet2_dic[k]['up_size'])
			self.ws2.write(self.row_sheet2,5,self.sheet2_dic[k]['up_size'])

			temp=0
			for v in self.sheet2_dic[k]['duration']:
				temp += v
			self.sheet2_dic[k]['duration'].append(temp/len(self.sheet2_dic[k]['duration']))
			self.ws2.write(self.row_sheet2,3,self.sheet2_dic[k]['duration'][-1])
			self.sheet2_dic[k]['duration']=self.is_avg(self.sheet2_dic[k]['duration'])

			self.ws2.write(self.row_sheet2,6,self.sheet2_dic[k]['duration'])

			temp=0
			is_same = 1
			for v in self.sheet2_dic[k]['up_max_ipt']:
				temp+=v
			temp=temp/len(self.sheet2_dic[k]['up_max_ipt'])
			for v in self.sheet2_dic[k]['up_max_ipt']:
				if temp != v:
					is_same=0
			self.ws2.write(self.row_sheet2,13,is_same)
			if (temp == 0):
				#是0
				self.ws2.write(self.row_sheet2,11,1)
			else:
				#不小哦
				self.ws2.write(self.row_sheet2,11,0)

			temp=0
			for v in self.sheet2_dic[k]['dw_max_ipt']:
				temp+=v
			temp= temp/len(self.sheet2_dic[k]['dw_max_ipt'])
			is_same=1
			for v in self.sheet2_dic[k]['dw_max_ipt']:
				if temp != v:
					is_same = 0
			self.ws2.write(self.row_sheet2,14,is_same)
			if (temp == 0):
				#是0 说很小
				self.ws2.write(self.row_sheet2,12,1)
			else:
				#不是0
				self.ws2.write(self.row_sheet2,12,0)

			temp = 0
			for v in self.sheet2_dic[k]['up_avg_ipt']:
				temp+=v
			temp = temp/len(self.sheet2_dic[k]['up_avg_ipt'])
			is_same=1#判断是否相同
			for v in self.sheet2_dic[k]['up_avg_ipt']:
				if temp != v:
					#输出不一样啊
					is_same=0
			self.ws2.write(self.row_sheet2,15,is_same)
			if temp == 0:
				#是0
				self.ws2.write(self.row_sheet2,9,1)
				self.ws2.write(self.row_sheet2,7,1)
			elif temp<0.001:
				#很小
				self.ws2.write(self.row_sheet2,9,0)
				self.ws2.write(self.row_sheet2,7,1)
			else:
				#不小
				self.ws2.write(self.row_sheet2,9,0)
				self.ws2.write(self.row_sheet2,7,0)
			temp = 0
			is_same=1
			for v in self.sheet2_dic[k]['dw_avg_ipt']:
				temp+=v
			temp = temp/len(self.sheet2_dic[k]['dw_avg_ipt'])
			for v in self.sheet2_dic[k]['dw_avg_ipt']:
				if temp != v:
					is_same = 0
			self.ws2.write(self.row_sheet2,16,is_same)
			if temp == 0:
				#是0
				self.ws2.write(self.row_sheet2,10,1)
				self.ws2.write(self.row_sheet2,8,1)
			elif temp<0.001:
				#很小
				self.ws2.write(self.row_sheet2,10,0)
				self.ws2.write(self.row_sheet2,8,1)
			else:
				#不小
				self.ws2.write(self.row_sheet2,10,0)
				self.ws2.write(self.row_sheet2,8,0)
			self.row_sheet2+=1
		self.sheet2_dic.clear()


	def writesheet_name(self):
		self.ws.write_merge(self.row,self.row+len(self.mydict)-1,0,0,self.datasetname,self.style0)
		#print self.path_write
		#self.wb.save(self.path_write)

	def writesheet_data(self,towrite):
		for i in range(len(towrite)):
			self.ws.write(self.row,i+1,towrite[i],self.style0)
		self.row+=1
		#self.wb.save(self.path_write)

	def com_wr_sheet2(self):#####################################################################
		self.ws2.write_merge(self.row_sheet2,self.row_sheet2+len(self.sheet2_dic)-1,0,0,self.datasetname,self.style0)#写数据集名称

	def write_sheet3(self):
		for k in self.sheet3_dic:
			self.ws3.write(self.row_sheet3,0,k )
			for i in range(len(self.sheet3_dic[k])):
				self.ws3.write(self.row_sheet3,i+1,self.sheet3_dic[k][i])
			self.row_sheet3+=1
		#self.sheet3_dic.clear()

	def write_sheet4(self):
		for key in self.sheet4_dic:
			self.ws4.write(self.row_sheet4,0,key,self.style0)
			self.ws4.write(self.row_sheet4,1,(self.sheet4_dic[key]['icmp_success']*1.0)/self.sheet4_dic[key]['icmp_all'],self.style0)
			for i in xrange(len(self.sheet4_dic[key]['icmp_time'])):
				try:
					self.ws4.write(self.row_sheet4,i+2,self.sheet4_dic[key]['icmp_time'][i],self.style0)
				except Exception as e:
					print '*'*40
					print e
			self.row_sheet4+=1


	def wfile(self):
		#将字典内容写入到文件中
		#print 'Begin_write...'
		#f=open(wpath,'a')
		print 'writing '+self.datasetname
		self.writesheet_name()
		for key in self.mydict:
			self.Feature_DataSet(key)#把写好的字典内相关字段备份并做处理
			towrite=[]
			towrite.append(self.mydict[key]['SrcIP'])
			towrite.append(self.mydict[key]['DstIP'])
			towrite.append(self.mydict[key]['proto'])
			towrite.append(self.mydict[key]['src_port'])
			towrite.append(self.mydict[key]['dst_port'])
			towrite.append(self.mydict[key]['up_pkts'])
			towrite.append(self.mydict[key]['dw_pkts'])
			towrite.append(self.mydict[key]['up_pl_pkts'])
			towrite.append(self.mydict[key]['dw_pl_pkts'])
			towrite.append(self.mydict[key]['up_pl_bytes'])
			towrite.append(self.mydict[key]['dw_pl_bytes'])
			towrite.append(self.mydict[key]['duration'])
			if(self.mydict[key]['up_min_ipt'] == 99999.9):
				self.mydict[key]['up_min_ipt']=0
			if(self.mydict[key]['dw_min_ipt'] == 99999.9):
				self.mydict[key]['dw_min_ipt']=0
			if(self.mydict[key]['up_min_plsize'] == 99999.9):
				self.mydict[key]['up_min_plsize']=0
			if(self.mydict[key]['dw_min_plsize'] == 99999.9):
				self.mydict[key]['dw_min_plsize']=0
			towrite.append(self.mydict[key]['up_min_ipt'])
			towrite.append(self.mydict[key]['dw_min_ipt'])
			towrite.append(self.mydict[key]['up_max_ipt'])
			towrite.append(self.mydict[key]['dw_max_ipt'])
			towrite.append(self.mydict[key]['up_avg_plsize'])
			towrite.append(self.mydict[key]['dw_avg_plsize'])
			towrite.append(self.mydict[key]['up_min_plsize'])
			towrite.append(self.mydict[key]['dw_min_plsize'])
			towrite.append(self.mydict[key]['up_max_plsize'])
			towrite.append(self.mydict[key]['dw_max_plsize'])
			towrite.append(self.mydict[key]['up_stdev_plsize'])
			towrite.append(self.mydict[key]['dw_stdev_plsize'])
			towrite.append(self.mydict[key]['up_avg_ipt'])
			towrite.append(self.mydict[key]['dw_avg_ipt'])
			towrite.append(self.mydict[key]['up_stdev_ipt'])
			towrite.append(self.mydict[key]['dw_stdev_ipt'])
			towrite.append(self.mydict[key]['avg_ttl'])
			towrite.append(self.mydict[key]['up_avg_plsize/duration'])
			towrite.append(self.mydict[key]['num_dns'])
			tempp = sum(self.mydict[key]['up_stdev_ipt_list'])
			if tempp:
				self.mydict[key]['up_pl_bytes_v']=self.mydict[key]['up_pl_bytes']/tempp
			else:
				self.mydict[key]['up_pl_bytes_v']=0
			tempp = sum(self.mydict[key]['dw_stdev_ipt_list'])
			if tempp:
				self.mydict[key]['dw_pl_bytes_v']=self.mydict[key]['dw_pl_bytes']/tempp
			else:
				self.mydict[key]['dw_pl_bytes_v'] = 0
			towrite.append(self.mydict[key]['up_pl_bytes_v'])
			towrite.append(self.mydict[key]['dw_pl_bytes_v'])
			towrite.append(self.mydict[key]['no_shark_response'])
			if self.mydict[key]['many_1'] =='':
				self.mydict[key]['many_1']=''
			towrite.append(self.mydict[key]['many_1'])
			towrite.append(self.mydict[key]['up_rst'])
			towrite.append(self.mydict[key]['dw_rst'])
			#towrite=temp_w.split(',')
			self.writesheet_data(towrite)
			#f.write(temp_w)
		self.com_sheet2()
		self.write_sheet4()
		self.mydict.clear()
		
		#self.wb.save(self.path_write)
		print 'End '+self.datasetname
		#f.close()
		#print 'Done!'


	def isindic(self,keytofind):
		return self.mydict.get(keytofind,False)#不在字典中则返回false,在则返回True
		#setdefault(key)没有就插入，有则返回值对应的值


	def classfy(self,x):
		temp_key1= x.payload.src+'.'+str(x.payload.sport)+'_'+x.payload.dst+'.'+str(x.payload.dport)
		temp_key2= x.payload.dst+'.'+str(x.payload.dport)+'_'+x.payload.src+'.'+str(x.payload.sport)
		
		if(self.isindic(temp_key1) != False):
			keyy=temp_key1
			self.mydict[keyy]['up_pkts'] += 1
			self.mydict[keyy]['duration'] = x.time - self.mydict[keyy]['start_time']
			self.mydict[keyy]['up_avg_ipt'] = (self.mydict[keyy]['up_avg_ipt']*(self.mydict[keyy]['up_pkts']-2)+x.time-self.mydict[keyy]['up_last_time'])/(self.mydict[keyy]['up_pkts']-1)
			self.mydict[keyy]['up_stdev_ipt_list'].append(x.time - self.mydict[keyy]['up_last_time'])
			if x.ttl>128:
				self.mydict[keyy]['to_ttl'] += (256-x.ttl)
			elif x.ttl>64:
				self.mydict[keyy]['to_ttl'] += (128-x.ttl)
			elif x.ttl>32:
				self.mydict[keyy]['to_ttl'] += (64-x.ttl)
			else:
				self.mydict[keyy]['to_ttl'] += (32-x.ttl)
			self.mydict[keyy]['avg_ttl'] = self.mydict[keyy]['to_ttl']/(self.mydict[keyy]['up_pkts']+self.mydict[keyy]['dw_pkts'])
			te=0.0
			for pp in self.mydict[keyy]['up_stdev_ipt_list']:
				te+=(pp-self.mydict[keyy]['up_avg_ipt'])*(pp-self.mydict[keyy]['up_avg_ipt'])
			self.mydict[keyy]['up_stdev_ipt']=te/(self.mydict[keyy]['up_pkts']-1)
			if(len(x.payload.payload.payload) != 0):
				self.mydict[keyy]['up_pl_pkts'] +=1
				self.mydict[keyy]['up_pl_bytes'] += len(x.payload.payload.payload)
				self.mydict[keyy]['up_avg_plsize'] = self.mydict[keyy]['up_pl_bytes']/self.mydict[keyy]['up_pl_pkts']
				self.mydict[keyy]['up_stdev_plsize_list'].append(len(x.payload.payload.payload))
				te=0.0
				for pp in self.mydict[keyy]['up_stdev_plsize_list']:
					te +=(pp-self.mydict[keyy]['up_avg_plsize'])*(pp-self.mydict[keyy]['up_avg_plsize'])
				self.mydict[keyy]['up_stdev_plsize']=te/self.mydict[keyy]['up_pl_pkts']
				if(self.mydict[keyy]['up_min_plsize']>len(x.payload.payload.payload)):
					self.mydict[keyy]['up_min_plsize']=len(x.payload.payload.payload)
				if(self.mydict[keyy]['up_max_plsize']<len(x.payload.payload.payload)):
					self.mydict[keyy]['up_max_plsize']=len(x.payload.payload.payload)
			if(self.mydict[keyy]['up_min_ipt']>(x.time - self.mydict[keyy]['up_last_time'])):
				self.mydict[keyy]['up_min_ipt'] = x.time - self.mydict[keyy]['up_last_time']
			if(self.mydict[keyy]['up_max_ipt']<(x.time - self.mydict[keyy]['up_last_time'])):
				self.mydict[keyy]['up_max_ipt'] = x.time - self.mydict[keyy]['up_last_time']
			self.mydict[keyy]['up_last_time']=x.time
			try:
				self.mydict[keyy]['up_avg_plsize/duration']= self.mydict[keyy]['up_avg_plsize']/self.mydict[keyy]['duration']
			except Exception , e:
				pass
			#计算dns数量
			if x.payload.payload.payload.name == 'DNS':
				self.mydict[keyy]['num_dns'] += 1
			if x.payload.payload.name == 'TCP':
				if x.payload.payload.flags == 4:
					self.mydict[keyy]['up_rst']+=1
				if x.payload.payload.flags  == 16 :
					
					if self.mydict[keyy]['no_shark_response'] == 2:
						self.mydict[keyy]['no_shark_response'] = 0
				if (x.payload.payload.flags  ==53)&('1' not in self.mydict[keyy]['many_1']):
					self.mydict[keyy]['many_1'] += '1'
				elif (x.payload.payload.flags  ==3)&('2' not in self.mydict[keyy]['many_1']):
					self.mydict[keyy]['many_1'] += '2'
				elif (x.payload.payload.flags  ==17)&('3' not in self.mydict[keyy]['many_1']):
					self.mydict[keyy]['many_1'] += '3'

		elif (self.isindic(temp_key2)!= False):
			#在字典中，则对对应的键值做更新
			keyy=temp_key2
			self.mydict[keyy]['dw_pkts'] +=1 ###何为上行，此处把发起链接方发送的数据当做上行
			self.mydict[keyy]['duration'] = x.time - self.mydict[keyy]['start_time']
			if x.ttl>128:
				self.mydict[keyy]['to_ttl'] += 256-x.ttl
			elif x.ttl>64:
				self.mydict[keyy]['to_ttl'] += 128-x.ttl
			elif x.ttl>32:
				self.mydict[keyy]['to_ttl'] += 64-x.ttl
			else:
				self.mydict[keyy]['to_ttl'] += 32-x.ttl
			self.mydict[keyy]['avg_ttl'] = self.mydict[keyy]['to_ttl']/(self.mydict[keyy]['up_pkts']+self.mydict[keyy]['dw_pkts'])
			if(self.mydict[keyy]['dw_pkts']>1):
				self.mydict[keyy]['dw_stdev_ipt_list'].append(x.time - self.mydict[keyy]['dw_last_time'])
				self.mydict[keyy]['dw_avg_ipt'] = (self.mydict[keyy]['dw_avg_ipt']*(self.mydict[keyy]['dw_pkts']-2)+x.time-self.mydict[keyy]['dw_last_time'])/(self.mydict[keyy]['dw_pkts']-1)
				te=0.0
				for pp in self.mydict[keyy]['dw_stdev_ipt_list']:
					te+=(pp-self.mydict[keyy]['dw_avg_ipt'])*(pp-self.mydict[keyy]['dw_avg_ipt'])
				self.mydict[keyy]['dw_stdev_ipt']=te/(self.mydict[keyy]['dw_pkts']-1)
			if(len(x.payload.payload.payload) != 0):
				self.mydict[keyy]['dw_pl_pkts'] +=1
				self.mydict[keyy]['dw_pl_bytes'] += len(x.payload.payload.payload)
				self.mydict[keyy]['dw_avg_plsize'] = self.mydict[keyy]['dw_pl_bytes']/self.mydict[keyy]['dw_pl_pkts']
				self.mydict[keyy]['dw_stdev_plsize_list'].append(len(x.payload.payload.payload))
				te=0.0
				for pp in self.mydict[keyy]['dw_stdev_plsize_list']:
					te +=(pp-self.mydict[keyy]['dw_avg_plsize'])*(pp-self.mydict[keyy]['dw_avg_plsize'])
				self.mydict[keyy]['dw_stdev_plsize']=te/self.mydict[keyy]['dw_pl_pkts']
				if(self.mydict[keyy]['dw_min_plsize']>len(x.payload.payload.payload)):
					self.mydict[keyy]['dw_min_plsize']=len(x.payload.payload.payload)
				if(self.mydict[keyy]['dw_max_plsize']<len(x.payload.payload.payload)):
					self.mydict[keyy]['dw_max_plsize']=len(x.payload.payload.payload)
			if(self.mydict[keyy]['dw_last_time']!=-1):
				if(self.mydict[keyy]['dw_min_ipt']>(x.time - self.mydict[keyy]['dw_last_time'])):
					self.mydict[keyy]['dw_min_ipt'] = x.time - self.mydict[keyy]['dw_last_time']
				if(self.mydict[keyy]['dw_max_ipt']<(x.time - self.mydict[keyy]['dw_last_time'])):
					self.mydict[keyy]['dw_max_ipt'] = x.time - self.mydict[keyy]['dw_last_time']
			self.mydict[keyy]['dw_last_time']=x.time
			#计算dns数量
			if x.payload.payload.payload.name == 'DNS':
				self.mydict[keyy]['num_dns'] += 1
			if x.payload.payload.name=='TCP':
				if x.payload.payload.flags == 4:
					self.mydict[keyy]['dw_rst']+=1
				if (x.payload.payload.flags & 18) == 18:
					if self.mydict[keyy]['no_shark_response'] == 1:
						self.mydict[keyy]['no_shark_response'] = 2
				if (x.payload.payload.flags == 16)&(x.ack-self.mydict[keyy]['last_seq']==1):
					if self.mydict[keyy]['no_shark_response'] == 0:
						self.mydict[keyy]['no_shark_response'] = 3
				if self.mydict[keyy]['seq_num'] == 2:
					self.mydict[keyy]['last_seq'] = x.seq
					self.mydict[keyy]['seq_num'] +=1
				if (x.payload.payload.flags & 53 ==53)&('1' not in self.mydict[keyy]['many_1']):
					self.mydict[keyy]['many_1']+='1'
				elif (x.payload.payload.flags & 3 ==3)&('2' not in self.mydict[keyy]['many_1']):
					self.mydict[keyy]['many_1']+='2'
				elif (x.payload.payload.flags & 17 ==17)&('3' not in self.mydict[keyy]['many_1']):
					self.mydict[keyy]['many_1']+='3'

		else:
			#不在字典中，新加入该关键字，并对内容进行更新
			temp_add={
				temp_key1:{
				'SrcIP':x.payload.src,
				'DstIP':x.payload.dst,
				'src_port':x.payload.sport,
				'dst_port':x.payload.dport,
				'proto':x.payload.proto,#协议号
				'up_pkts':1,#//上行数据包总数
				'dw_pkts':0,#//下行数据包总数
				'up_pl_pkts':0,#//上行有载荷数据包总数
				'dw_pl_pkts':0,#//下行载有荷数据包总数
				'up_pl_bytes':0,#//上行载荷总量
				'up_pl_bytes_v':0,#上行流速率大小
				'dw_pl_bytes':0,#//下行载荷总量
				'dw_pl_bytes_v':0.0,#下行流速率大小
				'duration':0.0,#流持续时间
				'up_min_ipt':99999.9,#//上行最小时间间隔
				'dw_min_ipt':99999.9,#//下行最小时间间隔
				'up_max_ipt':0.0,#//上行最大时间间隔
				'dw_max_ipt':0.0,#//下行最大时间间隔
				'up_avg_plsize':len(x.payload.payload.payload),#上行载荷平均值
				'dw_avg_plsize':0.0,#下行载荷平均值
				'up_min_plsize':99999.9,#上行最小载荷量
				'dw_min_plsize':99999.9,#下行最小载荷量
				'up_max_plsize':len(x.payload.payload.payload),#上行最大载荷量
				'dw_max_plsize':0.0,#下行最大载荷量
				'up_stdev_plsize':0.0,#上行载荷方差
				'dw_stdev_plsize':0.0,#下行载荷方差
				'up_avg_ipt':0.0,#上行数据包时间间隔平均值
				'dw_avg_ipt':0.0,#下行数据包时间间隔平均值
				'up_stdev_ipt':0.0,#上行时间间隔方差
				'dw_stdev_ipt':0.0,#下行时间间隔方差
				'up_last_time':x.time,#//上一个数据包的时间
				'dw_last_time':-1,
				'start_time':x.time,#流的开始时间
				'up_stdev_plsize_list':[],#上行载荷list
				'dw_stdev_plsize_list':[],#下行载荷list
				'avg_ttl':0,#//ttl平均值
				'to_ttl':0,#ttl和
				'up_avg_plsize/duration':0.0,

				'up_stdev_ipt_list':[],#上行时间间隔list
				'dw_stdev_ipt_list':[],#下行时间间隔list

				'num_dns':0,#dns数据包数量

				'no_shark_response':-1,#0-源ip正常回应，1-源ipSYN为1；2-目的IPSYN=1，ACK=1；3-源IP多次回应ACK=1
				'many_1':'',#0-正常；1-ACK=1、URG,FIN,RST同时=1；2-SYN、FIN同时=1；3-ACK,FIN同时=1
				'last_seq':0,
				'seq_num':0,
				'dw_rst':0,
				'up_rst':0
				}
			}
			#计算dns数量
			if x.payload.payload.name=='TCP':
				temp_add[temp_key1]['last_seq'] = x.seq
				temp_add[temp_key1]['seq_num'] +=1
				if x.payload.payload.flags == 4:
					temp_add[temp_key1]['up_rst']+=1
				if x.payload.payload.flags ==2:
					temp_add[temp_key1]['no_shark_response'] = 1
				if x.payload.payload.flags & 53 ==53:
					temp_add[temp_key1]['many_1']+='1'
				elif x.payload.payload.flags & 3 ==3:
					temp_add[temp_key1]['many_1'] += '2'
				elif x.payload.payload.flags & 17 ==17:
					temp_add[temp_key1]['many_1'] += '3'
			if x.payload.payload.payload.name == 'DNS':
				temp_add[temp_key1]['num_dns'] += 1

			if x.ttl>128:
				temp_add[temp_key1]['to_ttl'] += 256-x.ttl
			elif x.ttl>64:
				temp_add[temp_key1]['to_ttl'] += 128-x.ttl
			elif x.ttl>32:
				temp_add[temp_key1]['to_ttl'] += 64-x.ttl
			else:
				temp_add[temp_key1]['to_ttl'] += 32-x.ttl
			if(len(x.payload.payload.payload) != 0 ):
				temp_add[temp_key1]['up_pl_pkts'] +=1
				temp_add[temp_key1]['up_pl_bytes'] += len(x.payload.payload.payload)
				temp_add[temp_key1]['up_min_plsize'] = len(x.payload.payload.payload)
				temp_add[temp_key1]['up_stdev_plsize_list'].append(len(x.payload.payload.payload))
			self.mydict.update(temp_add)
def main():
	path_pcap=''
	path_write=''
	try:
		#print sys.argv
		opts, args = getopt.getopt(sys.argv[1:], "i:o:")
		for a,b in opts:
			if a == '-i':
				path_pcap = b
				path_write = b+r'\1.xls'
			if a == '-o':
				path_write = b
	except Exception , e:
		
		print 'input right format please: python '+sys.argv[0]+' -i path_inpput -o path_output\n\
		path_input:path of pcap files,eg: C:\\pcap\n\
		path_output:path of result file. eg: C:\\pcap_out\\1.csv\n\
		Nobody is responsible for any question.'
		exit(0)
		
	#path_pcap = r'F:\pcap'
	#path_write = r'F:\pcap\1234.xls'
	p=pcap_a(path_write)
	a=os.walk(path_pcap)	
	#bb=a.next()[2]
	#print a
	#将pcap文件格式转化为标准
	for i in a:
		#print i
		a_temp=i[2]
		path_pcap=i[0]
		p.path_write=path_pcap+r'\1.xls'
		for temp_pcap in a_temp:
			if(temp_pcap[-4:] != 'pcap'):
				continue
			print 'begin read'+temp_pcap
			
			path_pcap1=os.path.join(path_pcap,temp_pcap)
			
			'''
			path_pcap2=path_pcap1+'ng'
			os.rename(path_pcap1,path_pcap2)
			#将pcap文件格式转化为标准
			#time.sleep(5)
			cmmd = 'tshark.exe -r '+path_pcap2+' -w '+path_pcap1+' -F pcap'
			#print cmmd
			os.system(cmmd)
			os.remove(path_pcap2)
			'''	

			#print path_pcap2
			print path_pcap1
			f=scapy.rdpcap(path_pcap1)
			#temp_len=len(f)
			f=iter(f)
			p.setname(temp_pcap[:-5])
			print 'read success'
			num = 1
			#temp_len=len(f)
			for k in f:
				if num % 1000 == 0:
					sys.stdout.write('{0}/100\r'.format(num/1000))
					sys.stdout.flush()
				#print num
				num+=1
				#i=num*100/temp_len
				#sys.stdout.write('{0}/100'.format(i))
				#sys.stdout.flush()
				if(k.payload.name != 'IP'):
					continue
					#ipv6好烦啊
				if k.payload.payload.name =='ICMP':
					p.icmp_sheet4(k)
				if ((k.payload.payload.name == 'TCP')|(k.payload.payload.name == 'UDP')):
					
					p.classfy(k)
					#print str(p.mydict['172.16.253.129.68_172.16.253.254.67']['avg_ttl'])+'+++'+str(p.mydict['172.16.253.129.68_172.16.253.254.67']['to_ttl'])
			del f
			gc.collect()
			p.wfile()
			p.wb.save(p.path_write)
		p.write_sheet3()
		p.wb.save(p.path_write)
		

if __name__=="__main__":
	main()
