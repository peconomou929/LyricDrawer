import graphics
from code import text

hold_char = "-"
rest_char = "."
tone_char = "*"
disconnect_char = ";"
hold_width_R = 0.5
rest_width_R = 0.3
tone_radius_R = 0.1

def from_token(token, note_level):
	if set(token) == {rest_char}:
		return Rest(len(token))

	if token[-1] == disconnect_char:
		token = token[0:-1]
		connected = False
	else:
		connected = True

	if set(token) == {hold_char}:
		return Hold(note_level, len(token), connected)
	elif token == tone_char:
		return Tone(note_level, connected)
	else: 
		return Word(note_level, token, connected)

class Word:
	def __init__(self, note_level, word, connected):
		self.connected = connected
		self.word = word
		self.note_level = note_level
	def get_note_level(self):
		return self.note_level
	def move_note_level(self, change):
		self.note_level += change
	def get_width_R(self):
		return text.get_width_R(self.word)
	def draw(self, win, x, y, font_size):
		text.place(self.word, font_size, x, y, "left_middle").draw(win)

class Tone:
	def __init__(self, note_level, connected):
		self.note_level = note_level
		self.connected = connected
	def get_note_level(self):
		return self.note_level
	def move_note_level(self, change):
		self.note_level += change
	def get_width_R(self):
		return 0
	def draw(self, win, x, y, font_size):
		radius = font_size * tone_radius_R
		circle = graphics.Circle(graphics.Point(x, y), radius).draw(win)
		circle.setFill("black")
		
class Hold:
	def __init__(self, note_level, duration, connected):
		self.note_level = note_level
		self.duration = duration
		self.connected = connected
	def get_note_level(self):
		return self.note_level
	def move_note_level(self, change):
		self.note_level += change
	def get_width_R(self):
		return hold_width_R * self.duration
	def draw(self, win, x, y, font_size):
		width = font_size * self.get_width_R()
		graphics.Line(graphics.Point(x, y), graphics.Point(x + width, y)).draw(win)
		
class Rest:
	def __init__(self, duration):
		self.duration = duration
		self.connected = False
	def get_note_level(self):
		return None
	def move_note_level(self, change):
		pass
	def get_width_R(self):
		return rest_width_R * self.duration
	def draw(self, win, x, y, font_size):
		pass

