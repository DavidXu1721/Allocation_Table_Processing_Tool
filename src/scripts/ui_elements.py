import sys
import os
import pygame
from .utils import drawText, load_font, scale_pos
import math
import random

def close_window(game, windowID): 
    for window in game.ui_elements['windows']:
        if window.windowID == windowID:
            game.ui_elements['windows'].remove(window)

def change_window_pos_and_dim(game, windowID, position= None, dimensions= None): 
    for window in game.ui_elements['windows']:
        if window.windowID == windowID:
            if position != None:
                window.position = position
            if dimensions != None:
                window.dimensions = dimensions
                window.surface = pygame.Surface(window.dimensions, pygame.SRCALPHA, 32)
            

def update_ui_elements(game):
    mouse_on_window = False

    for window in reversed(game.ui_elements['windows'].copy()): ## the purpose of reversing is the ensure that the buttons that get updates are the ones that are blitted on top of everything
            
        if window.window_type == 'focused':      ## We honestly should remake this code, but all in all, just make sure that the focused window is to the right of the ui_elements['windows']
            print('asdddd')
            mouse_on_window = True

            if window.get_rect().collidepoint(scale_pos(game, pygame.mouse.get_pos(), game.scale_lock)):
                
                for element in reversed(window.elements.copy()):
                    if element['type'] == 'button':
                        if element['content'].get_rect(offset=window.position).collidepoint(scale_pos(game, pygame.mouse.get_pos(), game.scale_lock)):
                            if not game.player_inputs['mouse'][0]:
                                element['content'].state = 'hover'
                        else: 
                            element['content'].state = 'idle'              
                break
        else:                                                                                   
            if window.get_rect().collidepoint(scale_pos(game, pygame.mouse.get_pos(), game.scale_lock)):
                mouse_on_window = True
                for element in reversed(window.elements.copy()):
                    if element['type'] == 'button':
                        if element['content'].get_rect(offset=window.position).collidepoint(scale_pos(game, pygame.mouse.get_pos(), game.scale_lock)):
                            if not game.player_inputs['mouse'][0]:
                                element['content'].state = 'hover'
                        else: 
                            element['content'].state = 'idle'               
                break
    
    for window in reversed(game.ui_elements['windows'].copy()):
        for element in reversed(window.elements.copy()):
            if element['type'] == 'dynamic_textbox':
                ## print('textbox update')
                element['content'].update()
            if element['type'] == 'input_textbox':
                element['content'].update()

    if not mouse_on_window:

        for window in reversed(game.ui_elements['windows'].copy()):
            for element in reversed(window.elements.copy()):
                if element['type'] == 'button':
                
                    element['content'].state = 'idle'
    
    for button in reversed(game.ui_elements['buttons'].copy()):

        if button.get_rect().collidepoint(scale_pos(game, pygame.mouse.get_pos(), game.scale_lock)) and not mouse_on_window:
            if not game.player_inputs['mouse'][0]:
                button.state = 'hover'
        else: 
            button.state = 'idle'

    return mouse_on_window

def render_ui(game):
    for button in game.ui_elements['buttons'].copy():
        button.render()
    for window in game.ui_elements['windows'].copy(): ## we need to render the buttons before the windows, obviously
        if window.window_type != 'focused':
            window.render()

    for window in game.ui_elements['windows'].copy(): ## we render 'alert' windows above everything else
        if window.window_type == 'focused':
            s = pygame.Surface((game.display.get_width(), game.display.get_height()))  # the size of your rect
            s.set_alpha(128)                # alpha level
            s.fill((0, 0, 0))               # this fills the entire surface
            game.display.blit(s, (0,0))    # (0,0) are the top-left coordinates
            window.render()

def ui_process_mouse_button_down(game, mouse_button, mouse_on_window):
    clicked_button = False

    match mouse_button: ## I'm considering mousewheel up as 4 and mousewheel down as 5 as god intended
        
        case 1:
            ## we first need to deactivate all the input boxes
            for window in reversed(game.ui_elements['windows'].copy()):
                for element in reversed(window.elements.copy()):
                    if element['type'] == 'input_textbox':
                        element['content'].active = False

            ## then we handle the rest of the mouse click
            if not mouse_on_window:
                for button in reversed(game.ui_elements['buttons'].copy()):
                    
                    if button.get_rect().collidepoint(scale_pos(game, pygame.mouse.get_pos(), game.scale_lock)) and button.state == 'hover':
                        button.state = 'clicked'
                        clicked_button = True
                        break

            else:
                focused_window = False

                for window in reversed(game.ui_elements['windows'].copy()):
                    if window.window_type == 'focused':
                        focused_window = True

                        for element in reversed(window.elements.copy()):
                            if element['type'] == 'button':
                                if element['content'].get_rect(offset=window.position).collidepoint(scale_pos(game, pygame.mouse.get_pos(), game.scale_lock)) and element['content'].state == 'hover':
                                    element['content'].state = 'clicked'
                                    clicked_button = True
                                    break
                            if element['type'] == 'switch':
                                if element['content'].get_rect(offset=window.position).collidepoint(scale_pos(game, pygame.mouse.get_pos(), game.scale_lock)):
                                    switch_options = [1, 0]
                                    element['content'].state = switch_options[element['content'].state]
                                    break
                            if element['type'] == 'input_textbox':
                                if element['content'].get_rect(offset=window.position).collidepoint(scale_pos(game, pygame.mouse.get_pos(), game.scale_lock)):
                                    element['content'].active = True
                                    element['content'].text_cursor_location = len(element['content'].txt_content)
                                    clicked_button = True
                                    break
                        break
                
                if not focused_window:
                    for window in reversed(game.ui_elements['windows'].copy()):

                        for element in reversed(window.elements.copy()):
                            if element['type'] == 'button':
                                if element['content'].get_rect(offset=window.position).collidepoint(scale_pos(game, pygame.mouse.get_pos(), game.scale_lock)) and element['content'].state == 'hover':
                                    element['content'].state = 'clicked'
                                    clicked_button = True
                                    break
                            if element['type'] == 'switch':
                                if element['content'].get_rect(offset=window.position).collidepoint(scale_pos(game, pygame.mouse.get_pos(), game.scale_lock)):
                                    switch_options = [1, 0]
                                    element['content'].state = switch_options[element['content'].state]
                                    break
                            if element['type'] == 'input_textbox':
                                if element['content'].get_rect(offset=window.position).collidepoint(scale_pos(game, pygame.mouse.get_pos(), game.scale_lock)):
                                    element['content'].active = True
                                    element['content'].text_cursor_location = len(element['content'].txt_content)
                                    clicked_button = True
                                    break
                        
                        if window.get_rect().collidepoint(scale_pos(game, pygame.mouse.get_pos(), game.scale_lock)):
                            break

            if not clicked_button:
                for window in reversed(game.ui_elements['windows'].copy()):

                    for element in reversed(window.elements.copy()):
                        if element['type'] == 'dynamic_textbox':
                            if element['content'].ready_for_next_stage:
                                element['content'].stage += 1
                                element['content'].txt_progress = 0
                                if element['content'].stage >= len(element['content'].txt_content): ## my patience has withered away a long time ago, from now on this game will be coded like a piece of modern art
                                    return {'type': 'textbox_conclusion', 'actions': [['remove_window', window]]}
                            else:
                                element['content'].txt_progress = len(element['content'].txt_content[element['content'].stage]) * 60

        case 4:
            if mouse_on_window:
                focused_window = False

                for window in reversed(game.ui_elements['windows'].copy()):
                    if window.window_type == 'focused':
                        focused_window = True
                        break
                
                if not focused_window:
                    for window in reversed(game.ui_elements['windows'].copy()):
                        
                        if window.window_type == 'scrollable' and window.get_rect().collidepoint(scale_pos(game, pygame.mouse.get_pos(), game.scale_lock)):
                            shift_distance = min(game.settings['scroll_speed'], 5 - window.get_element_limit('top'))

                            window.shift_elements(y = shift_distance)

        case 5:
            if mouse_on_window:
                focused_window = False

                for window in reversed(game.ui_elements['windows'].copy()):
                    if window.window_type == 'focused':
                        focused_window = True
                        break
                
                if not focused_window:
                    for window in reversed(game.ui_elements['windows'].copy()):
                        
                        if window.window_type == 'scrollable' and window.get_rect().collidepoint(scale_pos(game, pygame.mouse.get_pos(), game.scale_lock)):
                            shift_distance = max(-game.settings['scroll_speed'], window.get_rect().height - 5 - window.get_element_limit('bottom'))

                            window.shift_elements(y = shift_distance)

        case _:
            print("More mouse functions TBA")

def ui_process_keyboard_button_down(game, event):

    for window in reversed(game.ui_elements['windows'].copy()):
        for element in reversed(window.elements.copy()):
            if element['type'] == 'input_textbox' and element['content'].active:
                if event.key == pygame.K_BACKSPACE and element['content'].text_cursor_location != 0:
                    element['content'].txt_content = element['content'].txt_content[:element['content'].text_cursor_location -1] + element['content'].txt_content[element['content'].text_cursor_location:]
                    element['content'].text_cursor_location -= 1
                elif event.key == pygame.K_RETURN:
                    element['content'].active = False
                elif event.key == pygame.K_LEFT:
                    element['content'].text_cursor_location = max(0, element['content'].text_cursor_location - 1)
                    print('you went left')
                elif event.key == pygame.K_RIGHT:
                    element['content'].text_cursor_location = min(len(element['content'].txt_content), element['content'].text_cursor_location + 1)   
                    print('you went right') 
                elif (event.key != pygame.K_RSHIFT and event.key != pygame.K_LSHIFT) and element['content'].char_limit != None and len(element['content'].txt_content) < element['content'].char_limit:
                    element['content'].txt_content = element['content'].txt_content[:element['content'].text_cursor_location] + event.unicode + element['content'].txt_content[element['content'].text_cursor_location:]
                    element['content'].text_cursor_location += 1
                elif (event.key != pygame.K_RSHIFT and event.key != pygame.K_LSHIFT) and element['content'].char_limit == None:
                    element['content'].txt_content = element['content'].txt_content[:element['content'].text_cursor_location] + event.unicode + element['content'].txt_content[element['content'].text_cursor_location:]
                    element['content'].text_cursor_location += 1

                break

def extract_data(game, ui_elementID):

    for button in reversed(game.ui_elements['buttons'].copy()):
        if button.buttonID == ui_elementID:
            pass        ## There isn't really a point in doing this kind of extraction, but we might as well add it in

    for window in reversed(game.ui_elements['windows'].copy()):
        
        for element in reversed(window.elements.copy()):
            if element['type'] == 'button':
                if element['content'].buttonID == ui_elementID:
                    pass        ## Likewise, there isn't really a point in doing this
            if element['type'] == 'switch':
                if element['content'].switchID == ui_elementID:
                    return element['content'].state
            if element['type'] == 'input_textbox':
                if element['content'].input_boxID == ui_elementID:
                    return element['content'].txt_content
                
def set_progress(game, ui_elementID, progress):
    for window in reversed(game.ui_elements['windows'].copy()):
        
        for element in reversed(window.elements.copy()):
            if element['type'] == 'loading_bar':
                if element['content'].loading_barID == ui_elementID:
                    element['content'].progress = progress
                
def close_window(game, windowID):
    for window in reversed(game.ui_elements['windows'].copy()):
        if window.windowID == windowID:
            game.ui_elements['windows'].remove(window)
            return None
    
    print("ERROR: WINDOW NOT FOUND")

def add_window_element(game, windowID, element):
    for window in reversed(game.ui_elements['windows'].copy()):

        if window.windowID == windowID:

            match element['type']:
                case 'textbox':
                    window.elements.append(element)
                case 'textbox_big':
                    window.elements.append(element)
                case 'label':
                    window.elements.append(element)
                case 'button':
                    window.elements.append({'type': 'button', 'content': Button(window.game, window.surface, element['dimensions'], element['position'], element['bg_color'], element['bd_color'], element['txt_color'], element['txt_font'], element['txt_align'], element['txt_content'], element['elements'], element['buttonID'])})
                case 'switch/off':
                    window.elements.append({'type': 'switch', 'content': Switch(window.game, window.surface, element['dimensions'], element['position'], txt_font=element['txt_font'], txt_content=element['txt_content'], switchID=element['switchID'])})
                case 'loading_bar/default':
                    window.elements.append({'type': 'loading_bar', 'content': LoadingBar(window.game, window.surface, dimensions= element['dimensions'], position= element['position'], loading_barID= element['loading_barID'])})
                case 'dynam_textbox/default':
                    window.elements.append({'type': 'dynamic_textbox', 'content': DynamicTextBox(window.game, window.surface, element['dimensions'], element['position'], txt_content= element['txt_content'])}) 
                case 'input_textbox/default':
                    window.elements.append({'type': 'input_textbox', 'content': InputBox(window.game, window.surface, element['dimensions'], element['position'], txt_content= element['txt_content'], input_boxID= element['input_boxID'], char_limit= element['char_limit'])}) 
                case 'input_textbox/vert':
                    window.elements.append({'type': 'input_textbox', 'content': InputBox(window.game, window.surface, element['dimensions'], element['position'], txt_content= element['txt_content'], input_box_orientation= 'vertical', input_boxID= element['input_boxID'], char_limit= element['char_limit'])}) 
                case 'input_textbox/hori_colored':
                    window.elements.append({'type': 'input_textbox', 'content': InputBox(window.game, window.surface, element['dimensions'], element['position'], bd_color= element['bd_color'], txt_color = element['txt_color'], txt_content= element['txt_content'], input_boxID= element['input_boxID'], char_limit= element['char_limit'])}) 
                case 'input_textbox/vert_colored':
                    window.elements.append({'type': 'input_textbox', 'content': InputBox(window.game, window.surface, element['dimensions'], element['position'], bd_color= element['bd_color'], txt_color = element['txt_color'], txt_content= element['txt_content'], input_box_orientation= 'vertical', input_boxID= element['input_boxID'], char_limit= element['char_limit'])}) 
                case 'input_textbox/small':
                    window.elements.append({'type': 'input_textbox', 'content': InputBox(window.game, window.surface, element['dimensions'], element['position'], txt_font= 'input_box_small', txt_content= element['txt_content'],  input_boxID= element['input_boxID'], char_limit= element['char_limit'])}) 

def remove_window_element(game, windowID, ui_elementID):
    for window in reversed(game.ui_elements['windows'].copy()):

        if window.windowID == windowID:

            for element in reversed(window.elements.copy()):
                if element['type'] == 'button':
                    if element['content'].buttonID == ui_elementID:
                        window.elements.remove(element)
                        return None
                if element['type'] == 'switch':
                    if element['content'].switchID == ui_elementID:
                        window.elements.remove(element)
                        return None
                if element['type'] == 'loading_bar':
                    if element['content'].loading_barID == ui_elementID:
                        window.elements.remove(element)
                        return None
                if element['type'] == 'input_textbox':
                    if element['content'].input_boxID == ui_elementID:
                        window.elements.remove(element)
                        return None
    
    print("ERROR: WINDOW NOT FOUND")

def check_window(game, windowID):
    for window in reversed(game.ui_elements['windows'].copy()):
        if window.windowID == windowID:
            return True
        
    return False
            
###### ELEMENT FORMATS ######

# {'type': 'textbox', 'dimensions': (200, 100), 'position': (0, 0), 'color': 'black', 'text': "*Add text here*"}
# {'type': 'button', 'dimensions': (200, 100), 'position': (0, 0), 'bg_color': 'black', 'bd_color': 'white', 'txt_color': 'white', 'txt_font': 'button_default', 'txt_align': 'center', 'txt_content': '*Add text here*', 'elements': [], 'buttonID': 'UNASSIGNED'}

class Window(object):
    def __init__(self, game, 
                 parent_surf, 
                 windowID= '',
                 window_type= 'default',
                 dimensions= (100, 100), 
                 position= (20, 20), 
                 bg_color= 'black', 
                 bd_color= 'white',
                 elements= []):
        self.game = game
        self.parent_surf = parent_surf
        self.windowID = windowID
        self.window_type = window_type

        self.dimensions = dimensions
        if position == 'centered':
            self.position = ((self.parent_surf.get_width() - self.dimensions[0])* 0.5, (self.parent_surf.get_height() - self.dimensions[1])* 0.5)
        else:
            self.position = position
        self.bg_color = bg_color
        self.bd_color = bd_color
        
        self.surface = pygame.Surface(self.dimensions, pygame.SRCALPHA, 32)
        
        self.elements = []                 # I think this might be kind of retarded

        for element in elements:
            match element['type']:
                case 'textbox':
                    self.elements.append(element)  ## {'type': 'textbox', 'color': '**text color**', 'text': '**text content**', 'dimensions': **textbox dimensions**, 'position': **textbox position**}
                case 'textbox_big':
                    self.elements.append(element)
                case 'label':
                    self.elements.append(element)
                case 'button':
                    self.elements.append({'type': 'button', 'content': Button(self.game, self.surface, element['dimensions'], element['position'], element['bg_color'], element['bd_color'], element['txt_color'], element['txt_font'], element['txt_align'], element['txt_content'], element['elements'], element['buttonID'])})
                case 'switch/off':
                    self.elements.append({'type': 'switch', 'content': Switch(self.game, self.surface, element['dimensions'], element['position'], txt_font=element['txt_font'], txt_content=element['txt_content'], switchID=element['switchID'])})
                case 'switch/on':
                    self.elements.append({'type': 'switch', 'content': Switch(self.game, self.surface, element['dimensions'], element['position'], txt_font=element['txt_font'], txt_content=element['txt_content'], state= 1,switchID=element['switchID'])})
                case 'loading_bar/default':
                    self.elements.append({'type': 'loading_bar', 'content': LoadingBar(self.game, self.surface, dimensions= element['dimensions'], position= element['position'], loading_barID= element['loading_barID'])})
                case 'dynam_textbox/default':
                    self.elements.append({'type': 'dynamic_textbox', 'content': DynamicTextBox(self.game, self.surface, element['dimensions'], element['position'], txt_content= element['txt_content'])}) 
                case 'input_textbox/default':
                    self.elements.append({'type': 'input_textbox', 'content': InputBox(self.game, self.surface, element['dimensions'], element['position'], txt_content= element['txt_content'], input_boxID= element['input_boxID'], char_limit= element['char_limit'])}) 
                case 'input_textbox/vert':
                    self.elements.append({'type': 'input_textbox', 'content': InputBox(self.game, self.surface, element['dimensions'], element['position'], txt_content= element['txt_content'], input_box_orientation= 'vertical', input_boxID= element['input_boxID'], char_limit= element['char_limit'])}) 
                case 'input_textbox/hori_colored':
                    self.elements.append({'type': 'input_textbox', 'content': InputBox(self.game, self.surface, element['dimensions'], element['position'], bd_color= element['bd_color'], txt_color = element['txt_color'], txt_content= element['txt_content'], input_boxID= element['input_boxID'], char_limit= element['char_limit'])}) 
                case 'input_textbox/vert_colored':
                    self.elements.append({'type': 'input_textbox', 'content': InputBox(self.game, self.surface, element['dimensions'], element['position'], bd_color= element['bd_color'], txt_color = element['txt_color'], txt_content= element['txt_content'], input_box_orientation= 'vertical', input_boxID= element['input_boxID'], char_limit= element['char_limit'])}) 
                case 'input_textbox/small':
                    self.elements.append({'type': 'input_textbox', 'content': InputBox(self.game, self.surface, element['dimensions'], element['position'], txt_font= 'input_box_small', bd_color= element['bd_color'], txt_color = element['txt_color'], txt_content= element['txt_content'],  input_boxID= element['input_boxID'], char_limit= element['char_limit'])}) 

    def update(self):
        pass ## this may be needed in the future

    def get_rect(self, offset= (0, 0)):
        return pygame.Rect(self.position[0] + offset[0], self.position[1] + offset[1], self.dimensions[0], self.dimensions[1])
    
    def get_element_limit(self, direction):
        """This function finds the right/left/top/bottommost point of all the elements in the window"""

        match direction: ## here i and j are variables for the equations to calculate the exact position of the left, right, top and bottom points of each element, 
                         ## where 'i' determines it it's horizontal(0) or vertical(1) and 'j' determines if we need to add the width/height or not. It's just a quick and simple way of doing it imo
            case 'left': 
                i, j = 0, 0
            case 'right':
                i, j = 0, 1
            case 'top':
                i, j = 1, 0
            case 'bottom':
                i, j = 1, 1
            case _:
                print('ERROR: INVALID DIRECTION')

        list_of_limits = []
        
        for element in self.elements:
            if element['type'] == 'textbox':  ## Alright, this probably should be a class, but whatever man, like it's not like textboxes are interactable or anything
                list_of_limits.append(element['position'][i] + j * element['dimensions'][i])
            elif element['type'] == 'textbox_big':  ## Alright, this probably should be a class, but whatever man, like it's not like textboxes are interactable or anything
                list_of_limits.append(element['position'][i] + j * element['dimensions'][i])
            elif element['type'] == 'label':
                displayed_text = self.game.fonts[element['txt_font']].render(element['txt_content'], False, element['txt_color'])
                dimensions = (displayed_text.get_rect().width, displayed_text.get_rect().height)
                list_of_limits.append(element['position'][i] + j * dimensions[i])
            elif element['type'] in ['button', 'switch', 'loading_bar', 'dynamic_textbox', 'input_textbox']:
                list_of_limits.append(element['content'].position[i] + j * element['content'].dimensions[i])
            else:
                print("ERROR: INVALID ELEMENT TYPE!!!")

        if len(list_of_limits) == 0:
            return 0

        if j == 0:
            return min(list_of_limits)
        else:
            return max(list_of_limits)
        
    def shift_elements(self, x=0, y=0):
        for element in self.elements:
            if element['type'] == 'textbox': 
                element['position'] = (element['position'][0] + x, element['position'][1] + y) ## [i] + j * element['dimensions'][i])
            elif element['type'] == 'textbox_big': 
                element['position'] = (element['position'][0] + x, element['position'][1] + y) ## [i] + j * element['dimensions'][i])
            elif element['type'] == 'label':
                element['position'] = (element['position'][0] + x, element['position'][1] + y) 
            elif element['type'] in ['button', 'switch', 'loading_bar', 'dynamic_textbox', 'input_textbox']:
                element['content'].position = (element['content'].position[0] + x, element['content'].position[1] + y)
            else:
                print("ERROR: INVALID ELEMENT TYPE!!!")

    def render(self):
        self.surface.fill(pygame.Color(0, 0, 0, 0))

        if self.bg_color != 'transparent':
            pygame.draw.rect(self.surface, self.bg_color, pygame.Rect(0, 0, self.dimensions[0], self.dimensions[1]))

        for element in self.elements: ## MORE STUFF TBA (remember to do this for the other classes)
            if element['type'] == 'textbox':  ## Alright, this probably should be a class, but whatever man, like it's not like textboxes are interactable or anything
                drawText(self.surface, 
                         element['text'], 
                         element['color'], 
                         pygame.Rect(element['position'][0], element['position'][1], element['dimensions'][0], element['dimensions'][1]), 
                         self.game.fonts['textbox'])
            elif element['type'] == 'textbox_big': 
                drawText(self.surface, 
                         element['text'], 
                         element['color'], 
                         pygame.Rect(element['position'][0], element['position'][1], element['dimensions'][0], element['dimensions'][1]), 
                         self.game.fonts['label'])
            elif element['type'] == 'label':
                displayed_text = self.game.fonts[element['txt_font']].render(element['txt_content'], False, element['txt_color'])
                self.surface.blit(displayed_text, displayed_text.get_rect(topleft = element['position']))
            elif element['type'] in ['button', 'switch', 'loading_bar', 'dynamic_textbox', 'input_textbox']:
                element['content'].render()
            else:
                print("ERROR: INVALID ELEMENT TYPE!!!")

        if self.window_type == 'scrollable':
            pygame.draw.rect(self.surface, self.bd_color, 
                             pygame.Rect(self.dimensions[0] - 10, 
                                         (-self.get_element_limit('top')/(self.get_element_limit('bottom') - self.get_element_limit('top') + 10)) * self.dimensions[1], 10, self.dimensions[1] * self.dimensions[1]/(self.get_element_limit('bottom') - self.get_element_limit('top') + 10)))

        if self.bd_color != 'transparent':
            pygame.draw.rect(self.surface, self.bd_color, pygame.Rect(0, 0, self.dimensions[0], self.dimensions[1]), width= 1)

        if self.position == 'mouse':
            self.parent_surf.blit(self.surface, self.position)
        else:
            self.parent_surf.blit(self.surface, self.position)


class Button(object):
    def __init__(self, game, 
                 parent_surf,
                 dimensions= (100, 100), 
                 position= (20, 20), 
                 bg_color= {'idle': 'black',
                            'hover': (30, 30, 30),
                            'clicked': 'white'}, 
                 bd_color= {'idle': 'white',
                            'hover': 'black',
                            'clicked': 'black'}, 
                 txt_color= {'idle': 'white',
                            'hover': 'white',
                            'clicked': 'black'},
                 txt_font= 'button_default',
                 txt_align= 'center',                         ## alright, look, I'm gonna have to stop this overengineering at some point, I'm not going to abstract textboxes into every button and instead make it intrinsic
                 txt_content= '',
                 elements= [],
                 buttonID= 'UNASSIGNED'                       ## this is what gets returned to the game when the button is pressed
                 ):
        
        self.game = game
        self.parent_surf = parent_surf

        self.dimensions = dimensions
        self.position = position
        self.bg_color = bg_color
        self.bd_color = bd_color
        self.txt_color = txt_color
        self.txt_font = txt_font
        self.txt_align = txt_align
        self.txt_content = txt_content
        self.elements = elements
        self.buttonID = buttonID 

        self.state = 'idle'

        self.surface = pygame.Surface(self.dimensions, pygame.SRCALPHA, 32) ## I don't think the buttons need a surface, but, then I realised that some buttons might need images (like icons), and stuff, so yeah, whatever. this might bite me in the ass later down the line. but it's not like I'm gonna be spamming buttons on an idle game.
    
    def get_rect(self, offset= (0, 0)):                     ## I personally think this is a clever way of doing this, trhe offset would be set to the position of the window, if the button was in a window
        return pygame.Rect(self.position[0] + offset[0], self.position[1] + offset[1], self.dimensions[0], self.dimensions[1])

    def render(self):
        self.surface.fill(pygame.Color(0, 0, 0, 0))
        
        if self.bg_color != 'transparent':
            pygame.draw.rect(self.surface, self.bg_color[self.state], pygame.Rect(0, 0, self.dimensions[0], self.dimensions[1]))

        button_text = self.game.fonts[self.txt_font].render(self.txt_content, False, self.txt_color[self.state])

        match self.txt_align:
            case 'center':
                self.surface.blit(button_text, button_text.get_rect(center = (self.dimensions[0] * 0.5, self.dimensions[1] * 0.5)))
            
            case 'left':
                self.surface.blit(button_text, button_text.get_rect(midleft = (5, self.dimensions[1] * 0.5)))

            case _: ## I'll add mroe cases when I need to
                print("ERROR: INVALID ELEMENT TYPE!!!")
                assert False

        for element in self.elements: ## MORE STUFF TBA (remember to do this for the other classes)
            if element['type'] == 'textbox':  ## Alright, this probably should be a class, but whatever man, like it's not like textboxes are interactable or anything
                drawText(self.surface, 
                         element['text'], 
                         element['color'], 
                         pygame.Rect(element['position'][0], element['position'][1], element['dimensions'][0], element['dimensions'][1]), 
                         self.game.fonts['textbox'])

            elif element['type'] == 'button':
                pass
            else:
                print("ERROR: INVALID ELEMENT TYPE!!!")
                assert False

        if self.bd_color != 'transparent':
            pygame.draw.rect(self.surface, self.bd_color[self.state], pygame.Rect(0, 0, self.dimensions[0], self.dimensions[1]), width= 1)

        self.parent_surf.blit(self.surface, self.position)

class Switch(object):
    def __init__(self, game,
                 parent_surf, 
                 dimensions= (100, 100), 
                 position= (20, 20), 
                 bg_color= ['black', 'white'], 
                 bd_color= ['white', 'black'],
                 txt_color= ['white', 'black'],
                 txt_font= 'textbox',                   
                 txt_content= '', 
                 txt_align= 'center',
                 state= 0,
                 elements= [],
                 switchID= 'UNASSIGNED'           
                 ):
        self.game = game
        self.parent_surf = parent_surf

        self.dimensions = dimensions
        self.position = position
        self.bg_color = bg_color
        self.bd_color = bd_color
        self.txt_color = txt_color
        self.txt_font = txt_font
        self.txt_content = txt_content
        self.txt_align = txt_align
        self.elements = elements
        self.switchID = switchID

        self.state = state

        self.surface = pygame.Surface(self.dimensions, pygame.SRCALPHA, 32)
    
    def get_rect(self, offset= (0, 0)):                     ## I personally think this is a clever way of doing this, trhe offset would be set to the position of the window, if the button was in a window
        return pygame.Rect(self.position[0] + offset[0], self.position[1] + offset[1], self.dimensions[0], self.dimensions[1])

    def render(self):
        self.surface.fill(pygame.Color(0, 0, 0, 0))
        
        if self.bg_color != 'transparent':
            pygame.draw.rect(self.surface, self.bg_color[self.state], pygame.Rect(0, 0, self.dimensions[0], self.dimensions[1]))

        button_text = self.game.fonts[self.txt_font].render(self.txt_content, False, self.txt_color[self.state])

        match self.txt_align:
            case 'center':
                self.surface.blit(button_text, button_text.get_rect(center = (self.dimensions[0] * 0.5, self.dimensions[1] * 0.5)))
            
            case 'left':
                self.surface.blit(button_text, button_text.get_rect(midleft = (5, self.dimensions[1] * 0.5)))

            case _: ## I'll add mroe cases when I need to
                print("ERROR: INVALID ELEMENT TYPE!!!")
                assert False

        for element in self.elements: ## MORE STUFF TBA (remember to do this for the other classes)
            if element['type'] == 'textbox':  ## Alright, this probably should be a class, but whatever man, like it's not like textboxes are interactable or anything
                drawText(self.surface, 
                         element['text'], 
                         element['color'], 
                         pygame.Rect(element['position'][0], element['position'][1], element['dimensions'][0], element['dimensions'][1]), 
                         self.game.fonts['textbox'])

            elif element['type'] == 'button':
                pass
            else:
                print("ERROR: INVALID ELEMENT TYPE!!!")
                assert False

        if self.bd_color != 'transparent':
            pygame.draw.rect(self.surface, self.bd_color[self.state], pygame.Rect(0, 0, self.dimensions[0], self.dimensions[1]), width= 1)

        self.parent_surf.blit(self.surface, self.position)


class DynamicTextBox(object):
    def __init__(self, game,
                 parent_surf, 
                 dimensions= (100, 100), 
                 position= (20, 20), 
                 bg_color= 'transparent', 
                 bd_color= 'transparent',
                 txt_color= 'white',
                 txt_font= 'textbox',                   
                 txt_content= '',            
                 ):
        self.game = game
        self.parent_surf = parent_surf

        self.dimensions = dimensions
        self.position = position
        self.bg_color = bg_color
        self.bd_color = bd_color
        self.txt_color = txt_color
        self.txt_font = txt_font
        self.txt_content = txt_content

        self.stage = 0
        self.visible_txt = ''
        self.txt_progress = 0
        self.ready_for_next_stage = False

        self.surface = pygame.Surface(self.dimensions, pygame.SRCALPHA, 32)

    def update(self):
        self.ready_for_next_stage = False
        if self.txt_progress/60 <= len(self.txt_content[self.stage]):
            self.txt_progress += self.game.settings['text_speed']
            self.visible_txt = self.txt_content[self.stage][:-1][:int(self.txt_progress/60)]
            print(self.visible_txt)
        else:
            self.ready_for_next_stage = True

    def render(self):
        self.surface.fill(pygame.Color(0, 0, 0, 0))

        if self.bg_color != 'transparent':
            pygame.draw.rect(self.surface, self.bg_color, pygame.Rect(0, 0, self.dimensions[0], self.dimensions[1]))
        
        drawText(self.surface, 
                    self.visible_txt, 
                    self.txt_color, 
                    pygame.Rect(0, 0, self.dimensions[0], self.dimensions[1]), self.game.fonts[self.txt_font])

        if self.bd_color != 'transparent':
            pygame.draw.rect(self.surface, self.bd_color, pygame.Rect(0, 0, self.dimensions[0], self.dimensions[1]), width= 1)

        self.parent_surf.blit(self.surface, self.position)

class InputBox(object): ## So far, all instances of input boxes must be in a window
    
    def __init__(self, game,
                 parent_surf, 
                 dimensions= (100, 100), 
                 position= (20, 20), 
                 bg_color= 'transparent', 
                 bd_color= 'white',
                 txt_color= 'white',
                 txt_font= 'input_box_default',                   
                 txt_content= '',
                 input_box_orientation= 'horizontal',
                 input_boxID= 'UNASSIGNED',
                 char_limit= None
                 ):
        
        self.game = game
        self.parent_surf = parent_surf

        self.dimensions = dimensions
        self.position = position
        self.bg_color = bg_color
        self.bd_color = bd_color
        self.txt_color = txt_color
        self.txt_font = txt_font
        self.txt_content = txt_content
        self.input_box_orientation = input_box_orientation
        self.input_boxID = input_boxID
        self.char_limit = char_limit

        self.active = False
        self.insert_marker_timer = 0
        self.text_cursor_location = 0

        self.surface = pygame.Surface(self.dimensions, pygame.SRCALPHA, 32)

    def get_rect(self, offset= (0, 0)):                     ## I personally think this is a clever way of doing this, trhe offset would be set to the position of the window, if the button was in a window
        return pygame.Rect(self.position[0] + offset[0], self.position[1] + offset[1], self.dimensions[0], self.dimensions[1])
        
    def update(self):
        self.insert_marker_timer += 1

    def render(self):
        self.surface.fill(pygame.Color(0, 0, 0, 0))

        if self.bg_color != 'transparent':
            pygame.draw.rect(self.surface, self.bg_color, pygame.Rect(0, 0, self.dimensions[0], self.dimensions[1]))
        
        if self.input_box_orientation == 'horizontal':
            displayed_text = self.game.fonts[self.txt_font].render(self.txt_content, False, self.txt_color)
            positioning_text = self.game.fonts[self.txt_font].render(self.txt_content[:self.text_cursor_location], False, self.txt_color)
        elif self.input_box_orientation == 'vertical':
            displayed_text = self.game.fonts[self.txt_font].render(self.txt_content + ' ', False, self.txt_color)
            positioning_text = self.game.fonts[self.txt_font].render(self.txt_content[:self.text_cursor_location] + ' ', False, self.txt_color)

        if self.input_box_orientation == 'horizontal':
            self.surface.blit(displayed_text, displayed_text.get_rect(topleft = (5, 5)))
            if self.insert_marker_timer % 20 > 10 and self.active: 
                ## print(displayed_text.get_rect(topleft = (5, 5)).right)
                ## print(displayed_text.get_rect(topleft = (5, 5)).top)
                ## print(displayed_text.get_rect(topleft = (5, 5)).height)
                pygame.draw.rect(self.surface, self.txt_color, pygame.Rect(positioning_text.get_rect(topleft = (5, 5)).right - 2, 
                                                                           positioning_text.get_rect(topleft = (5, 5)).top, 
                                                                           5, positioning_text.get_rect(topleft = (5, 5)).height))
        elif self.input_box_orientation == 'vertical':
            rotated_displayed_text = pygame.transform.rotate(displayed_text, 90)
            rotated_positioning_text = pygame.transform.rotate(positioning_text, 90)
            self.surface.blit(rotated_displayed_text, rotated_displayed_text.get_rect(bottomleft = (5, self.dimensions[1] - 5)))
            if self.insert_marker_timer % 20 > 10 and self.active: 
                ## print(displayed_text.get_rect(topleft = (5, 5)).right)
                ## print(displayed_text.get_rect(topleft = (5, 5)).top)
                ## print(displayed_text.get_rect(topleft = (5, 5)).height)

                print(rotated_displayed_text.get_rect(bottomleft = (5, self.dimensions[1] - 5)))
                ## print(pygame.Rect(rotated_displayed_text.get_rect(bottomleft = (5, self.dimensions[1] - 5)).left, 
                ##                                                            rotated_displayed_text.get_rect(bottomleft = (5, self.dimensions[1] - 5)).top - 2, 
                ##                                                            rotated_displayed_text.get_rect(topleft = (5, 5)).width, 5))
                ## pygame.draw.rect(self.surface, self.txt_color, rotated_displayed_text.get_rect(bottomleft = (5, self.dimensions[1] - 5)))
                pygame.draw.rect(self.surface, self.txt_color, pygame.Rect(rotated_positioning_text.get_rect(bottomleft = (5, self.dimensions[1] - 5)).left, 
                                                                           rotated_positioning_text.get_rect(bottomleft = (5, self.dimensions[1] - 5)).top + 2, 
                                                                           displayed_text.get_rect(topleft = (5, 5)).height, 5))

        if self.bd_color != 'transparent':
            pygame.draw.rect(self.surface, self.bd_color, pygame.Rect(0, 0, self.dimensions[0], self.dimensions[1]), width= 1)

        self.parent_surf.blit(self.surface, self.position)

class LoadingBar(object): ## So far, all instances of input boxes must be in a window
    
    def __init__(self, game,
                 parent_surf, 
                 dimensions= (100, 100), 
                 position= (20, 20), 
                 bg_color= 'black', 
                 bd_color= 'white',
                 bar_color= 'white',
                 loading_barID= 'UNASSIGNED'
                 ):
        
        self.game = game
        self.parent_surf = parent_surf

        self.dimensions = dimensions
        self.position = position
        self.bg_color = bg_color
        self.bd_color = bd_color
        self.bar_color = bar_color

        self.loading_barID = loading_barID
        self.progress = 0

        self.surface = pygame.Surface(self.dimensions, pygame.SRCALPHA, 32)

    def get_rect(self, offset= (0, 0)):                     ## I don't really see a point in doing this for a progress bar, but whatever
        return pygame.Rect(self.position[0] + offset[0], self.position[1] + offset[1], self.dimensions[0], self.dimensions[1])

    def render(self):
        self.surface.fill(pygame.Color(0, 0, 0, 0))

        if self.bg_color != 'transparent':
            pygame.draw.rect(self.surface, self.bg_color, pygame.Rect(0, 0, self.dimensions[0], self.dimensions[1]))
        
        pygame.draw.rect(self.surface, self.bar_color, pygame.Rect(2, 2, (self.dimensions[0] - 4) * self.progress, self.dimensions[1] - 4))

        if self.bd_color != 'transparent':
            pygame.draw.rect(self.surface, self.bd_color, pygame.Rect(0, 0, self.dimensions[0], self.dimensions[1]), width= 1)

        self.parent_surf.blit(self.surface, self.position)



## I don't know why i am keeping is code lol:
#          Window(self, self.display, 
#                 windowID= "TestVertInputWindow", 
#                 dimensions= (400, 500), position= (400, 400), 
#                 elements= [{'type': 'label',
#                             'position': (10, 10),
#                             'txt_font': 'label',
#                             'txt_content': 'MONTH:',
#                             'txt_color': 'white'},
#                            {'type': 'label',
#                             'position': (220, 10),
#                             'txt_font': 'label',
#                             'txt_content': 'WEEK:',
#                             'txt_color': 'white'},
#                            {'type': 'input_textbox/vert',
#                             'dimensions': (40, 400),
#                             'position': (100, 10),
#                             'txt_content': '',
#                             'input_boxID': 'TestMonthInputBox',
#                             'char_limit': 20},
#                            {'type': 'input_textbox/vert',
#                             'dimensions': (40, 400),
#                             'position': (300, 10),
#                             'txt_content': '',
#                             'input_boxID': 'TestDayInputBox',
#                             'char_limit': 20}])],
