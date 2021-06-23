import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.request import urlretrieve
from selenium import webdriver
from time import sleep
import os


# download web novel
def get_content(url):
    content = requests.get(url)
    content.encoding = 'utf-8'
    bs2 = BeautifulSoup(content.text, 'lxml')
    content = bs2.find(name='div', attrs={'class':'post-content-right'})
    paras = content.find_all(name='p')
    paras = [para.text.strip() for para in paras]
    
    return paras

def spyreader(hostname):
    req3 = requests.get(hostname)
    req3.encoding = 'utf-8'
    html = req3.text
    bs = BeautifulSoup(html, 'lxml')

    titles = bs.find_all(name='div', attrs={'class':'content'})
    for title in tqdm(titles):
        a = title.find(name='a')
        name = a.string.strip()
        assert('downloading'+name)
        url = a.get(key='href')
        content = get_content(url)
        with open(name+'.txt', 'a', encoding='utf-8') as f:
            f.write(name)
            f.write('\n')
            f.write('\n'.join(content))
            f.write('\n')
            


# download book from TsinghuaLib

# 获取图片地址前缀
def get_prefix(url):
    pre = url.split('mobile/')
    pre = pre[0] + 'files/mobile/'
    return pre

#获取总页数
def get_total_num_page(url):
    # 创建无界面的chrome浏览器
    opts = webdriver.ChromeOptions()
    opts.headless = True
    browser = webdriver.Chrome(options=opts)
    browser.get(url)
    sleep(0.5) # 等待页面渲染完成
    pages = browser.find_elements_by_class_name('title')
#     print(pages[-4].get_attribute('textContent'))
    total_num_pages = int(pages[-4].get_attribute('textContent'))
    browser.quit()
    return total_num_pages
    
def get_book_from_tsinghua_lib(url, dname):
    pre = get_prefix(url)
    
    total_num_pages = get_total_num_page(url)
#     print('Total number of pages: ', total_num_pages)
    
    if not os.path.isdir(dname):
        os.mkdir(dname)
    dname = './' + dname + '/'
    
    with tqdm(range(1, total_num_pages + 1)) as t:
        try:
                for i in t:
                    durl = pre + str(i) + '.jpg'
                    fname = dname + str(i) + '.jpg'
                    urlretrieve(durl, fname)
        except BaseException:
            t.close()
            print('Error')
        else:
            t.close()
            print('Done')


if __name__ == "__main__":
    # for books with a single chapter
    url = 'http://reserves.lib.tsinghua.edu.cn/book5//00003534/00003534000/mobile/index.html'
    dname = '有机化学_王芹珠'

    get_book_from_tsinghua_lib(url=url, dname=dname)

    # for books with multiple chapters
    num_chapers = 6
    head = 'http://reserves.lib.tsinghua.edu.cn/book5//00000906/0000090600'
    tail = '/mobile/index.html'
    urls = [head+str(i)+tail for i in range(0, num_chapers)]
    dnames = ['微生物学实验指导_陈今春'+str(i) for i in range(0, num_chapers)]

    for i in range(0, num_chapers):
        get_book_from_tsinghua_lib(urls[i], dnames[i])



