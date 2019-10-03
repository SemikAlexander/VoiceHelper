import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import webbrowser
import random
import platform

# настройки
options = {
	"alias": ('кеша','кеш','инокентий','иннокентий','кишун','киш',
			  'кишаня','кяш','кяша','кэш','кэша'),
	"tbr": ('скажи','расскажи','покажи','сколько','произнеси', 'запусти', 'открой'),
	"cmds": {
		"ctime": ('текущее время','сейчас времени','который час', 'сколько времени'),
		"radio": ('включи музыку','воспроизведи радио','включи радио'),
		"explorer": ('мой компьютер', 'проводник'),
		'info_about':('кто ты', 'что ты такое'),
		"internet_chrome": ('запусти хром', 'открой хром', 'google chrome'),
		"internet_firefox": ('запусти мозилу', 'открой мозилу', 'Mazilla Firefox'),
		"game_start": ('игрушку','игру'),
		"stupid1": ('расскажи анекдот','рассмеши меня','ты знаешь анекдоты'),
		"excuse": ('ты такой медленный', 'тормознутый', 'медленный', 'тугодум'),
		"goodbye": ('прощай','до свидания','до скорого','аривидерчи','пока')
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
		if voice.startswith(options["alias"]):	#обращение к помошнику
			cmd = voice
			for i in options['alias']:
				cmd = cmd.replace(i, "").strip()
			for i in options['tbr']:
				cmd = cmd.replace(i, "").strip()
			
			cmd = RecognizeCommand(cmd)
	
			ExecuteCommand(cmd['cmd'])
	
	except sr.UnknownValueError:
		print("[log] Голос не распознан!")
	except sr.RequestError as e:
		print("[log] Неизвестная ошибка, проверьте интернет!")

def RecognizeCommand(cmd):
	RC = {'cmd': '', 'percent': 0}
	for c, v in options['cmds'].items():
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
		HelperSay("Одну минуту")
		try:
			firefox_path = 'C:/Program Files/Mozilla Firefox/firefox.exe %s'
			webbrowser.get(firefox_path).open('https://pcradio.ru/')
		except webbrowser.Error as errorFireFox:
			try:
				webbrowser.get(chrome_path).open('https://pcradio.ru/')
			except webbrowser.Error as errorChrome:
				print("Something go wrong...")
   
	elif cmd == 'stupid1':
		# рассказать анекдот
		GetJocke()
	
	elif cmd == 'internet_chrome':
		# запустить google chrome
		HelperSay("Запускаю Гугл Хром")
		webbrowser.get(chrome_path).open('https://www.google.com/')

	elif cmd == 'internet_firefox':
		# запустить firefox
		HelperSay("Запускаю Мозилу")
		firefox_path = 'C:/Program Files/Mozilla Firefox/firefox.exe %s'
		webbrowser.get(firefox_path).open('https://www.google.com/')
	
	elif cmd == 'explorer':
		HelperSay("Открываю проводник")
		os.system(f'start {os.path.realpath("C:/")}')

	elif cmd == 'game_start':
		HelperSay("Запускаю игру")
		os.system(f'start RacerGame.py')

	elif cmd == 'excuse':
		HelperSay("Дело всё в том, что я, как Вам уже известно, а может быть и нет, написан на Питоне, а он не гарантирует высокую скорость обработки данных. Да и многое зависит от железа, которым Вы располагаете.")
		HelperSay("Если хотите, чтобы я работал быстрее, попросите моего создателя меня переписать на тот же Си + +. Вот только, скорее всего, он вряд ли согласится.")
	
	elif cmd == 'info_about':
		HelperSay("Я голосовой ассистент, который написан студентом группы ПИ 16 а Сёмиком Александром на Python с использованием простых библиотек.")
	
	elif cmd == 'goodbye':
		HelperSay("До свиданья!")
		os.abort()
	
	else:
		print('Команда не распознана, повторите!')

speak_engine = pyttsx3.init()

voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[3].id)

HelperSay("Добрый день, повелитель")
HelperSay("Кеша слушает")

#Запуск программы

if platform.system() == 'Linux':
	chrome_path = '/usr/bin/google-chrome %s'
elif platform.system() == 'Windows':
	chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
else:
	chrome_path = 'open -a /Applications/Google\ Chrome.app %s'		#MacOS has name "Darwin"

r = sr.Recognizer()
m = sr.Microphone(device_index = 2)	# active microphone index

while True:
	with m as source:
		print("Слушаю...")
		r.adjust_for_ambient_noise(source, duration = 1)
		audio = r.listen(source)
	ListenUserVoice(r, audio)