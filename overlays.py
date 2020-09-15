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
from bpy.types import Gizmo, GizmoGroup
import bgl
from gpu_extras.presets import draw_circle_2d

# NB: It is not possible to subclass View3DOverlay so overlays are
# mimicked using a gizmo+gizmogroup with no interaction.

# -------------------------------------------------------------------

# A gizmo implementing only the draw() method is just an overlay,
# but gizmos can actually get way more advanced (see gizmo templates)
class DemoToolWidget(Gizmo):
    bl_idname = "VIEW3D_GT_demo_tool"

    def draw(self, context):
        # Many custom drawing examples can be found in the gpu module doc:
        # https://docs.blender.org/api/current/gpu.html
        matrix = context.region_data.perspective_matrix

        bgl.glEnable(bgl.GL_BLEND)
        bgl.glEnable(bgl.GL_DEPTH_TEST)
        bgl.glLineWidth(2)
        
        cur = context.scene.demo_tool_cursor
        rad = context.scene.demo_tool_radius
        draw_circle_2d((cur[0], cur[1]), (1, 1, 1, 1), rad, 200)

        # restore opengl defaults
        bgl.glLineWidth(1)
        bgl.glDisable(bgl.GL_BLEND)
        bgl.glDisable(bgl.GL_DEPTH_TEST)

# -------------------------------------------------------------------

class DemoToolOverlay(GizmoGroup):
    bl_idname = "SCENE_GGT_demo_tool"
    bl_label = "Demo Tool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}

    def setup(self, context):
        self.gizmos.new(DemoToolWidget.bl_idname)

# -------------------------------------------------------------------

classes = (
    DemoToolWidget,
    DemoToolOverlay,
)
register, unregister = bpy.utils.register_classes_factory(classes)
