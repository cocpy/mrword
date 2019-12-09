import uuid
import requests
import hashlib
import time
import json
import logging

# pip install beautifulsoup4
from bs4 import BeautifulSoup


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}


def get_audio(name, url):
    """获取url中的读音并写入MP3文件夹中"""
    logging.info(url)
    r = requests.get(url, headers=headers)
    logging.info('requests is running')
    if r.status_code == 200:
        with open("mp3/%s.mp3" % name, "wb") as code:
            code.write(r.content)
            logging.info("download %s mp3 successfully" % name)
    else:
        logging.info('aidUrl to return error: %d' % r.status_code)


class OfficialAPI:
    """调用有道智云api"""

    YOU_DAO_URL = 'http://openapi.youdao.com/api'
    # 请重新申请
    APP_KEY = '30af9686870c0150'
    APP_SECRET = 'O7PPrAezLEPLFV6WMCyGyRDjkljlfVBZqi'

    @staticmethod
    def encrypt(sign_str):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(sign_str.encode('utf-8'))
        return hash_algorithm.hexdigest()

    @staticmethod
    def truncate(q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

    def do_request(self, data):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(self.YOU_DAO_URL, data=data, headers=headers)

    def connect(self, q):
        data = {}
        data['from'] = 'EN'
        data['to'] = 'zh-CHS'
        data['signType'] = 'v3'
        curtime = str(int(time.time()))
        data['curtime'] = curtime
        salt = str(uuid.uuid1())
        sign_str = self.APP_KEY + self.truncate(q) + salt + curtime + self.APP_SECRET
        sign = self.encrypt(sign_str)
        data['appKey'] = self.APP_KEY
        data['q'] = q
        data['salt'] = salt
        data['sign'] = sign
        response = self.do_request(self, data)
        content_json = json.loads(response.content)
        # error_code为0时，表示查询正常
        error_code = content_json['errorCode']

        if error_code == '0':
            # 英式音标
            phonetic = '[' + content_json['basic']['phonetic'] + ']'
            # 解释
            explains_list = content_json['basic']['explains']
            explains = "\n".join(explains_list)
            # 源语言发音地址
            origin_speak_url = content_json['speakUrl']

            get_audio(q, origin_speak_url)

            context = {'code': error_code, 'phonetic': phonetic, 'explains': explains}
        else:
            context = {'code': error_code}
        return context


class ReptileYouDao:

    @staticmethod
    def get_base_message(word):

            logging.info('is ready to send http request')
            response = requests.get('http://dict.youdao.com/search?q=%s&keyfrom=new-fanyi.smartResult' % word, headers=headers)
            logging.info(response)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')  # 结构化文本soup
            try:
                explains = soup.find(name='div', attrs={'class': 'trans-container'}).get_text().strip()  # 释义
                explains = explains[:explains.find('[')]  # 截取掉多余的字符串
                from utils.common import sub_str_len, instance_new_line
                explains = sub_str_len(explains, 3)
                phonetic = soup.find(name='span', attrs={'class': 'phonetic'}).get_text()  # 音标
                examples = soup.find(name='div', attrs={'class': 'examples'}).get_text()  # 例句
                examples_en = instance_new_line(examples.split('\n')[1], 50)
                examples_cn = instance_new_line(examples.split('\n')[2], 50, is_cn=True)
                # http://media.shanbay.com/audio/us/%s.mp3 扇贝单词美式发音
                # http://media.shanbay.com/audio/uk/%s.mp3 扇贝单词英式发音
                # http://dict.youdao.com/dictvoice?audio=%s 有道单词发音
                url = 'http://media.shanbay.com/audio/uk/%s.mp3' % word
                get_audio(word, url)  # 发音
                # print(examples.get_text())  # 获取标签内文本
                context = {'error_code': 0, 'phonetic': phonetic, 'explains': explains, 'examples_en': examples_en, 'examples_cn': examples_cn}
                print(context)
            except Exception:
                logging.info('%s can\'t import' % word)
                context = {'error_code': 404}
            return context


if __name__ == '__main__':
    # OfficialAPI.connect(OfficialAPI,'good')
    ReptileYouDao.get_base_message('good')
