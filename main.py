import requests
import json
import prettytable as zkz
name = input('请输入歌曲或歌手名称')
url = f'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p=1&n=10&w={name}'
r = requests.get(url)
print(r.text)
json_str = r.text
json_str = json_str[9:-1]
json_dict = json.loads(json_str)
song_list = json_dict['data']['song']['list']
tb = zkz.PrettyTable()
tb.field_names = ['序号','歌名','歌手','专辑']
music_info_list = []
count = 0
for song in song_list:
    songname = song['songname']
    songid = song['songid']
    singer = song['singer'][0]['name']
    albumname = song['albumname']
    tb.add_row([count,songname,singer,albumname])
    music_info_list.append([songid,singer,songname])
    count += 1
    print(tb)
while True:
    input_index = eval(input('请输入你要下载的歌曲序号(-2)退出'))
    if input_index == -1:
        break
    download_info = music_info_list[input_index]
    songmid = download_info[0]
    music_info_url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?data={"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch", "filename":"M800","param":{"guid":"8846039534","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","filename":"M800","param":{"guid":"8846039534","songmid":["%s"],"songtype":[0],"uin":"1152921504784213523","loginflag":1,"platform":"20"}},"comm":{"uin":"1152921504784213523","format":"json","ct":24,"cv":0}}' % songid
    json_data = requests.get(url=music_info_url).json()
    purl = json_data['req_0']['data']['midurlinfo'][0]['purl']
    media_url = 'https://dl.stream.qqmusic.qq.com/' + purl
    music_data = requests.get(media_url).content
    #保存数据
    with open(f'歌曲下载/{download_info[1]}-{download_info[2]}.mp3',mode='wb') as f:
            f.write(music_data)
    print(f'{download_info[1]},下载成功！')