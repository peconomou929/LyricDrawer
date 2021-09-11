import graphics

font = "courier"
char_width_R = 0.61
char_height_R = 1
loc_to_coords = {
	"left_bottom" : (-1, -1),
	"left_middle" : (-1, 0),
	"left_top": (-1, 1),
	"centre_bottom" : (0, -1),
	"centre" : (0, 0),
	"centre_top" : (0, 1),
	"right_bottom" : (1, -1),
	"right_middle" : (1, 0),
	"right_top" : (1, 1)
}

def get_width_R(text):
	return len(text) * char_width_R
def get_height_R():
	return char_height_R
def get_width(text, font_size):
	return get_width_R(text) * font_size
def get_height(font_size):
	return  get_height_R() * font_size
def place(text, font_size, x, y, loc = "centre"):
	coords = loc_to_coords[loc]
	width = get_width(text, font_size)
	height = get_height(font_size)
	centre = graphics.Point(x - coords[0] * width / 2, y - coords[1] * height / 2)
	message = graphics.Text(centre, text)
	message.setFace(font)
	message.setSize(font_size)
	return message

