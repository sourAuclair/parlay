from parlay import Parlay

def main():
	w = Parlay()
	w.calibrate_recognizer()
	while True:
		[ret_code, ret_data] = w.listen(timeout = 0.5, time_limit = 3)
		if ret_code == 1:
			speech_text = w.recognize(ret_data)
			print(speech_text)
		elif ret_code == 0:
			print(ret_code)
main()