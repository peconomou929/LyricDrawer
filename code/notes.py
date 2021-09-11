note_dict = {
	"B#" : 0,
	"C" : 0,
	"C#" : 1,
	"Db" : 1,
	"D" : 2,
	"D#" : 3,
	"Eb" : 3,
	"E" : 4,
	"Fb" : 4,
	"E#" : 5,
	"F" : 5,
	"F#" : 6,
	"Gb" : 6,
	"G" : 7,
	"G#" : 8,
	"Ab" : 8,
	"A" : 9,
	"A#" : 10,
	"Bb" : 10,
	"B" : 11,
	"Cb" : 11
}

note_char = ":"
octave_up_char = ">"
octave_down_char = "<"
n_notes = 12

def from_token(token):
	# parses note and returns note_id, octave_change if valid note otherwise None
	if token[-1] == note_char:
		token = token[0:-1]
	else:
		return None
	octave_change = 0
	if token[0] == octave_up_char:
		note_name = token.lstrip(octave_up_char)
		octave_change = len(token) - len(note_name)
	elif token[0] == octave_down_char:
		note_name = token.lstrip(octave_down_char)
		octave_change =  len(note_name) - len(token) 
	else:
		note_name = token
	if note_name not in note_dict:
		return None
	else:
		return note_dict[note_name], octave_change

def get_next_note_level(current_level, note_id, octave_change):
	next_level = current_level + (note_id - current_level) % n_notes
	if octave_change == 0 and 2 * (next_level - current_level) > n_notes:
		next_level -= n_notes
	elif octave_change > 0 and next_level > current_level:
		next_level -= n_notes
	next_level += octave_change * n_notes
	return next_level

