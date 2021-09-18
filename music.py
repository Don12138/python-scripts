# -*_coding:utf8-*-
import json
import random
import requests
import re
import eyed3
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
playlist_url = "https://api.imjad.cn/cloudmusic/?type=playlist&id="
song_url = "https://tenapi.cn/wyy?id="
headers = {
    'Connection': 'close'
}
user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0;) Gecko/20100101 Firefox/61.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
]


def main():
    download_playlist = input("下载歌单输入p,循环下载歌曲输入s")
    if download_playlist == 'p':
        input_data = input("请输入歌单url(id):")
        may_playlist = re.search("playlist\?id=\d*", input_data)
        if may_playlist is not None:
            playlist_id = input_data[may_playlist.span()[0] + 12:may_playlist.span()[1]]
            playlist(playlist_id)
        else:
            playlist(input_data)
    elif download_playlist == 's':
        while True:
            input_data = input("请输入歌曲url(id):")
            may_song = re.search("song\?id=\d*", input_data)
            if may_song is not None:
                song_id = input_data[may_song.span()[0] + 8:may_song.span()[1]]
                download(song_id)
            else:
                download(input_data)


def playlist(playlist_id):
    headers['User-Agent'] = random.choice(user_agent_list)
    result = requests.request(url=playlist_url + str(playlist_id), method="GET", verify=False, headers=headers)
    info = result.json()
    if "msg" in info.keys():
        print("未查询到歌单信息")

    song_ids = []
    print(info)
    for song_info in info['playlist']['trackIds']:
        song_ids.append(song_info["id"])

    while len(song_ids) != 0:
        for song_id in song_ids:
            try:
                headers['User-Agent'] = random.choice(user_agent_list)
                result = requests.request(url=song_url + str(song_id), method="GET", verify=False, headers=headers)
                info = result.json()
                if "msg" in info.keys():
                    print("请输入正确的歌单url(id)或歌曲url(id)")
                else:
                    if info['data']['url'] == '':
                        print(str(song_id) + "无url")
                        song_ids.remove(song_id)
                        continue
                    headers['User-Agent'] = random.choice(user_agent_list)
                    url = "http://music.163.com/api/song/detail/?id=" + str(song_id) + "&ids=%5B" + str(song_id) + "%5D"
                    result = requests.request(url=url, method="GET",headers=headers).json()  # 获取专辑名称和专辑封面
                    name = info['data']['name'] + "(" + result['songs'][0]['album']['name'] + ")"  # 歌曲文件名
                    img_url = result['songs'][0]['album']['blurPicUrl']  # 封面

                    f = requests.request(url=info['data']['url'], method="GET", verify=False, headers=headers)
                    with open("song/" + name + ".mp3", "wb") as code:
                        code.write(f.content)

                    q = requests.request(url=img_url, method="GET", verify=False)

                    audiofile = eyed3.load("song/" + name + ".mp3")
                    audiofile.tag.title = info['data']['name']
                    audiofile.tag.artist = info['data']['song']
                    audiofile.tag.album = result['songs'][0]['album']['name']
                    audiofile.tag.images.remove(u'')
                    audiofile.tag.images.set(3, q.content, "image/jpeg")
                    audiofile.tag.save()
                    print(info['data']['name'] + "下载完成")
                    song_ids.remove(song_id)
            except Exception as a :
                print(a)
                print(str(song_id) + "失败")


def download(song_id):
    success = False
    while not success:
        try:
            headers['User-Agent'] = random.choice(user_agent_list)
            info = requests.request(url=song_url + str(song_id), method="GET", verify=False, headers=headers).json()
            if "msg" in info.keys():
                print("请输入正确的歌单url(id)或歌曲url(id)")
                return
            else:
                if info['data']['url'] == '':
                    print("暂无url")
                    return
                headers['User-Agent'] = random.choice(user_agent_list)
                url = "http://music.163.com/api/song/detail/?id=" + song_id + "&ids=%5B" + song_id + "%5D"
                result = requests.request(url=url, method="GET").json()#获取专辑名称和专辑封面
                name = info['data']['name'] + "(" + result['songs'][0]['album']['name'] + ")"#歌曲文件名
                img_url = result['songs'][0]['album']['blurPicUrl']#封面

                f = requests.request(url=info['data']['url'], method="GET", verify=False, headers=headers)
                with open("song/" + name + ".mp3", "wb") as code:
                    code.write(f.content)

                q = requests.request(url=img_url, method="GET", verify=False)

                audiofile = eyed3.load("song/" + name + ".mp3")
                audiofile.tag.title = info['data']['name']
                audiofile.tag.artist = info['data']['song']
                audiofile.tag.album = result['songs'][0]['album']['name']
                audiofile.tag.images.remove(u'')
                audiofile.tag.images.set(3, q.content, "image/jpeg")
                audiofile.tag.save()
                print(info['data']['name'] + "下载完成")
                success = True
        except Exception as a:
            print(a)
            print(str(song_id) + "失败")


if __name__ == '__main__':
    main()
