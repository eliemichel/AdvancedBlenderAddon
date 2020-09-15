# ##### BEGIN GPL LICENSE BLOCK #####
#
#    Copyright (c) 2020 Elie Michel
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from bpy.types import (
    Scene, PropertyGroup
)
from bpy.props import (
    FloatProperty, IntProperty, PointerProperty, BoolProperty,
    FloatVectorProperty,
)

from math import sqrt

# -------------------------------------------------------------------
# A property group can have custom methods attached to it for a more
# convenient access. Members 'sample_count', 'accumulated' and 'accumulated_sq'
# are what is stored in .blend files but average() is used for display in panels
# and add_sample() in operators. A property group can hence contain logic.

class ProfilingCounterProperty(PropertyGroup):
    """A profiling counters can accumulate profiling timings with add_sample
    and then provide their average and standard deviation (stddev()).
    This is an example of advanced PropertyGroup."""

    sample_count: IntProperty(
        name="Sample Count",
        description="Number of sampled values accumulated in the total count",
        default=0,
        min=0,
    )

    accumulated: FloatProperty(
        name="Accumulated Values",
        description="Sum of all samples",
        default=0.0,
    )

    accumulated_sq: FloatProperty(
        name="Accumulated Squared Values",
        description="Sum of the square value of all samples (to compute standard deviation)",
        default=0.0,
    )

    def average(self):
        if self.sample_count == 0:
            return 0
        else:
            return self.accumulated / self.sample_count

    def stddev(self):
        if self.sample_count == 0:
            return 0
        else:
            avg = self.average()
            var = self.accumulated_sq / self.sample_count - avg * avg
            return sqrt(max(0, var))

    def add_sample(self, value):
        self.sample_count += 1
        self.accumulated += value
        self.accumulated_sq += value * value

    def reset(self):
        self.sample_count = 0
        self.accumulated = 0.0
        self.accumulated_sq = 0.0

# -------------------------------------------------------------------

classes = (
    ProfilingCounterProperty,
)
register_cls, unregister_cls = bpy.utils.register_classes_factory(classes)


def register():
    register_cls()

    # Add a profiling property to all scenes
    Scene.compute_centroid_profiling = PointerProperty(type=ProfilingCounterProperty)

    Scene.show_debug_icons = BoolProperty(
        name="Show Debug Icons",
        description="Draw in the scene properties panel the list of all available icons",
        default=False,
    )

    Scene.demo_tool_cursor = FloatVectorProperty(
        name="DemoTool's Cusor Position",
        description="Used internally by the Demo Tool operators to communicate with the overlay",
        options={'HIDDEN', 'SKIP_SAVE'},
    )

    Scene.demo_tool_radius = FloatProperty(
        name="DemoTool's Radius",
        description="Used internally by the Demo Tool operators to communicate with the overlay",
        default=10,
        options={'HIDDEN', 'SKIP_SAVE'},
    )


def unregister():
    unregister_cls()

    del Scene.compute_centroid_profiling
    del Scene.show_debug_icons
    del Scene.demo_tool_cursor
    del Scene.demo_tool_radius
