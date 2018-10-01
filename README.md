# 深圳公租房爬虫
按家庭人数分析区级排名

##目录

1.使用python的scrapy框架爬取深圳公租房轮候库，数据保存在文件里；

2.将文件数据导入mysql;

3.使用python将文本数据导入mysql；

4.使用ELK，将数据导入elasticsearch，通过kibana展示；

5.kibana数据分析；

##爬取说明
爬取网址：[http://www.szjs.gov.cn/bsfw/zdyw_1/zfbz/gxfgs/](http://www.szjs.gov.cn/bsfw/zdyw_1/zfbz/gxfgs/)

![page1](https://github.com/tianduo4/sz_security_housing/blob/master/imgs/page_1.png)

![page2](https://github.com/tianduo4/sz_security_housing/blob/master/imgs/page_2.png)

参考2018年9月30日爬取结果data.txt

    1	BHJ005840	3955877	1	南山区
    2	BHJ005866	3955878	1	南山区
    3	BHJ021327	3955879	2	南山区
    4	BHJ005848	3955880	1	南山区
    5	BHJ006961	3955881	4	南山区
    6	BHJ016656	3955882	1	南山区
    7	BHJ002199	3955883	1	南山区
    8	BHJ029628	3955884	3	罗湖区
    9	BHJ016179	3955885	3	盐田区
    10	BHJ022242	3955886	1	罗湖区