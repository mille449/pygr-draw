from stack import stack_annotations
from BaseSequencePicture import BaseSequencePicture

from cStringIO import StringIO
import json
from PIL import Image, ImageDraw

colors_d = dict(white='white',
               red='red',
               green='green',
               blue='blue',
               orange='orange',
               purple='purple',
               black='black')
class Bag(object):
    pass
colors = Bag()
colors.__dict__.update(colors_d)

class PythonList(BaseSequencePicture):
    SUFFIX = '.FOO'
    
    colors = colors
    
    
    def __init__(self, sequence_length, size=(1000,5000)):

        self.feature_list = []
        self.size = size
        resolution = size[0] / 2        # good default?
        
        BaseSequencePicture.__init__(self, sequence_length, resolution)
        
        # for final y-cropping.
        self.max_y = 2*self.SEQUENCE_OFFSET + self.SEQUENCE_HEIGHT
        self.set_left_margin_offset(0)

    def set_left_margin_offset(self, x):
        return
        
    def draw_sequence_line(self):
        return
        
    def _draw_feature(self, slot, start, stop, color=None, name=''):
        self.feature_list.append((name,
                                  slot,
                                  int(start),
                                  int(stop),
                                  color))
        return

    def _draw_feature_name(self, name, start_x, slot):
        return
        

    def _calc_textsize(self, text):
        return self.draw.textsize(text)

    def _draw_thin_feature(self, slot, start, stop, color=None, name=''):
        self.feature_list.append(("thin"+name,#indicator for a thin line
                                  slot,
                                  int(start),
                                  int(stop),
                                  color)) 

        return
        
 
    def finalize(self):
        return json.dumps(self.feature_list)






