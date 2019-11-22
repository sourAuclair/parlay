from parlay import Parlay
from tolkien import Tolkien
import time
from os import system
import platform
import concurrent.futures

# Gyldige setninger så langt. 
sent = [
		"Hei",
		"Kjør frem i 5 sekunder",
		"Kan du kjøre frem?",
		"Jeg vil at du skal kjøre frem i 5 sekunder",
		"Jeg vil at du skal kjøre frem i 5 minutter",
		"Kjør frem i 5 sekunder. Stopp etterpå.",
		"Kjør fram i 5 sekunder",
		"Kan du kjøre fram?",
		"Jeg vil at du skal kjøre fram i 5 sekunder",
		"Jeg vil at du skal kjøre fram i 5 minutter",
		"Kjør fram i 5 sekunder. Stopp etterpå.",
		"Kjør baklengs i 5 sekunder",
		"Kan du kjøre baklengs?",
		"Jeg vil at du skal kjøre baklengs i 5 sekunder",
		"Jeg vil at du skal kjøre baklengs i 5 minutter",
		"Kjør baklengs i 5 sekunder. Stopp etterpå.",
		"Stopp nå",
		"Snu til høyre",
		"Snu til venstre",
		"Snu mot høyre",
		"Snu mot venstre",
		"Snu deg 5 grader til høyre",
		"Snu deg 5 grader til venstre",
		"Kjør frem i 10 sekunder. Etterpå skal du stoppe."
	]

"""
0 Listen --Not currently in use--
1 Tolk
2 Phrase
3 Recognize
"""

corpus = """   ______                           \n  / ____/___  _________  __  _______\n / /   / __ \\/ ___/ __ \\/ / / / ___/\n/ /___/ /_/ / /  / /_/ / /_/ (__  ) \n\\____/\\____/_/  / .___/\\__,_/____/  \n               /_/                  """

def clear():
	sys = platform.system()
	if sys == "Windows":
		_ = system("cls")
	else:
		_ = system("clear")

def main():
	parlay = Parlay()
	clear()
	parlay.run(time_limit = 5, timeout = 0.5)
	# parlay.calibrate_recognizer()
	# tolk = Tolkien()

	# time_limit = 5
	# timeout = 0.5

	# action_queue = []
	# clear()
	# print(corpus)
	# with concurrent.futures.ThreadPoolExecutor(max_workers = 10) as executor:
	# 	listen_thread = executor.submit(parlay.thr_listen(action_queue, time_limit, timeout))
	# 	print("POWER ON")
	# 	while True:
	# 		if listen_thread.done():
	# 			listen_thread = executor.submit(parlay.thr_listen(action_queue, time_limit, timeout))
	# 		if action_queue:
	# 			action = action_queue.pop(0)
	# 			# Currently unused
	# 			if action[0] == 0:
	# 				print(action[0])
	# 				listen_thread = executor.submit(parlay.thr_listen(action_queue, action[1], action[2]))
	# 			# Recognize
	# 			elif action[0] == 3:
	# 				print(action[0])
	# 				recognize_thread = executor.submit(parlay.thr_recognize(action_queue, action[1]))
	# 			# Tolk --Extract commands--
	# 			elif action[0] == 1:
	# 				print(action[0])
	# 				tolk_thread = executor.submit(tolk.thr_extract_commands(action_queue, action[1]))
	# 			# Phrase
	# 			elif action[0] == 2:
	# 				# print(action[0], ": ", action[1])
	# 				# Check that the phrase is not the empty string
	# 				if action[1]:
	# 					# parlay.speak(action[1])
	# 					print(action[1])
	# 		else:
	# 			time.sleep(0.1)

main()