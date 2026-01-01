import pygame
import os

BASE_IMG_PATH = 'assets/images/'
BASE_FONT_PATH = 'assets/font/'
BASE_TEXT_PATH = 'assets/text/'

def load_font(path, size=50):
    font = pygame.font.Font(BASE_FONT_PATH + path, size)
    return font

def load_image(path):
    print("image is loaded")
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name).convert())
    return images

def load_text(path):
    text = []
    f = open(BASE_TEXT_PATH + path, "r")
    line = f.readline()

    while line.find('#END#'):
        print(line)
        text.append(line)
        line = f.readline()

    f.close()
    return text

def scale_pos(game, mouse_pos, scale_locking= [True, False]): ## this takes the mouse position and translates it to the position so that it works when we resize a window where the elements sclae with the window size
    input_screen = (game.screen.get_width(), game.screen.get_height())
    target_screen = (game.display.get_width(), game.display.get_height())

    ## self.display.get_height()*self.screen.get_width() / self.display.get_width()

    if scale_locking[0]:

        if scale_locking[1]:
            result_mouse_positionx = (mouse_pos[0]/input_screen[0]) * target_screen[0]
            result_mouse_positiony = (mouse_pos[1]/input_screen[1]) * target_screen[1]
        else:
            result_mouse_positionx = (mouse_pos[0]/input_screen[0]) * target_screen[0]
            result_mouse_positiony = mouse_pos[1] / (target_screen[1] * input_screen[0]/target_screen[0]) * target_screen[1]
    else:
        
        if scale_locking[1]:
            result_mouse_positionx = mouse_pos[0] / (target_screen[0] * input_screen[1]/target_screen[1]) * target_screen[0]
            result_mouse_positiony = (mouse_pos[1]/input_screen[1]) * target_screen[1]
        else:
            result_mouse_positionx = mouse_pos[0]
            result_mouse_positiony = mouse_pos[1]

    return (result_mouse_positionx, result_mouse_positiony)

def drawText(surface, text:str, color, rect:pygame.Rect, font: pygame.font, stretch_to_contain= False, aa=True, bkg=None, lineSpacing = -2, alignment = 'left'):
    y = rect.top

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    ## print(text)

    while text:
        i = 1
        # print(i)
        # print(text[i])

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            if stretch_to_contain:
                rect.height = y + fontHeight - rect.top
            else:
                break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            if text[i-1] == "\n":
                # print(i-1)
                text = text.replace("\n", ' ', 1)
                break
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            last_word_index = text.rfind(" ", 0, i) + 1
        
        if last_word_index != 0:
            i = last_word_index ## yeah I know that this results in some really janky textboxes, but just don't do really vertically thin textboxes

        # render the line and blit it to the surface (we can set the surface to None to check if the text fits or how much we need to stretch it or whatever)
        if surface != None:

            if bkg != None:
                image: pygame.Surface = font.render(text[:i], 1, color, bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(text[:i], aa, color)

            if alignment == 'left':
                surface.blit(image, (rect.left, y))
            elif alignment == 'center':
                surface.blit(image, image.get_rect(midtop = (rect.centerx, y)))
            elif alignment == 'right':
                surface.blit(image, image.get_rect(topright = (rect.left, y)))

        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]
        # print(f'remaining text is {text}')
        # input()
    
    if stretch_to_contain:
        return rect.height
    else:
        return text

def alphabet_converter(number):
	# The alphabet numbering system is just base 26 but you turn the 0 into the Z and take one index from the letter to the left
	column_key = ''
	base_26_num = []
	num_to_char = {'0':'0', '1':'A', '2':'B', '3':'C', '4':'D', '5':'E', '6':'F', '7':'G', '8':'H', '9':'I', '10':'J', '11':'K', '12':'L', '13':'M', '14':'N', '15':'O', '16':'P', '17':'Q', '18':'R', '19':'S', '20':'T', '21':'U', '22':'V', '23':'W', '24':'X', '25':'Y', '26':'Z'}
	index = 0

	while pow(26, index) <= number :
		index += 1
	
	for i in range(0, index + 1):

		char_index = int((number)/pow(26, (index - i)))
		# print("From", required_number, "we get", char_index)
		number = number % pow(26, (index - i))

		base_26_num.append(char_index)

    # print(base_26_num)

	# This code is a process to turn the 0's to 'Z's
	carrying_over = True
	while carrying_over:
		carrying_over = False
		for i in range(0, len(base_26_num)):
			if base_26_num[i] == 0 and i >= 2:
				if i-1 != 0:
					base_26_num[i-1] -= 1
				base_26_num[i] = 26
				carrying_over = True
				break


	# print(base_26_num)
	
	while base_26_num[0] == 0:
		base_26_num.pop(0)

	for index in base_26_num:
		column_key = column_key + num_to_char[str(index)]

	return column_key

def draw_alpha(surf: pygame.Surface, shape_dict: dict):
    surface = pygame.Surface((surf.get_width(), surf.get_height()), pygame.SRCALPHA)

    if shape_dict['type'] =='circle':
        if not 'width' in shape_dict.keys():
            shape_dict['width'] = 0
        if not 'draw_top_right' in shape_dict.keys():
            shape_dict['draw_top_right'] = False
        if not 'draw_top_left' in shape_dict.keys():
            shape_dict['draw_top_left'] = False
        if not 'draw_bottom_left' in shape_dict.keys():
            shape_dict['draw_bottom_left'] = False
        if not 'draw_bottom_right' in shape_dict.keys():
            shape_dict['draw_bottom_right'] = False
        pygame.draw.circle(surface, shape_dict['color'], shape_dict['center'], shape_dict['radius'], shape_dict['width'], shape_dict['draw_top_right'], shape_dict['draw_top_left'], shape_dict['draw_bottom_left'], shape_dict['draw_bottom_right'])
    elif shape_dict['type'] == 'line':
        if not 'width' in shape_dict.keys():
            shape_dict['width'] = 1
        pygame.draw.line(surface, shape_dict['color'], shape_dict['start_pos'], shape_dict['end_pos'], shape_dict['width'])
    else:
        print('ERROR INVALID SHAPE TYPE')

    surf.blit(surface, (0, 0))

def profile():
    pass

class Animation(object):
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0 

    def copy(self): 
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
            # This increments the frame^ and this^ is to loop it back to 0 when it reaches the end
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame / self.img_duration)]