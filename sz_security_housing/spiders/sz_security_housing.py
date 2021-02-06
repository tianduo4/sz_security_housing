# -*- coding: utf-8 -*-
import scrapy
from sz_security_housing.items import SzSecurityHousingItem
from scrapy.http import FormRequest
import json
import time

class SzSecurityHousingSpider(scrapy.Spider):
	#爬虫名
	name = 'szsh'

     #爬虫域
	allowed_domains = ['zjj.sz.gov.cn']

	default_pageSize=100  #接口最大支持100

	start_pageNum=1

	fetch_maxcount=26202

	def start_requests(self):
		url='http://zjj.sz.gov.cn/bzflh/lhmcAction.do?method=queryYgbLhmcList&waittype=2'

		headers = {
			'Accept': 'application/json, text/javascript, */*; q=0.01',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.9',
			'Connection': 'keep-alive',
			'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
			'Cookie':'_trs_uv=jw3pizal_1323_iylm; pgv_pvi=6386012160; ftzjjszgovcn=0; Hm_lvt_ddaf92bcdd865fd907acdaba0285f9b1=1612591183; swfUrl=%2Fvideos%2Fcnill_polyfill.swf; session-cookie=59436614; JSESSIONID=FP517QIoSGPw-rxUZoeKY_kKonPBUSvoMYgHAMpaAK-lsOa6VpqD!-522403324; Hm_lpvt_ddaf92bcdd865fd907acdaba0285f9b1=1612592534',
			'Host': 'zjj.sz.gov.cn',
			'Origin': 'http://zjj.sz.gov.cn',
			'Referer': 'http://zjj.sz.gov.cn/bzflh/lhmcAction.do?method=queryYgbLhmcInfo&waittype=2',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
		}

		yield scrapy.FormRequest(
			url = url,
			headers = headers,
			formdata = {"pageNumber" : "1", "pageSize" : str(self.default_pageSize),"waittype":"2","num":"0","shoulbahzh":"","xingm":"","idcard":"","start_paix":"","end_paix":""},
			meta={'pageNum':self.start_pageNum,'pageSize':self.default_pageSize,"headers":headers},
			callback = self.parse
		)


	def parse(self,response):
		data  = json.loads(response.body_as_unicode())
		# print(data)
		total = data["total"]
		# print(total)
		list = data["rows"]
		item=SzSecurityHousingItem()
		for value in list:
			item['userid']=value['LHMC_ID']
			item['seqno']=value['PAIX']
			item['applyNo']=value['SHOULHZH']
			item['username']=value['XINGM']
			# print(value)
			yield item
		url = 'http://zjj.sz.gov.cn/bzflh/lhmcAction.do?method=queryYgbLhmcList&waittype=2'
		meta=response.meta
		prepageNumber=meta["pageNum"]
		pageSize=meta["pageSize"]
		headers=meta["headers"]
		current_total=prepageNumber*pageSize
		print('finsh scrapy pageNumber:%s'%prepageNumber)
		print('finsh current total:%s'%current_total)
		print(self.fetch_maxcount)
		print(len(list))
		print('pageSize:%s'%pageSize)
		pageNumber=prepageNumber+1
		if len(list) == pageSize and current_total<self.fetch_maxcount:
			requestdata={"pageNumber" : "1", "pageSize" : str(self.default_pageSize),"waittype":"2","num":"0","shoulbahzh":"","xingm":"","idcard":"","start_paix":"","end_paix":""}
			requestdata['pageNumber']=str(pageNumber)
			requestdata['pageSize']=str(pageSize)
			meta['pageNum']=pageNumber
			# print(requestdata)
			yield scrapy.FormRequest(
				url = url,
				headers = headers,
				formdata =requestdata,
				meta=meta,
				callback = self.parse
			)
