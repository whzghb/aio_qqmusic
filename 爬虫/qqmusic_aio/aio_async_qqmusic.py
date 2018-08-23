import aiohttp
import asyncio
import json
import re
from config import *
import pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

# http://ws.stream.qqmusic.qq.com/C100(004W8SSn2fdHzj).m4a?fromtag=0&guid=126548448

async def get_html(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
               "Chrome/66.0.3359.181 Safari/537.36"}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            return await response.text()

async def save(res):
    for rank,detail in enumerate(res):
        if detail != None:
            result = {
                "rank":rank+1,
                "url":"http://ws.stream.qqmusic.qq.com/C100%s.m4a?"
                      "fromtag=0&guid=126548448" % detail[2],
                "name":detail[3],
                "singer":detail[1],
            }
            try:
                if db[MONGO_TABLE].insert(result):
                    # print("保存成功",result)
                    pass
            except Exception as e:
                print(e)

async def html_parse(result):
    # 有的url请求之后不返回数据，此处没有数据的result不为空，而是等于1，很坑
    if len(result) == 1:
        pass
    else:
        pattern = re.compile('.*?"cur_count":"(\d+)".*?"singer".*?"name":'
                             '"(.*?)".*?"songmid":"(.*?)","songname":"(.*?)",',re.S)
        res = result.strip().replace(" ", "").replace("'", '"')
        res = re.findall(pattern, res)
        await save(res)

async def request(num):
    # 每页爬取多少取决于下方的song_num,每个榜单最大为300,所以此处可以取到300
    url = "https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?tpl=3&page=detail&topid={}&song_begin=0&song_num=300".format(num)
    result = await get_html(url)
    list_info = await html_parse(result)

if __name__ == "__main__":
    # 爬取多少取决于下方的range
    task = [asyncio.ensure_future(request(i)) for i in range(1, 400)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(task))

