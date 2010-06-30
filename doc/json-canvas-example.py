#***************************** simple example *******************************

from pygr import seqdb
genome = seqdb.BlastDB('example.fa')
sequence_name ='chrI'

import pygr_draw
from pygr_draw import Annotation

image = pygr_draw.Draw('json-canvas-example.js')
colors = image.colors

###

annots = []
annots.append(Annotation('exon1', sequence_name, 0, 500, color=colors.blue))
annots.append(Annotation('exon2', sequence_name, 200, 500, color=colors.green))
annots.append(Annotation('exon3', sequence_name, 250, 300, color=colors.black))

for i in range(250, 500, 10):
    name = 'exon%d' % (i+4)
    start = i
    end = 2000

    annots.append(Annotation(name, sequence_name, start, end,color=colors.red))

image.add_track(annots, genome)

subsequence = genome[sequence_name][0:1000]
image.save(subsequence)

print 'Output in', image.filename



#**************************** group example ********************************

#from pygr import seqdb
#genome = seqdb.BlastDB('example.fa')
#sequence_name = 'chrI'
#
#import pygr_draw
#from pygr_draw import AnnotationGroup, Annotation
#
#image = pygr_draw.Draw('json-canvas-example.js')
#colors = image.colors
#
#annots = []
#annots.append(Annotation('blip', sequence_name, 25, 75, color=colors.green))
#
#gene1_exons = ((50, 100), (200, 300), (500, 1500))
#annots.append(AnnotationGroup('gene1', sequence_name, gene1_exons,
#                              color=colors.red))
#
#gene2_exons = ((100, 300), (1500, 2000), (3000, 3750))
#annots.append(AnnotationGroup('gene2', sequence_name, gene2_exons,
#                              color=colors.blue))
#
#gene3_exons = ((3800, 4000), (4500, 5000))
#annots.append(AnnotationGroup('gene3', sequence_name, gene3_exons,
#                              color=colors.blue))
#
#gene4_exons = ((100, 300), (1500, 2000), (3000, 3750))
#annots.append(AnnotationGroup('gene4', sequence_name, gene4_exons,
#                              color=colors.blue))
#
#image.add_track(annots, genome)
#
#subseq = genome[sequence_name][:4000]
#image.save(subseq)
#
#print 'Output in', image.filename
