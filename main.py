from parlay import Parlay
from tolkien import Tolkien
import time
from os import system
import platform
import concurrent.futures

# Gyldige setninger så langt + ulike varianter.
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

main()
