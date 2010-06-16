from stack import stack_annotations
from BaseSequencePicture import BaseSequencePicture

from cStringIO import StringIO
import json

class ColorList(object):
    pass

colors = ColorList()
colors.white = "#ffffff"
colors.red = "#ff0000"
colors.green = "#00ff00"
colors.blue = "#0000ff"
colors.orange = "#ff8040"
colors.purple = "#800080"
colors.black = "#000000"

class JSONSequencePicture(BaseSequencePicture):
    SUFFIX = '.js'

    colors = colors

    rectangles = [];
    texts = [];

    def __init__(self, sequence_length, size=(1000,5000)):
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

#        self.image = Image.new("RGB", (self.w + x, self.h), colors.white)
#        self.draw = ImageDraw.Draw(self.image)

        canvas_width = self.w - self.SEQUENCE_BASE - self.left_margin_offset
        self.seq_to_canvas = float(canvas_width) / float(self.resolution)


    def draw_sequence_line(self):
        '''
        Draw the black line at the top representing the sequence with ticks
        indicating resolution.
        '''
        start_x = self.left_margin_offset
        start_y = self.SEQUENCE_OFFSET + self.SEQUENCE_TICK_HEIGHT / 2 \
                  - self.SEQUENCE_HEIGHT / 2

        w = self.w - self.SEQUENCE_BASE - self.left_margin_offset
        h = self.SEQUENCE_HEIGHT

        self.rectangles.append(({"rect":(start_x, start_y, w, h ),
                            "fill":colors.black}))

        self._calc_tick_spacing()
        n_ticks = self.sequence_length / self.TICKSPACING
        ticklocations = [ i * self.TICKSPACING for i in range(n_ticks + 1) ]

        start_y = self.SEQUENCE_OFFSET

        # conversion factor
        w = self.w - self.SEQUENCE_BASE - self.left_margin_offset
        seq_to_canvas = float(w) / float(self.sequence_length)

        for loc in ticklocations:
            start_x = self.left_margin_offset + int(loc * seq_to_canvas)

            self.rectangles.append(({"rect":(start_x, start_y,
                                    self.SEQUENCE_TICK_WIDTH,
                                    self.SEQUENCE_TICK_HEIGHT),
                                    "fill":colors.black}))
        

    def _draw_feature(self, slot, start, stop, color=None, name=''):
        '''
        Draw an annotation, or part of an annotation, as a thick line.
        '''
        if color is None:
            color = self.colors.red

        start_y = self.SEQUENCE_OFFSET + (slot+1)*self.FEATURE_SPACING

        start_x = int(start*self.seq_to_canvas + 0.5) + self.left_margin_offset
        width = int( float(stop - start) * self.seq_to_canvas + 0.5 )
        width = max(width, 1)

        assert width > 0

        self.rectangles.append(({"rect":(start_x, start_y, width, self.FEATURE_HEIGHT ),
                            "fill":color, "outline":colors.black}))
        self.max_y = max(start_y + self.FEATURE_HEIGHT, self.max_y)


    def _draw_feature_name(self, name, start_x, slot):
        '''
        Draw the name of the annotation next to it.
        '''
        start_x = int( float(start_x) * self.seq_to_canvas + 0.5)
        start_x += self.left_margin_offset

        start_y = self.SEQUENCE_TEXT_OFFSET + (slot + 1.75)*self.FEATURE_SPACING

        # use js to calculate text width and x poisitioning
        xsize = self._calc_textsize(name)[0]
        self.texts.append(({"text":(name, start_x - xsize, start_y),
                            "fill":colors.black} ))


    def _calc_textsize(self, text):
        '''
        Calculate the width of the text label for an annotation.
        '''
        text_size = len(text)*7
        return [text_size]


    def _draw_thin_feature(self, slot, start, stop, color=None):
        '''
        Draw an annotation as a thin line.
        '''
        if color is None:
            color = self.colors.red

        start_y = self.SEQUENCE_OFFSET + (slot+1)*self.FEATURE_SPACING +\
                  self.THIN_FEATURE_OFFSET

        start_x = int(start*self.seq_to_canvas+0.5) + self.left_margin_offset
        width = int( float(stop - start) * self.seq_to_canvas + 0.5)
        width = max(width, 1)

#        if width + start_x > self.w - self.SEQUENCE_OFFSET:
#            width = self.w - self.SEQUENCE_OFFSET - start_x

        self.rectangles.append(({"rect":(start_x, start_y, width,
                                self.THIN_FEATURE_HEIGHT),
                                "fill":color, "outline":color}))
        self.max_y = max(start_y + self.THIN_FEATURE_HEIGHT, self.max_y)



    def finalize(self):
        '''
        Returns the image as a string that can be written to a file.
        '''
        fp = StringIO()
        fp.write("annots=")
        json.dump({"rectangles":self.rectangles, "texts":self.texts}, fp, indent=4) # indent is for pretty printing
        fp.write(";")

        return fp.getvalue()
        