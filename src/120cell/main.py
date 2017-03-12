# pylint: disable=unused-import

import numpy as np
from vapory import *
from penrose import Penrose
from cell120 import Cell_120

try:
    from vapory import Media
except ImportError:
    class Media(POVRayElement):
        """Media()"""


default = Finish('ambient', 0.3, 'diffuse', 0.7, 'phong', 1)


penrose_config = {'vertex_size': 0.05,
                  'vertex_texture': Texture(Pigment('color', 'White'),
                                            default),
                  'edge_thickness': 0.05,
                  'edge_texture': Texture(Pigment('color', 'White'),
                                          default),
                  'default': default}


cell_120_config = {'vertex_size': 0.05,
                   'vertex_texture': Texture(Pigment('color', 'White'),
                                             default),
                   'edge_thickness': 0.05,
                   'edge_texture': Texture('T_Chrome_4D',
                                           Pigment('color', 'White', 'transmit', 0),
                                           Finish('reflection', 0.4, 'brilliance', 0.4)),
                   'face_texture': Texture(Pigment('color', 'Blue', 'transmit', 0.7),
                                           Finish('reflection', 0, 'brilliance', 0)),
                   'interior': Interior(Media('intervals', 1, 'samples', 1, 1, 'emission', 1))}


leftwall = Penrose(num_lines = 12,
                   shift = (0.5, 0.5, 0.5, 0.5, 0.5),
                   thin_color = (0.75, 0.25, 1),
                   fat_color = (1, 0.25, 0.5),
                   **penrose_config).put_objs('scale', 1.5,
                                              'rotate', (0, -45, 0),
                                              'translate', (-18, 0, 18))

rightwall = Penrose(num_lines = 12,
                    shift = np.random.random(5),
                    thin_color = (0.5, 0, 1),
                    fat_color = (0, 0.5, 1),
                    **penrose_config).put_objs('scale', 1.5,
                                               'rotate', (0, 45, 0),
                                               'translate', (18, 0, 18))

floor = Penrose(num_lines= 12,
                shift = (0.1, 0.2, -0.3, 0.6, -0.6),
                thin_color = (1, 0, 1),
                fat_color = (0, 1, 1),
                **penrose_config).put_objs('scale', 1.5, 'rotate', (90, 0, 0))

polytope = Cell_120(**cell_120_config)
cell_120 = polytope.put_objs('scale', 1.5,
                             'translate',
                             (0, -polytope.bottom, 0))

camera = Camera('location', (0, 12, -30), 'look_at', (0, 0, 20))
light = LightSource((-30, 10, -30), 'color', (1, 1, 1))
objects = [light, leftwall, rightwall, floor, cell_120]
scene = Scene(camera, objects, included=['colors.inc', 'metals.inc'])
scene.render('penrose_120_cell.png', width=600, height=480, antialiasing=0.001, remove_temp=False)
