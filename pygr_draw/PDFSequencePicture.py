from stack import stack_annotations
from BaseSequencePicture import BaseSequencePicture

from cStringIO import StringIO

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors

class PDFSequencePicture(BaseSequencePicture):
    SUFFIX = '.pdf'
    
    colors = colors
    
   
    HORIZONTAL_MARGIN = 100                 # horizontal margin
    VERTICAL_MARGIN = 100               # vertical margin

    TEXT_OFFSET = 8
    

    
    def __init__(self, sequence):
        self.w, self.h = landscape(letter)
        BaseSequencePicture.__init__(self, sequence, int(self.w))
        
        self.data_fp = StringIO()
        self.canvas = canvas.Canvas(self.data_fp, pagesize=(self.w,self.h))

        # conversion factor
        self.seq_to_canvas = float((self.w - 2*self.HORIZONTAL_MARGIN) /
                                   self.resolution)
        
    def draw_sequence_line(self):
        start_x = self.HORIZONTAL_MARGIN
        start_y = self.VERTICAL_MARGIN + self.SEQUENCE_TICK_HEIGHT / 2 -\
                  self.SEQUENCE_HEIGHT / 2
        start_y = self.h - start_y

        seq_w = self.w - 2*self.HORIZONTAL_MARGIN
        seq_h = self.SEQUENCE_HEIGHT
        
        self.canvas.rect(start_x, start_y, seq_w, -seq_h, fill=1)

        ## draw ticks
        start_y = self.VERTICAL_MARGIN
        start_y = self.h - start_y
        
        h = -self.SEQUENCE_TICK_HEIGHT
        w = self.SEQUENCE_TICK_WIDTH

        for loc in self.ticks.iterkeys():
            start_x = loc * (seq_w - self.SEQUENCE_TICK_WIDTH) + self.HORIZONTAL_MARGIN
            self.canvas.rect(start_x, start_y, w, h, fill=1)

            textsize = self._calc_textsize(self.ticks[loc])[0]/2
            self.canvas.drawCentredString(start_x, (start_y + self.FEATURE_SPACING),\
                            self.ticks[loc])

    def _calc_textsize(self, text):
        text_size = len(text)*5
        return [text_size]
    
    def _draw_feature(self, slot, start, stop, color=None, name=''):
        if color is None:
            color = self.colors.red
            
        start_y = (self.VERTICAL_MARGIN + (slot+1)*self.FEATURE_SPACING)
        start_y = self.h - start_y

        start = int(self.seq_to_canvas * start)
        stop = int(self.seq_to_canvas * stop)
        
        start_x = start + self.HORIZONTAL_MARGIN
        width = stop - start
        
        width = max(width, 1)

        assert width > 0

        self.canvas.setFillColor(color)
        self.canvas.setStrokeColor(self.colors.black)
        self.canvas.rect(start_x, start_y, width, -self.FEATURE_HEIGHT, fill=1)

    def _draw_feature_name(self, name, start_x, slot):
        start_y = self.VERTICAL_MARGIN + self.TEXT_OFFSET + (slot + 1) * self.FEATURE_SPACING
        start_y = self.h - start_y
        start_x = (start_x + self.HORIZONTAL_MARGIN)*self.seq_to_canvas
        self.canvas.setFillColor(self.colors.black)
        self.canvas.drawRightString(start_x, start_y, name)

    def _draw_thin_feature(self, slot, start, stop, color=None, name=''):
        if color is None:
            color = self.colors.red
            
        start_y = self.VERTICAL_MARGIN + (slot+1)*self.FEATURE_SPACING +\
                  self.THIN_FEATURE_OFFSET
        start_y = self.h - start_y

        start = int(self.seq_to_canvas * start)
        stop = int(self.seq_to_canvas * stop)

        start_x = start + self.HORIZONTAL_MARGIN
        width = stop - start
        width = max(width, 1)

        if width + start_x > self.w - self.HORIZONTAL_MARGIN:
            width = self.w - self.HORIZONTAL_MARGIN - start_x

        self.canvas.setFillColor(color)
        self.canvas.setStrokeColor(color)
        self.canvas.rect(start_x, start_y, width, -self.THIN_FEATURE_HEIGHT,
                         fill=1)

    def finalize(self):
        self.canvas.showPage()
        self.canvas.save()
        return self.data_fp.getvalue()
