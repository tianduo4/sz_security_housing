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
	allowed_domains = ['szjs.gov.cn']

	def start_requests(self):
		url = 'http://bzflh.szjs.gov.cn/TylhW/lhmcAction.do?method=queryYgbLhmcList'

		headers = {
			'Accept': 'application/json, text/javascript, */*; q=0.01',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.9',
			'Connection': 'keep-alive',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Host': 'bzflh.szjs.gov.cn',
			'Origin': 'http://bzflh.szjs.gov.cn',
			'Referer': 'http://bzflh.szjs.gov.cn/TylhW/lhmcAction.do?method=queryYgbLhmcInfo&waittype=2',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
		}

		yield scrapy.FormRequest(
			url = url,
			headers = headers,
			formdata = {"pageNumber" : "1", "pageSize" : "10","waittype":"2","num":"0","shoulbahzh":"","xingm":"","idcard":""},
			meta={'pageNum':1,'pageSize':10,"headers":headers},
			callback = self.parse
        )


	def parse(self,response):
		item=SzSecurityHousingItem()
		data  = json.loads(response.body_as_unicode())
		# print(data)
		total = data["total"]
		# print(total)
		list = data["rows"]
		for value in list:
			item['userid']=value['LHMC_ID']
			item['seqno']=value['PAIX']
			item['applyNo']=value['SHOULHZH']
			yield item

		url = 'http://bzflh.szjs.gov.cn/TylhW/lhmcAction.do?method=queryYgbLhmcList'
		meta=response.meta
		prepageNumber=meta["pageNum"]
		pageSize=meta["pageSize"]
		headers=meta["headers"]
		print('finsh scrapy pageNumber:%s'%prepageNumber)
		print(len(list))
		time.sleep( 2 )
		pageNumber=prepageNumber+1
		if len(list) == pageSize:
			requestdata={"pageNumber" : "1", "pageSize" : "1000","waittype":"2","num":"0","shoulbahzh":"","xingm":"","idcard":""}
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
