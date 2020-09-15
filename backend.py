# If this module does not use bpy nor any blender related module, it may
# be licensed with something else than the GPL:

# ##### BEGIN MIT LICENSE BLOCK #####
#
#    Copyright (c) 2020 Elie Michel
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the “Software”), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#  The Software is provided “as is”, without warranty of any kind, express or
#  implied, including but not limited to the warranties of merchantability,
#  fitness for a particular purpose and noninfringement. In no event shall the
#  authors or copyright holders be liable for any claim, damages or other
#  liability, whether in an action of contract, tort or otherwise, arising
#  from, out of or in connection with the software or the use or other dealings
#  in the Software.
#
# ##### BEGIN MIT LICENSE BLOCK #####

import numpy as np

# This shows how to efficiently access mesh vertex positions as numpy arrays
def compute_centroid(obj):
    vertices = obj.data.vertices

    # Buffer of positions as a numpy array
    positions = np.zeros((len(vertices), 3), dtype=np.float32)

    # The foreach_get/foreach_set functions are available on many Blender's
    # object to efficiently copy internal data into python objects supporting
    # the buffer protocole, like for instance numpy arrays:
    # (it is important to use ravel() to present the array as single dimensional)
    vertices.foreach_get('co', positions.ravel())

    # Convert to world space
    matrix = np.array(obj.matrix_world)
    homogenous_coords = np.vstack((positions.T, np.ones((1, len(vertices)))))
    world_positions = matrix.dot(homogenous_coords)[:-1,:].T

    return world_positions.mean(axis=0)
