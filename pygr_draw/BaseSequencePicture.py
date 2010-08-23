from stack import stack_annotations

from pygr.sequence import Sequence
from pygr import seqdb, cnestedlist
import math

class BaseSequencePicture(object):
    SUFFIX = None                       # must define
    colors = None                       # must define

    SEQUENCE_HEIGHT = 2

    SEQUENCE_TICK_HEIGHT = 6
    SEQUENCE_TICK_WIDTH = 2

    HORIZONTAL_MARGIN = 50
    VERTICAL_MARGIN = 50
    VERTICAL_MARGIN_TEXT = 48

    FEATURE_HEIGHT = 8
    THIN_FEATURE_HEIGHT = 2
    THIN_FEATURE_OFFSET = 3
    FEATURE_SPACING = 12

    def __init__(self, sequence, resolution):
        self.sequence_length = len(sequence)
        self.sequence_start = sequence.start

        # resolution controls the granularity used to calculate overlaps.
        self.resolution = resolution
        
        self.imageseq = Sequence('A'*resolution, 'bitmap')
        self.genome = dict(bitmap=self.imageseq)
        self.set_left_margin_offset(0)
        self.ticks = {}
        self._calc_ticks()

    def draw_sequence_line(self):
        '''
        Draw the black line at the top representing the sequence with ticks
        indicating resolution.
        '''
        raise NotImplementedError

    def _draw_feature(self, slot, start, stop, color=None, name=''):
        '''
        Draw an annotation, or part of an annotation, as a thick line.
        '''
        raise NotImplementedError

    def _draw_feature_name(self, name, start_x, slot):
        '''
        Draw the name of the annotation next to it.
        '''
        raise NotImplementedError

    def _draw_thin_feature(self, slot, start, stop, color=None, name=''):
        '''
        Draw an annotation as a thin line.
        '''
        raise NotImplementedError

    def _calc_textsize(self, text):
        '''
        Calculate the width of the text label for an annotation.
        '''
        raise NotImplementedError
    
    def finalize(self):
        '''
        Returns the image as a string that can be written to a file.
        '''
        raise NotImplementedError

    def set_left_margin_offset(self, x):
        self.left_margin_offset = x

    ###

    def _calc_tick_spacing(self):
        '''
        Calculate the width in bases for each tick
        '''

        # this will give 1-10 ticks in every range/2
        # increase this number for more ticks
        span = self.sequence_length/2;

        # this will give us the highest power of 10 the the span reaches
        tickunit = int(math.log(span)/math.log(10))

        self.TICKSPACING = 10**tickunit
        if (span / self.TICKSPACING < 5): self.TICKSPACING /= 2;



    def _calc_ticks(self):
        '''
        Calculate the tick locations on the sequence line.
        Creates self.ticks as a dictionary with the keys being a normalized (0-1)
        representatin of the values, for easy conversion to pixel scale,
        and the values being a string representing the location in bases.
        '''

        self._calc_tick_spacing()

        # put the first tick at the first valid location from the start
        # of the sequence
        start_x = self.TICKSPACING - (self.sequence_start % self.TICKSPACING)
        

        # draw n=0 tick instead of n=1 tick when at multiples of TICKSPACING
        if (start_x == self.TICKSPACING): start_x = 0        

        tick = float(start_x - self.sequence_start) / self.sequence_length
        tick_text = str(self.sequence_start + start_x)

        while(start_x <= self.sequence_start + self.sequence_length):
            self.ticks[tick]=tick_text
            start_x+=self.TICKSPACING
            tick = float(start_x - self.sequence_start) / self.sequence_length
            tick_text = str(self.sequence_start + start_x)




    def draw_annotations(self, nlmsa, start_slot=0):
        try:
            annotations = nlmsa[self.imageseq]
        except KeyError:
            return 0
        
        if not annotations:
            return 0

        slots_d = stack_annotations(self.imageseq, nlmsa)
        max_slot_used = max(slots_d.values())

        for annotation in annotations:
            is_group = getattr(annotation, 'group', False) 
           
            subseq = annotation.sequence

            slot = start_slot + slots_d[annotation.id]
            color = annotation.color

            feat_start = annotation.feature_start
            stop = annotation.sequence.stop

            if is_group:
                self._draw_feature_name(annotation.name, feat_start, slot)
                self._draw_thin_feature(slot, feat_start, stop, color=color,
                    name=annotation.name)

                for (start, stop) in annotation.annots:
                    self._draw_feature(slot, start, stop, color)
            else:
                self._draw_feature(slot, feat_start, stop, color,
                                   name=annotation.name)
                self._draw_feature_name(annotation.name, feat_start, slot)

        return max_slot_used + 1
