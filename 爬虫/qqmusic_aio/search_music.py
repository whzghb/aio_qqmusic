import requests
from urllib.parse import quote_plus
import jsonpath
import json
import threading
import itertools
# url  = "https://y.qq.com/portal/search.html#page=1&searchid=1&remoteplace=txt.yqq.top&t=song&w=%E6%B1%AA%E5%B3%B0"
# http://ws.stream.qqmusic.qq.com/C100000PLHrM2luXiz.m4a?fromtag=0&guid=126548448
class GetMusic(object):
    def __init__(self, keyword, headers):
        self.keyword = keyword
        self.headers = headers
        self.all_json_obj = []

    def get_response(self,url):
        response = requests.get(url, headers=headers)
        response_text = response.text
        dict_data = response_text[9:len(response_text) - 1].replace(" ", "")
        json_data = json.loads(dict_data)
        # print(jsonpath.jsonpath(json_data,"$..keyword"))
        if jsonpath.jsonpath(json_data, "$..keyword") != ['']:
            self.all_json_obj.append(json_data)

    def get_url(self):
        task = []
        for i in range(50):
            url = "https://c.y.qq.com/soso/fcgi-bin/search_for_qq_cp?g_tk=5381&uin=0" \
                  "&format=jsonp&inCharset=utf-8&outCharset=utf-8&notice=0&platform=h5" \
                  "&needNewCode=1&w=%s&zhidaqu=1&catZhida=1&t=0&flag=1&ie=utf-8" \
                  "&sem=1&aggr=0&perpage=20&n=30&p=%s&remoteplace=txt.mqq.all&_=1520833663464'" \
                  % (self.keyword, str(i))
            response = threading.Thread(target=self.get_response,args=(url,))
            response.start()
            task.append(response)
        for t in task:
            t.join()

    def json_parse(self):
        all_song = []
        for response in self.all_json_obj:
            song_mid = jsonpath.jsonpath(response,'$..songmid')
            song_name = jsonpath.jsonpath(response,'$..songname')
            song_singer = jsonpath.jsonpath(response,'$..singer.0.name')
            song_album = jsonpath.jsonpath(response,'$..albumname')
            if not song_name or not song_singer or not song_mid or not song_album:
                continue
            else:
                zip_list = zip(list(song_name),list(song_mid),list(song_singer),list(song_album))
                all_song.append(list(zip_list))
        all_song = list(itertools.chain(*all_song))
        res = []
        count = 0
        for i in range(len(all_song)):
            if all_song[i] != None:
                all_song[i] = list(all_song[i])
                all_song[i][1] = "http://ws.stream.qqmusic.qq.com/C100%s.m4a?fromtag=0&guid=126548448" % \
                                 all_song[i][1]
                if self.keyword != all_song[0] and self.keyword != all_song[2]:
                    count += 1
                    res.append(all_song[i])
                else:
                    res.insert(i-count, all_song[i])
        return res

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/66.0.3359.181 Safari/537.36"}
headers["referer"] = "https://y.qq.com/"
