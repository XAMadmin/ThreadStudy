import requests
from lxml import etree
import time
from fake_useragent import UserAgent


headers = {
     "User-Agent": str(UserAgent().random),
     "Cookie": "BAIDU_SSP_lcr=https://www.baidu.com/link?url=oZLH4S6k5AVyLn8BB8sM9RP0EqxNz_KgvyqL5wnN_BNKv6TqX9w7h6DxnIrkv1PK&wd=&eqid=88a47e2c00196df000000005601c9bb5; Hm_lvt_2fc12699c699441729d4b335ce117f40=1612487599; Hm_lpvt_2fc12699c699441729d4b335ce117f40=1612489932"
     
}


url = "https://www.doutula.com/photo/list/"

# 单线程下载
def down_load():
    response = requests.get(url=url, headers=headers)
    time.sleep(5)
    if response.status_code == 200:
        cookie = response.cookies.items()
        print(cookie)
        html = response.text
        text = etree.HTML(html)
        divs = text.xpath("//div[@class='random_picture']/ul[@class='list-group']/li[@class='list-group-item']/div[@class='page-content text-center']/div/a")
        for div in divs:
            img_url = div.xpath(".//img/@data-backup")[0]
            img_name = img_url.split("/")[-1]
            print(img_url) 
            i = 0   
            while True:        
                try:
                    res = requests.get(url=img_url, headers=headers, stream=True)
                    with open("imges/"+img_name, 'wb') as f:
                        for chunk in res.iter_content(chunk_size=512):
                            if chunk:
                                f.write(chunk)
                                f.flush()
                    print("图片下载成功...")
                    i = 0
                except Exception as e: 
                    i += 1 
                    print("图片下载失败第" + str(i) + "次")
                    print(e) 
                    time.sleep(1)
                if i==0:
                    break
                
            # time.sleep(2)


if __name__ == "__main__":
    start = time.time()
    down_load()
    end = time.time()
    print("完成时间：" + str(end - start))
 