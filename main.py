from parlay import Parlay
from tolkien import Tolkien

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
		# "Kjør fremover i 5 sekunder",
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

def main():
	tolk = Tolkien()
	# while True:
	# 	inp = input("Tekst: ")
	# 	tolk.pos_info_dump(inp)
		# tolk.extract_commands(inp)
		# tolk.print_commands()
		# print(tolk.certainty_of_commands_parsing)

	w = Parlay()
	w.calibrate_recognizer()
	print("POWER ON!")
	while True:
		[ret_code, ret_data] = w.listen(time_limit = 3, timeout = 0.5)
		if ret_code == 1:
			speech_text = w.recognize(ret_data)
			tolk.extract_commands(speech_text)
			print(speech_text)
			tolk.print_commands()
		# elif ret_code == 0:
		# 	print(ret_code)


main()