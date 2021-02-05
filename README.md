# 多线程下载斗图图片

## 构造多线程函数

此程序仅供学习使用

[斗图地址](https://www.doutula.com/photo/list/)

+ 所需库：

  ```
  fake-useragent==0.1.11
  lxml==4.6.2
  requests==2.25.1
  ```

1. 获取需要爬取的url地址

```python
def get_url(img_url_que, img_name_que):
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        html = response.text
        text = etree.HTML(html)
        divs = text.xpath("//div[@class='random_picture']/ul[@class='list-group']/li[@class='list-group-item']/div[@class='page-content text-center']/div/a")
        for div in divs:
            img_url = div.xpath(".//img/@data-backup")[0]
            img_name = img_url.split("/")[-1]
            img_url_que.put(img_url)
            img_name_que.put(img_name)
```



2. 构造下载图片函数

```python
def down_load(img_url_que, img_name_que, j):
    while True:
        img_url = img_url_que.get()
        img_name= img_name_que.get()
        i = 0   
        while True: 
            try:
                res = requests.get(url=img_url, headers=headers, stream=True)
                with open("imges/"+img_name, 'wb') as f:
                    for chunk in res.iter_content(chunk_size=512):
                        if chunk:
                            f.write(chunk)
                            f.flush()
                print("线程【{}】:图片{},下载完成。。。".format(j, img_name))
                i = 0
            except Exception as e: 
                i += 1 
                print("线程【{}】:尝试下载图片{},失败第{}次。。。".format(j, img_name, i))
                # print(e) 
                time.sleep(1) # 下载失败进行线程切换
            if i==0 or i==50: # 尝试50次下载，超过次数自动终止当前图片下载
                break
        img_url_que.task_done()
        img_name_que.task_done()
```

+ 这里主要技术：利用 消息队列来进行线程的之间的管理，保证程序的正常执行，以及队列执行完毕自动关闭主线程

```python
def run():
    img_url_que = Queue()
    img_name_que = Queue()
    
    p = Thread(target=get_url, args=(img_url_que, img_name_que))
    p.setDaemon(True)
    p.start()

    time.sleep(5) # 等待该线程抓取url响应,之后再开启下载线程

    for j in  range(5):
        d = Thread(target=down_load, args=(img_url_que, img_name_que, j))
        d.setDaemon(True)
        d.start()

    for que in [img_url_que, img_name_que]:
        que.join()
```

