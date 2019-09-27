import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import webbrowser
import random

# настройки
opts = {
	"alias": ('кеша','кеш','инокентий','иннокентий','кишун','киш',
			  'кишаня','кяш','кяша','кэш','кэша'),
	"tbr": ('скажи','расскажи','покажи','сколько','произнеси', 'запусти', 'открой'),
	"cmds": {
		"ctime": ('текущее время','сейчас времени','который час', 'сколько времени'),
		"radio": ('включи музыку','воспроизведи радио','включи радио'),
		'info_about':('кто ты', 'что ты такое', 'как тебя зовут'),
		"internet_chrome": ('запусти хром', 'открой хром', 'google chrome'),
		"internet_firefox": ('запусти мозилу', 'открой мозилу', 'Mazilla Firefox'),
		"stupid1": ('расскажи анекдот','рассмеши меня','ты знаешь анекдоты')
	}
}

jockesToUser = []

def HelperSay(whatSpeek):
	print(whatSpeek)
	speak_engine.say(whatSpeek)
	speak_engine.runAndWait()
	speak_engine.stop()

def ListenUserVoice(recognizer, audio):
	try:
		voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
		print("Распознано: " + voice)
		if voice.startswith(opts["alias"]):	#обращение к помошнику
			cmd = voice
			for i in opts['alias']:
				cmd = cmd.replace(i, "").strip()
			for i in opts['tbr']:
				cmd = cmd.replace(i, "").strip()
			
			cmd = RecognizeCommand(cmd)
	
			ExecuteCommand(cmd['cmd'])
	
	except sr.UnknownValueError:
		print("[log] Голос не распознан!")
	except sr.RequestError as e:
		print("[log] Неизвестная ошибка, проверьте интернет!")

def RecognizeCommand(cmd):
	RC = {'cmd': '', 'percent': 0}
	for c, v in opts['cmds'].items():
		for x in v:
			vrt = fuzz.ratio(cmd, x)
			if vrt > RC['percent']:
				RC['cmd'] = c
				RC['percent'] = vrt
	return RC

def GetJocke():
	file = open('Jockes.txt', 'r', encoding='utf-8')
	for line in file:
		jockesToUser.append(line)
	HelperSay(random.choice(jockesToUser))

def ExecuteCommand(cmd):
	if cmd == 'ctime':
		# сказать текущее время
		now = datetime.datetime.now()
		HelperSay("Сейчас " + str(now.hour) + ":" + str(now.minute))
   
	elif cmd == 'radio':
		# воспроизвести радио
		os.system("D:\\Jarvis\\res\\radio_record.m3u")
   
	elif cmd == 'stupid1':
		# рассказать анекдот
		GetJocke()
	
	elif cmd == 'internet_chrome':
		# запустить google chrome
		HelperSay("Запускаю Гугл Хром")
		chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
		webbrowser.get(chrome_path).open('https://www.google.com/')

	elif cmd == 'internet_firefox':
		# запустить firefox
		HelperSay("Запускаю Firefox")
		firefox_path = 'C:/Program Files/Mozilla Firefox/firefox.exe %s'
		webbrowser.get(firefox_path).open('https://www.google.com/')

	elif cmd == 'info_about':
		HelperSay("Я голосовой ассистент, который написан студентом группы ПИ 16 а Сёмиком Александром на Python с использованием простых библиотек.")
	else:
		print('Команда не распознана, повторите!')

speak_engine = pyttsx3.init()

HelperSay("Добрый день, повелитель")
HelperSay("Кеша слушает")

#Запуск программы
r = sr.Recognizer()
m = sr.Microphone(device_index = 2)	# active microphone index
r.adjust_for_ambient_noise(source, duration = 1)

while True:
	with m as source:
		print("Слушаю...")
		audio = r.listen(source)
	ListenUserVoice(r, audio)