import urllib
from urllib.parse import quote
import requests
import execjs
import time
import random
import csv
from datetime import datetime


def cookies_to_dict(cookie_string: str) -> dict:
    cookies = cookie_string.strip().split('; ')
    cookie_dict = {}
    for cookie in cookies:
        if cookie == '' or cookie == 'douyin.com':
            continue
        key, value = cookie.split('=', 1)
        cookie_dict[key] = value
    return cookie_dict


HOST = 'https://www.douyin.com'
PARAMS1 = {
    'device_platform': 'webapp',
    'aid': '6383',
    'channel': 'channel_pc_web',
    'update_version_code': '170400',
    'pc_client_type': '1',  # Windows
    'version_code': '190600',
    'version_name': '19.6.0',
    'cookie_enabled': 'true',
    'screen_width': '1536',  # from cookie dy_swidth
    'screen_height': '864',  # from cookie dy_sheight
    'browser_language': 'zh-CN',
    'browser_platform': 'Win32',
    'browser_name': 'Edge',
    'browser_version': '126.0.0.0',
    'browser_online': 'true',
    'engine_name': 'Blink',
    'engine_version': '126.0.0.0',
    'os_name': 'Windows',
    'os_version': '10',
    'cpu_core_num': '12',  # device_web_cpu_core
    'device_memory': '8',  # device_web_memory_size
    'platform': 'PC',
    'downlink': '10',
    'effective_type': '4g',
    'round_trip_time': '100',
    # 'webid': '',   # from doc
    # 'verifyFp': '',   # from cookie s_v_web_id
    # 'fp': '', # from cookie s_v_web_id
    # 'msToken': '',  # from cookie msToken
    # 'a_bogus': '' # sign
}
PARAMS2 = {
    'device_platform': 'webapp',
    'aid': '6383',
    'channel': 'channel_pc_web',
    'aweme_id': '7392551560301006090',
    'cursor': '0',
    'count': '20',
    'item_type': '0',
    'whale_cut_token': '',
    'cut_version': '1',
    'rcFT': '',
    'update_version_code': '170400',
    'pc_client_type': '1',
    'version_code': '170400',
    'version_name': '17.4.0',
    'cookie_enabled': 'true',
    'screen_width': '1536',
    'screen_height': '864',
    'browser_language': 'zh-CN',
    'browser_platform': 'Win32',
    'browser_name': 'Edge',
    'browser_version': '126.0.0.0',
    'browser_online': 'true',
    'engine_name': 'Blink',
    'engine_version': '126.0.0.0',
    'os_name': 'Windows',
    'os_version': '10',
    'cpu_core_num': '12',
    'device_memory': '8',
    'platform': 'PC',
    'downlink': '10',
    'effective_type': '4g',
    'round_trip_time': '100',
    'webid': '7385074968550475275',
    'msToken': '_ErSVNPvTrmYqlk3XFnkSk5I6YdjGeoMVCQfCrvVcOnJZvT1fctOmnCG4FG6DoymrVNY7-pD7ckMN6WIApTA9WFtme19QOQtPhEg2lO7soqMOqYEsqQ4DoXnsUM0PQ%3D%3D'

}

cookie = "ttwid=1%7C5YPnAzzd0On7_Nlpm6ehFwdr_GOkz3OSNtVaxYRAC9Y%7C1719471779%7C4c1442fe8808443aacffb9f78ae6cb115f7e93a67e80cf9d00ebbde308df474b; UIFID_TEMP=c4683e1a43ffa6bc6852097c712d14b81f04bc9b5ca6d30214b0e66b4e38528096014edc369c1be1d5510b302a65a54bc5a08d82a97dff35f2c5fd209fd0ccb021780c023ed0410d72a0fccc9c5e06a12f7d53142163a7cadaf9a84032f10719; fpk1=U2FsdGVkX1/FOCt7ZdO3GR7H96xIVpd88afsSTkS3nR8A7j/yaxjEYz3xRiHkoCAz5f5AlGkWQT+7tNPMXiwlQ==; fpk2=5f4591689f71924dbd1e95e47aec4ed7; bd_ticket_guard_client_web_domain=2; UIFID=c4683e1a43ffa6bc6852097c712d14b81f04bc9b5ca6d30214b0e66b4e38528096014edc369c1be1d5510b302a65a54b5f829e90687e739d4608bc8011d94b4e41142b27ed318d7fae17f0834225b0af6562d402bf9380710c9961abf452aa064369df94092ee7977b73fb185404f8ee1b6b1291bad1b10cdc713d891d41a070ef83c69fc31f818df9b1a608aa0012c9bee09861845e19e69a050579f82ec7f604dfc1165a1dd66b7ee5de66ba28e945; __live_version__=%221.1.2.1736%22; live_use_vvc=%22false%22; SEARCH_RESULT_LIST_TYPE=%22single%22; xgplayer_user_id=795886229454; store-region=cn-sd; store-region-src=uid; my_rd=2; d_ticket=42bdd37da9893b9f392ce6129faf5a261d341; __ac_signature=_02B4Z6wo00f01oO2LkAAAIDDXO3dD2zcsn6DlirAAMZXj8iDvujauPLvi.SXT6siQmXXTdGXpZ8jZ126Nry6gbpelY9mj3qEVwu4raGAiRtPTbmR9rqe0UM7EJ7vljiNwfg63cvAH036hU5U35; passport_assist_user=CkEc-GhDXVz4819hwQGk_tg9fcUSad9EOJT4HT0Jzpb3ZQIYibeg37tn1sVjBw3hhrlHnq-fukLuPUbxgrEdgLiqVhpKCjwF4wK8G3d4_qFyfq6hxmjUwv_MloPgHKXX---7vVuWz0mik_E5wn5wemZbUzvWsjqlP1p8YMGVdx_bUeQQhvbXDRiJr9ZUIAEiAQNm-LL1; n_mh=f2T98qC_bXxSUAIlHU6iXq4YpTdHx0TSa0p9KKjv-_o; uid_tt=65b04977b02658ee389640f77df97b40; uid_tt_ss=65b04977b02658ee389640f77df97b40; sid_tt=03967f2304d6ae371f8a27e6d303c427; sessionid=03967f2304d6ae371f8a27e6d303c427; sessionid_ss=03967f2304d6ae371f8a27e6d303c427; s_v_web_id=verify_m1eji7r2_FDDnMk9U_r2GE_4TOW_9ZIh_AF8UfkYChtxL; SelfTabRedDotControl=%5B%5D; is_staff_user=false; passport_csrf_token=2b3b8cad764caeccda528e26a56fc2c5; passport_csrf_token_default=2b3b8cad764caeccda528e26a56fc2c5; douyin.com; xg_device_score=7.623778012680619; device_web_cpu_core=12; device_web_memory_size=8; architecture=amd64; IsDouyinActive=true; home_can_add_dy_2_desktop=%220%22; dy_swidth=1536; dy_sheight=864; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A864%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A12%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A100%7D%22; csrf_session_id=6d92ff4df078b73168ab286392d5dc3c; strategyABtestKey=%221729151749.347%22; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A1%7D%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D; publish_badge_show_info=%220%2C0%2C0%2C1729151749832%22; biz_trace_id=7aea13b9; passport_fe_beating_status=true; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCSVV6TmhXK0xoT2I2UUU2Zlp5a2FNTEFBcXY4ZkJrRTJMYkt3dm0vaVRjSHc0ZFVaNVA5Z1QxNWhNL2VSdzdibVpKa0VIcjNRb0NCNGMxZ2d6OGVOakE9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; sid_guard=03967f2304d6ae371f8a27e6d303c427%7C1729151749%7C5184000%7CMon%2C+16-Dec-2024+07%3A55%3A49+GMT; sid_ucp_v1=1.0.0-KDA2OTljMTI4N2Y1MDgzZjdmMzRkOGI4NGJlMmU5MTAxMWEwMTVhOWEKGwiugbDjuIzgBBCFhsO4BhjvMSAMOAZA9AdIBBoCbGYiIDAzOTY3ZjIzMDRkNmFlMzcxZjhhMjdlNmQzMDNjNDI3; ssid_ucp_v1=1.0.0-KDA2OTljMTI4N2Y1MDgzZjdmMzRkOGI4NGJlMmU5MTAxMWEwMTVhOWEKGwiugbDjuIzgBBCFhsO4BhjvMSAMOAZA9AdIBBoCbGYiIDAzOTY3ZjIzMDRkNmFlMzcxZjhhMjdlNmQzMDNjNDI3; odin_tt=972c9307c084dbfbc3418f755198104ef76ee1d0f654e0f5962f0b9881d5bb8d32e6bf2336cf6e837c2343805e384ff7ddde27ebe8bfb4d03ed6e0320e526c52"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "sec-ch-ua-platform": "Windows",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
    "referer": "https://www.douyin.com/search/%E5%AD%A6%E4%B9%A0?aid=d62c0903-7a41-4205-ac28-53d641e767c4&type=general",
    "priority": "u=1, i",
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "accept": "application/json, text/plain, */*",
    "dnt": "1",
    "Cookie": cookie
}


def get_webid():
    # if not self.WEBID:
    #     f=open("douyin.txt",mode="w",encoding="utf-8")
    #     url = 'https://www.douyin.com/?recommend=1'
    #     text = self.getHTML(url)
    #     f.write(text)
    #     f.close()
    #     pattern = r'\\"user_unique_id\\":\\"(\d+)\\"'
    #     match = re.search(pattern, text)
    #     if match:
    #         self.WEBID = match.group(1)
    WEBID = '7385074968550475275'
    return WEBID


def get_ms_token(randomlength=126):
    ms_token = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789='
    length = len(base_str) - 1
    for _ in range(randomlength):
        ms_token += base_str[random.randint(0, length)]
    return ms_token
    # ms_token="Zu4Q516lyCH2OasZZsCwjucmcMLRiQETxGi2MUHWwGNgM5WzkUAApaVPzEKDxzCTWsqyL84NslvOArM0OY9uUDMMvN6tJcCiN4em0yn9bfaJzDJYAMoNTuuEhdhFlA"


def get_page(page_id, csvwriter, cursor='0'):
    comment_cot = 0
    tem_dic = {}
    tem_dic.update(PARAMS2)
    tem_dic['msToken'] = get_ms_token(126)
    tem_dic['webid'] = get_webid()
    tem_dic['cursor'] = cursor
    params_str = urllib.parse.urlencode(PARAMS2) + "%3D%3D"
    tem_dic['aweme_id'] = page_id
    # "device_platform=webapp&aid=6383&channel=channel_pc_web&source=6&update_version_code=170400&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Edge&browser_version=126.0.0.0&browser_online=true&engine_name=Blink&engine_version=126.0.0.0&os_name=Windows&os_version=10&cpu_core_num=12&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=100&webid=7385074968550475275&verifyFp=verify_lyql8b0n_db9f3563_63bb_a0cc_e1a0_0178f90a76ea&fp=verify_lyql8b0n_db9f3563_63bb_a0cc_e1a0_0178f90a76ea&msToken=bktpWUL1ueGS3n61qPVYIxGMStKLLzivuWId0yd71dqGW_4JuorA0mT3ZpBu434jrnSXKcqbqAN6cCeGHRFFdynNFnDiTSU3jsc91E5ZwnC4hXAzuAgnEMdQ5sdzwQ%3D%3D&msToken=bktpWUL1ueGS3n61qPVYIxGMStKLLzivuWId0yd71dqGW_4JuorA0mT3ZpBu434jrnSXKcqbqAN6cCeGHRFFdynNFnDiTSU3jsc91E5ZwnC4hXAzuAgnEMdQ5sdzwQ%3D%3D"
    params_str = urllib.parse.urlencode(tem_dic)

    a_bogus = execjs.compile(open("douyin.js").read()).call("get_bogus", params_str, HEADERS['User-Agent'])
    tem_dic['a_bogus'] = a_bogus
    url2 = 'https://www.douyin.com/aweme/v1/web/comment/list/?'
    respond = requests.get(url2, headers=HEADERS, params=tem_dic)
    json_data2 = respond.json()
    comment = json_data2['comments']
    has_more = json_data2['has_more']
    cursor = json_data2['cursor']

    for j in range(len(comment)):
        dic = {
            'name': comment[j]['user']['nickname'],
            'content': comment[j]['text'],
            'time': str(datetime.fromtimestamp(comment[j]['create_time'])),
            'po': comment[j]['ip_label'],
            'like': comment[j]['digg_count']

        }
        csvwriter.writerow(dic.values())
        comment_cot += 1

    respond.close()
    return has_more, cursor, comment_cot

def get_main(csvwriter, main_cursor='0'):
    comment_cot = 0
    PARAMS1['offset'] = main_cursor
    url = "https://www.douyin.com/aweme/v1/web/general/search/single/?"
    respond = requests.get(url, headers=HEADERS, params=PARAMS1)
    json_data = respond.json()
    respond.close()
    clist = json_data['data']
    main_cursor = json_data['cursor']
    main_has_more = json_data['has_more']
    for i in range(len(clist)):
        try:
            aweme_id = clist[i]['aweme_info']['aweme_id']
            print(aweme_id)
            has_more, cursor, the_cot = get_page(aweme_id, csvwriter)
            comment_cot += the_cot
            while has_more == 1:
                time.sleep(random.random() + 1)
                has_more, cursor, the_cot = get_page(aweme_id, csvwriter, cursor)
                comment_cot += the_cot
        except:
            continue
    return main_has_more, main_cursor, comment_cot


if __name__ == "__main__":
    comment_cot = 0
    main_cursor = '0'
    goal_cot = 100000
    f = open("douyin情感.csv", mode="a", encoding='utf_8', newline='')
    csvwriter = csv.writer(f)
    COOKIES = cookies_to_dict(cookie)
    # print(r.COOKIES)-
    keyword = "情感"
    main_cursor = '0'
    PARAMS1['verifyFp'] = COOKIES.get('s_v_web_id', None)
    PARAMS1['fp'] = COOKIES.get('s_v_web_id', None)
    PARAMS1['webid'] = get_webid()
    PARAMS1['keyword'] = keyword
    PARAMS1['filter_selected'] = {"sort_type": "1", "publish_time": "0"}
    PARAMS1['offset'] = '0'
    PARAMS1['count'] = '15'
    if main_cursor == '0':
        main_has_more, main_cursor, the_cot = get_main(csvwriter)
        comment_cot += the_cot
    while comment_cot < goal_cot:
        time.sleep(random.random() + 1)
        print(main_cursor)
        main_has_more, main_cursor, the_cot = get_main(csvwriter, main_cursor)
        comment_cot += the_cot

    f.close()
