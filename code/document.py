from graphics import *
from code import notes
from code import lyric_items
from code import text

'''
Any variable ending in _R means that it is relative to font size. 
To get the value in pixels, multiply by font size.
'''

class DocText:
	type_to_size = {
		"Title" : 14,
		"Header" : 12,
		"Normal" : 10
	}
	def __init__(self, text_type, text):
		self.text = text
		self.size = DocText.type_to_size[text_type]

class Gap:
	pass

class LyricLine:
	lyric_space_R = 0.6

	def __init__(self, line):
		tokens = line.split()
		items = []
		note_level = 0
		for token in tokens:
			note = notes.from_token(token)
			if note == None:
				items.append(lyric_items.from_token(token, note_level))
				if isinstance(items[-1], lyric_items.Rest):
					items[-2].connected = False
			else:
				note_id, octave_change = note
				note_level = notes.get_next_note_level(note_level, note_id, octave_change)
		self.lyric_items = items
	
	def get_width_R(self):
		result = sum(item.get_width_R() for item in self.lyric_items) 
		result += (len(self.lyric_items) - 1) * LyricLine.lyric_space_R
		return result

	def get_note_levels(self):
		non_rest_items = filter(lambda item : not isinstance(item, lyric_items.Rest), self.lyric_items)
		return map(lambda item : item.get_note_level(), non_rest_items)
	def get_note_level_range(self):
		highest = max(self.get_note_levels())
		lowest = min(self.get_note_levels())
		return highest - lowest
	def move(self, change):
		for item in self.lyric_items:
			item.move_note_level(change)
	def draw(self, win, ulx, uly, font_size):

		lyric_space = font_size * LyricLine.lyric_space_R
		section_margin = font_size * LyricSection.section_margin_R
		char_height = font_size * text.char_height_R
		note_level_dy = font_size * LyricSection.note_level_dy_R

		x = ulx + section_margin
		for i, item in enumerate(self.lyric_items):
			level = item.get_note_level()
			if level == None: level = 0
			y = uly - section_margin - char_height / 2 + note_level_dy * level
			if i > 0:
				x += lyric_space
				if prev_item.connected:
					Line(Point(prev_x, prev_y), Point(x, y)).draw(win)
			item.draw(win, x, y, font_size)	
			x += font_size * item.get_width_R()
			prev_x = x
			prev_y = y
			prev_item = item
	
	def get_spaced_note_levels(self, spacing):
		spaced_note_levels = []
		items = iter(self.lyric_items)
		item = next(items)
		note_level = item.get_note_level()
		item_x = item.get_width_R() + LyricLine.lyric_space_R
		x = 0
		while True:
			if x > item_x:
				item = next(items, None)
				if item == None: break
				note_level = item.get_note_level()
				item_x += item.get_width_R() + LyricLine.lyric_space_R
			else:
				spaced_note_levels.append(note_level)
				x += spacing
		return spaced_note_levels

class LyricSection:
	section_margin_R = 0.5
	note_levels_between_lines = 6
	note_level_dy_R = 0.3

	def __init__(self, lines):
		def get_min_diff(A, B):
			min_diff = None
			for a, b, in zip(A, B):
				if a == None or b == None:
					continue
				diff = a - b
				if min_diff == None or diff < min_diff:
					min_diff = diff
			return min_diff

		self.lyric_lines = [LyricLine(line) for line in lines]	
		spacing = 1

		for i, line in enumerate(self.lyric_lines):
			if i == 0:
				highest = max(line.get_note_levels())
				line.move(-highest)
			else:
				prev_line = self.lyric_lines[i-1]
				min_diff = get_min_diff(
					prev_line.get_spaced_note_levels(spacing),
					line.get_spaced_note_levels(spacing),
				)	
				line.move(min_diff - LyricSection.note_levels_between_lines)

	def get_height_R(self):
		highest = max(self.lyric_lines[0].get_note_levels())
		lowest = min(self.lyric_lines[-1].get_note_levels())
		return LyricSection.note_level_dy_R * (highest - lowest) + text.char_height_R + 2*LyricSection.section_margin_R
	def get_width_R(self):
		return max(line.get_width_R() for line in self.lyric_lines) + 2*LyricSection.section_margin_R
	def draw(self, win, ulx, uly, font_size):
		for line in self.lyric_lines:
			line.draw(win, ulx, uly, font_size)
		height = font_size * self.get_height_R() 
		width = font_size * self.get_width_R()
		Rectangle(Point(ulx, uly - height), Point(ulx + width, uly)).draw(win)

def remove_extension(file_path):
	if "." not in file_path:
		return file_path
	while not file_path[-1] == ".":
		file_path = file_path[0:-1]
	return file_path[0:-1]

class LyricDocument:
	def __init__(self, file_path):
		with open(file_path) as f:
			file_lines = [line.strip() for line in f.readlines()]

		score = []
		section_lines = []
		def dump(section_lines, score):
			if len(section_lines) > 0:
				score.append(LyricSection(section_lines))
				section_lines.clear()
			
		for line in file_lines:
			if len(line) == 0:
				dump(section_lines, score)
				score.append(Gap())
			else:
				first_word, rest = line.split(maxsplit = 1)
				text_type = first_word.rstrip(":")
				if text_type in {"Title", "Header", "Normal"}:
					dump(section_lines, score)
					score.append(DocText(text_type, rest))
				else:
					section_lines.append(line)
		dump(section_lines, score)
		self.target = remove_extension(file_path) + ".eps"
		self.score = score
	
	def get_max_section_width_R(self):
		sections = filter(lambda part : isinstance(part, LyricSection), self.score)
		return max(section.get_width_R() for section in sections)
	
	def get_width(self, lyric_size, margin):
		return lyric_size * self.get_max_section_width_R() + 2*margin

	def get_height(self, lyric_size, margin):
		result = margin
		for part in self.score:
			if isinstance(part, DocText):
				result += text.get_height(part.size)
			elif isinstance(part, Gap):
				result += margin
			elif isinstance(part, LyricSection):
				result += lyric_size * part.get_height_R()
			else:
				raise ValueError
			result += margin
		return result
		
	def draw(self, lyric_size, margin):
		width = self.get_width(lyric_size, margin)
		height = self.get_height(lyric_size, margin)
		win = GraphWin(" ", width, height)
		win.setCoords(0, 0, width, height)
		x = margin
		y = height - margin
		for part in self.score:
			if isinstance(part, DocText):
				text.place(part.text, part.size, x, y, "left_top").draw(win)
				y -= text.get_height(part.size)
			elif isinstance(part, Gap):
				y -= margin
			elif isinstance(part, LyricSection):
				part.draw(win, x, y, lyric_size)
				y -= lyric_size * part.get_height_R()
			else:
				raise ValueError
			y -= margin
		win.postscript(file = self.target, colormode = 'color')
		win.close()
