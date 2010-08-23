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
    
    #self.colors = colors
    colors = []
    
    
    def __init__(self, sequence_start, sequence_length, size=(1000,5000)):
        self.feature_list = []
        self.size = size
        resolution = size[0] / 2        # good default?
        
        BaseSequencePicture.__init__(self, sequence_start, sequence_length, resolution)
        
        # for final y-cropping.
        self.max_y = 2*self.VERTICAL_MARGIN + self.SEQUENCE_HEIGHT
        self.set_left_margin_offset(0)

    def set_left_margin_offset(self, x):
        return
        
    def draw_sequence_line(self):
        return
        
    def _draw_feature(self, slot, start, stop, color=None, name=''):
        self.feature_list.append((name,
                                  #slot,
                                  int(start),
                                  int(stop),
                                  color))
        return

    def _draw_feature_name(self, name, start_x, slot):
        return
        

    def _calc_textsize(self, text):
        return [len(text)*7]

    def _draw_thin_feature(self, slot, start, stop, color=None, name=''):
        self.feature_list.append(("thin"+name,# good indicator for a thin line?
                                  #slot,
                                  int(start),
                                  int(stop),
                                  color)) 

        return
        
 
    def finalize(self):
        return json.dumps([self.colors, self.feature_list])



    def draw_annotations(self, nlmsa, start_slot=0):
        try:
            annotations = nlmsa[self.imageseq]
        except KeyError:
            return 0

        if not annotations:
            return 0

        #slots_d = stack_annotations(self.imageseq, nlmsa)
        #max_slot_used = max(slots_d.values())

        slot = 0; # filler for arguments

        for annotation in annotations:
            is_group = getattr(annotation, 'group', False)

            #subseq = annotation.sequence

            #slot = start_slot + slots_d[annotation.id]
            color = annotation.color

            # keep track of the colors used
            if color not in self.colors:
                self.colors.append(color)

            colornum = self.colors.index(color)

            feat_start = annotation.feature_start
            stop = annotation.sequence.stop

            if is_group:
                #self._draw_feature_name(annotation.name, feat_start, slot)
                self._draw_thin_feature(slot, feat_start, stop, color=colornum,
                    name=annotation.name)

                for (start, stop) in annotation.annots:
                    self._draw_feature(slot, start, stop, colornum)
            else:
                self._draw_feature(slot, feat_start, stop, colornum,
                                   name=annotation.name)
                self._draw_feature_name(annotation.name, feat_start, slot)

        return 1 # max_slot_used + 1



