# -*- coding: utf-8 -*-

import time
from urllib import request
from lxml import etree
import re

class SzSecurityHousingPipeline(object):


	def process_item(self, item, spider):
		# print(item)
		url='http://zjj.sz.gov.cn/bzflh/lhmcAction.do?method=queryDetailLhc&lhmcId=%s&waittype=2'%(item['userid'])
		# print(url)
		try:
			response = request.urlopen(url,timeout=5)
			page = response.read()
			page = page.decode('utf-8')
			selector = etree.HTML(page)
			content=selector.xpath('//div[@class="leader_intro1"]')[1].xpath('string(.)')
			place = re.search('户籍所在区.*区',content).group().replace('户籍所在区：','')
			item['place']=place
			num=len(selector.xpath('//div[@class="leader_intro1"]'))-1
			item['num']=num
		except Exception:
			print ("Error:%s"%(item['seqno']))
			print(repr(e))

		# else:	
		# 	print ("Success:%s"%(item['seqno']))
		ret=str(item['userid'])+','+str(item['username'])+','+str(item['seqno'])+","+str(item['applyNo'])+","+str(item['num'])+","+str(item['place'])+"\n"
		today = time.strftime("%Y-%m-%d",time.localtime(time.time()))
		saveFile = open('data_'+today+'.txt','a')  
		saveFile.write(ret)  
		saveFile.close()  
		# print(item)