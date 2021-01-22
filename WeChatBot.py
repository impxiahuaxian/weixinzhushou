# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
from utils.jsonToDict import JsonDict
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from bs4 import BeautifulSoup
from setting import *
from horoscope_setting import *
import time
import itchat
import requests
import json
import re
GRACE_PERIOD = 15 * 60
class info():
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
			'Chrome/67.0.3396.87 Safari/537.36',
	}
	'''
	登录状态验证
	'''
	'''
	通过查找好友来获取登录状态
	判断用户是否还在线
	'''
	def _online(self):
		try:
			if itchat.search_friends():
				return True
		except IndexError:
			return False
		return True

	def is_online(self,auto_login = True):
		if self._online():
			return True
		if not auto_login:
			return self._online()
		#尝试重新登录两次
		for _ in range(2):
			if os.environ.get('MODE') == 'server':
				itchat.auto_login(enabelCmdQR=2,hotReload = True)
			else:
				itchat.auto_login(hotReload = True)
			if self._online():
				print('登录成功')
				return True
		print('登录失败')
		return False
	'''
	天气状况获取
	'''

	def get_Weather_info(self,city_name):
		city_codes = JsonDict().jsonToDict()
		city_code = city_codes[city_name]
		weather_url = "http://t.weather.sojson.com/api/weather/city/{}".format(city_code)
		#print(url)
		response = requests.get(weather_url)
	#print(response.status_code)
		if response.status_code == 200 and response.json()['status']==200:
			weather =  response.json()
		#位置
			location = weather['cityInfo']['parent']+weather['cityInfo']['city']
		#当前时间
			today_time = datetime.now().strftime('%Y{y}%m{m}%d{d}').format(y='年',m='月',d='日')
		# 今日天气
			today_weather = weather.get('data').get('forecast')[0]
		#print(today_weather)
        # 今日天气注意
		#当前状况事项
			notice = today_weather.get('notice')
        #print(weather.get('data').get("wendu"))
			nowtemperature = "当前温度：{}°C".format(weather.get('data').get('wendu'))
			nowshidu = "湿度：{}".format(weather.get('data').get('shidu'))
			nowpm25 = 'PM2.5:{}'.format(weather.get('data').get('pm25'))

		# 温度
			high = today_weather.get('high')
			high_c = high[high.find(' ') + 1:]
			low = today_weather.get('low')
			low_c = low[low.find(' ') + 1:]
			temperature = "温度：{}~~{}".format(low_c,high_c)
		# 风
			fx = today_weather.get('fx')
			fl = today_weather.get('fl')
			wind = "{}:{}".format(fx,fl)
		# 空气指数
			aqi = today_weather.get('aqi')
			aqi = "空气质量：{}".format(aqi)

			#today_msg = f'{today_time}\n。\n当前天气状况 : \n{nowtemperature}, {nowshidu}, {nowpm25}\n{notice}\n{temperature}\n{wind}\n{aqi}\n'
			today_msg = "{}当前天气状况：\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(today_time,nowtemperature,nowshidu,nowpm25,notice,temperature,wind,aqi)
			print(today_msg)
			return today_msg
	'''
	每日一句内容获取
	'''

	def get_one_info(self):

		print('每日『一句』')
		word_url = 'http://wufazhuce.com/'
		resp = requests.get(word_url, headers = self.headers)
		if resp.status_code == 200:
			soup_texts = BeautifulSoup(resp.text,'lxml')
			every_msg = soup_texts.find('div', class_='fp-one-cita').text
			print(every_msg)  # 只取当天的这句
			return every_msg
		print('每日『一句』获取失败')
		return None

	def get_horoscope(self,horo_name,is_tomorrow = False):

		const_name = CONSTELLATION_DICT[horo_name]
		resp_horo = HORO_TOMORROW.format(const_name) if is_tomorrow \
			else HORO_TODAY.format(const_name)
		resp = requests.get(resp_horo, headers = self.headers)
		if resp.status_code == 200:
			html = resp.text
			lucky_num = re.findall(r'<label>幸运数字：</label>(.*?)</li>', html)[0]
			lucky_color = re.findall(r'<label>幸运颜色：</label>(.*?)</li>', html)[0]
			detail_horoscope = re.findall(r'<p><strong class="p1">.*?</strong><span>(.*?)<small>', html)[0]

			if is_tomorrow:
				detail_horoscope = detail_horoscope.replace('今天','明天')

			horo_text = '{name}{_date}运势\n【幸运颜色】{color}\n【幸运数字】{num}\n【综合运势】{horoscope}'.format(
				_date='明日' if is_tomorrow else '今日',
				name = horo_name,
				color = lucky_color,
				num = lucky_num,
				horoscope = detail_horoscope
				)
			print(horo_text)
			return horo_text
	'''
	定时器任务设置
	'''
	def start_today_info(self):

		city_name = config.get('city_name')
		weather_misson = self.get_Weather_info(city_name = city_name)
		word_misson = self.get_one_info()
		horo_name = config.get('horo_name')
		horo_misson = self.get_horoscope(horo_name = horo_name)
		today_misson = weather_misson + word_misson + horo_misson
		wechat_name = config.get('wechat_name')
		UserName = itchat.search_friends(wechat_name)
		if UserName:
			UserName = UserName[0]['UserName']
		else:
			UserName = 'filehelper'
		print("给{}发送的今日提醒为：\n{}".format(wechat_name,today_misson))
		if self.is_online(auto_login = True):
			itchat.send(today_misson,toUserName = UserName)
		time.sleep(5)
		#print(today_misson)
		#return today_misson
		print('今日提醒发送成功：')
	'''
	执行任务定时器
	'''

	def scheduler(self):
		#alarm_time = config.get('alarm_time').strip()
		#hour,minute = [int(x) for x in alarm_time.split(':')]
		scheduler = BackgroundScheduler()
		#后台调度器，适用于非阻塞的状态，在后台独立运行
		scheduler.add_job(self.start_today_info,'cron',hour = '17',minute = '51',misfire_grace_time = GRACE_PERIOD)
		scheduler.start()
'''
机器人消息内容获取
'''

def get_response(text):
	params = {
        'appid': "ab6e2fd3f0056863324d736e5864bf5d",
        'userid': "M5",
        'spoken': text
    }
	url = 'https://api.ownthink.com/bot'
	resp = requests.get(url, params=params)
	if resp.status_code == 200:
		#print(resp.text)
		content_dict = resp.json()
		data = content_dict['data']
		if data['type'] == 5000:
			reply_text = data['info']['text']
			return reply_text
'''
查看微信好友性别

def search_male():
	friends = itchat.get_friends(update=True)[0:]
	male = female = other = 0
	for i in friends[1:]:
		sex = i["Sex"]
		if sex == 1:
			male += 1
		elif sex == 2:
			female += 1
		else:
			other += 1
	total = len(friends[1:])
	print("男性数目为：{}".format(male))
	print("女性数目为：{}".format(female))
	print("其他性别：{}".format(other))
'''

'''
自动回复功能
'''

@itchat.msg_register(itchat.content.TEXT)
def bot_reply(msg):
	default_reply = '我：' + msg['Text'] #返回发送者发送的消息
	#print("开始自动回复")
	reply = get_response(msg['Text'])
	return reply or default_reply

if __name__ == '__main__':
	itchat.auto_login()
	info().scheduler()
	#search_male()
	itchat.run()