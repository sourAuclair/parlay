import spacy
from spacy import displacy
from spacy.language import Language
from spacy.lang.nb import Norwegian
from spacy.lemmatizer import Lemmatizer

class Tolkien:
	def __init__(self, lang = 'no'):
		self.nlp = spacy.load('nb_core_news_sm')
		self.commands_in_text = []
		self.commands_structure = commands.get('no')
		self.certainty_of_commands_parsing = 1

	def set_lang(self, lang):
		if lang == 'no':
			self.nlp = spacy.load(commands.get('no'))
		elif lang == 'en':
			self.nlp = spacy.load(commands.get('en'))

	def extract_commands(self, sentence):
		self.commands_in_text = []
		sent = self.nlp(sentence)
		number_of_commands = 0
		number_of_correct_lemmas = 0
		for token in sent:
			if token.pos_ == "NUM":
				self.commands_in_text.append(token.text)
				continue
			for com in self.commands_structure:
				if token.lemma_.capitalize() == com:
					number_of_commands += 1
					self.commands_in_text.append(com)
					if token.pos_ == self.commands_structure.get(com)[0]:
						number_of_correct_lemmas += 1
		# self.certainty_of_commands_parsing = number_of_correct_lemmas / number_of_commands

	def thr_extract_commands(self, action_list, sentence):
		self.commands_in_text = []
		sent = self.nlp(sentence)
		number_of_commands = 0
		number_of_correct_lemmas = 0
		for token in sent:
			if token.pos_ == "NUM":
				self.commands_in_text.append(token.text)
				continue
			for com in self.commands_structure:
				if token.lemma_.capitalize() == com:
					number_of_commands += 1
					self.commands_in_text.append(com)
					if token.pos_ == self.commands_structure.get(com)[0]:
						number_of_correct_lemmas += 1
		# self.certainty_of_commands_parsing = number_of_correct_lemmas / number_of_commands
		action_list.insert(0, [2, self.stringify_commands()])

	def pos_info_dump(self, sentence):
		sent = self.nlp(sentence)
		for token in sent:
			print(token.text, token.lemma_, token.pos_, token.dep_, token.is_alpha, token.is_stop)

	def print_commands(self):
		print(self.commands_in_text)

	def stringify_commands(self):
		string_of_commands = ""
		for com in self.commands_in_text:
			string_of_commands += (com + " ")
		return string_of_commands

	def format_command_list(self):
		string_of_commands = ""
		for com in self.commands_in_text:
			string_of_commands += (com + ";")
		return string_of_commands


commands = {
	'no' : {
		"Hei" : [ "INTJ", 0],
		"Kjøre" : [ "VERB", 0 ],
		"Stoppe" : [ "VERB", 0],
		"Snu" : [ "VERB", 0],
		"Frem" : [ "ADP", 1 ],
		"Fram" : [ "ADP", 1 ],
		"Fremover" : [ "ADP", 1 ], # NOT CURRENTLY WORKING
		"Baklengs" : [ "ADV", 1 ],
		"Høyre" : [ "NOUN", 2],
		"Venstre" : [ "NOUN", 2],
		"Minutt" : [ "NOUN", 3],
		"Sekund" : [ "NOUN", 3],
		"Millisekund" : [ "NOUN", 3],
		"Grad" : [ "NOUN", 3]
	}
}