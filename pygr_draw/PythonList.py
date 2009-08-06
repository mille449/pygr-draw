from stack import stack_annotations
from BaseSequencePicture import BaseSequencePicture

from cStringIO import StringIO
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
    SEQUENCE_HEIGHT = 2
    
    SEQUENCE_TICK_HEIGHT = 6
    SEQUENCE_TICK_WIDTH = 2
    
    SEQUENCE_BASE = 50                 # horizontal margin
    SEQUENCE_OFFSET = 50               # vertical margin
    SEQUENCE_TEXT_OFFSET = 48          # vertical margin for text

    FEATURE_HEIGHT = 8
    THIN_FEATURE_HEIGHT = 2
    THIN_FEATURE_OFFSET = 3
    FEATURE_SPACING = 12
    
    def __init__(self, sequence_length, size=(1000,1000)):
        self.feature_list = []
        self.size = size
        resolution = size[0] / 2        # good default?
        
        BaseSequencePicture.__init__(self, sequence_length, resolution)
        
        # for final y-cropping.
        self.max_y = 2*self.SEQUENCE_OFFSET + self.SEQUENCE_HEIGHT
        self.set_left_margin_offset(0)

    def set_left_margin_offset(self, x):
        x = int(x)
        self.left_margin_offset = x + self.SEQUENCE_BASE

        self.w = self.size[0] + x
        self.h = self.size[1]
        
        self.image = Image.new("RGB", (self.w + x, self.h), colors.white)
        self.draw = ImageDraw.Draw(self.image)

        canvas_width = self.w - self.SEQUENCE_BASE - self.left_margin_offset
        self.seq_to_canvas = float(canvas_width) / float(self.resolution)
        
    def draw_sequence_line(self):
        start_x = self.left_margin_offset
        start_y = self.SEQUENCE_OFFSET + self.SEQUENCE_TICK_HEIGHT / 2 \
                  - self.SEQUENCE_HEIGHT / 2

        w = self.w - self.SEQUENCE_BASE - self.left_margin_offset
        h = self.SEQUENCE_HEIGHT

        self.draw.rectangle((start_x, start_y, start_x + w, start_y + h),
                            fill=colors.black)

        self._calc_tick_spacing()
        n_ticks = self.sequence_length / self.TICKSPACING
        ticklocations = [ i * self.TICKSPACING for i in range(n_ticks + 1) ]

        start_y = self.SEQUENCE_OFFSET
        end_y = self.SEQUENCE_OFFSET + self.SEQUENCE_TICK_HEIGHT

        # conversion factor
        w = self.w - self.SEQUENCE_BASE - self.left_margin_offset
        seq_to_canvas = float(w) / float(self.sequence_length)

        for loc in ticklocations:
            start_x = self.left_margin_offset + int(loc * seq_to_canvas)
            
            end_x = start_x + self.SEQUENCE_TICK_WIDTH
            self.draw.rectangle((start_x, start_y, end_x, end_y),
                                fill=colors.black)
        
    def _draw_feature(self, slot, start, stop, color=None, name=''):
        if color is None:
            color = self.colors.red

        start_y = self.SEQUENCE_OFFSET + (slot+1)*self.FEATURE_SPACING

        start_x = int(start*self.seq_to_canvas + 0.5) + self.left_margin_offset
        width = int( float(stop - start) * self.seq_to_canvas + 0.5 )
        width = max(width, 1)

        assert width > 0

        self.feature_list.append((name,
                                  slot,
                                  int(start),
                                  int(stop),
                                  color))

        self.max_y = max(start_y + self.FEATURE_HEIGHT, self.max_y)

    def _draw_feature_name(self, name, start_x, slot):
        start_x = int( float(start_x) * self.seq_to_canvas + 0.5)
        start_x += self.left_margin_offset
        
        start_y = self.SEQUENCE_TEXT_OFFSET + (slot + 1)*self.FEATURE_SPACING

        xsize = self._calc_textsize(name)[0]

    def _calc_textsize(self, text):
        return self.draw.textsize(text)

    def _draw_thin_feature(self, slot, start, stop, color=None):
        if color is None:
            color = self.colors.red
            
        start_y = self.SEQUENCE_OFFSET + (slot+1)*self.FEATURE_SPACING +\
                  self.THIN_FEATURE_OFFSET

        start_x = int(start*self.seq_to_canvas+0.5) + self.left_margin_offset
        width = int( float(stop - start) * self.seq_to_canvas + 0.5)
        width = max(width, 1)

#        if width + start_x > self.w - self.SEQUENCE_OFFSET:
#            width = self.w - self.SEQUENCE_OFFSET - start_x

        #self.draw.rectangle((start_x, start_y,
        #                     start_x+width, start_y + self.THIN_FEATURE_HEIGHT),
        #                    fill=color, outline=color)
        self.max_y = max(start_y + self.THIN_FEATURE_HEIGHT, self.max_y)

    def finalize(self):
        return self.feature_list
