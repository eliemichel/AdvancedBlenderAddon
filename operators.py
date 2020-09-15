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
from bpy.types import Operator
from bpy.props import FloatProperty
from bpy_extras import view3d_utils

from . import profiling
from . import backend

# -------------------------------------------------------------------

class ResetProfiling(Operator):
    bl_idname = "advanced_blender_addon.reset_profiling"
    bl_label = "Reset Profiling Counters"

    def execute(self, context):
        scene = context.scene
        scene.compute_centroid_profiling.reset()
        return {'FINISHED'}

# -------------------------------------------------------------------

class ComputeCentroid(Operator):
    """Compute the centroid of the object (this message is used as description in the UI)"""
    bl_idname = "advanced_blender_addon.compute_centroid"
    bl_label = "Compute Centroid"

    @classmethod
    def poll(cls, context):
        # Ensure that the operator will not be called when the context is
        # not compatible with it. Here for instance our operator only applies
        # to a mesh.
        # It is better to do these context checks here than directly in
        # execute() because it will also for instance deactivate buttons
        # pointing to this operator in the UI.
        return context.active_object is not None and context.active_object.type == 'MESH'

    def execute(self, context):
        timer = profiling.Timer()

        # The operator class defines the front-end to a function. Its core
        # logic will likely resides in a separate module (called 'backend' here)
        # as a regular python function.
        centroid = backend.compute_centroid(context.active_object)

        # Record in the profiling property the time spent in the core function
        context.scene.compute_centroid_profiling.add_sample(timer.ellapsed())

        # We can report messages to the user, doc at:
        # https://docs.blender.org/api/current/bpy.types.Operator.html#bpy.types.Operator.Operator.report
        self.report({'INFO'}, f"Centoid is at {centroid}")

        return {'FINISHED'}

# -------------------------------------------------------------------

class UpdateDemoOverlay(Operator):
    """Operator called by the DemoTool tool when the mouse moves"""
    bl_idname = "advanced_blender_addon.update_demo_overlay"
    bl_label = "Update Demo Overlay"

    radius: FloatProperty(
        name="Radius",
        description="The radius of the brush in the demo tool",
        default=10.0,
    )

    # A tool calls the invoke() method of the operator, providing info
    # about e.g. the mouse position
    def invoke(self, context, event):
        scene = context.scene

        # Project the mouse onto the ground plane
        origin, direction = self.get_mouse_ray(context, event)
        ground_position = origin - direction * (origin.z / direction.z)

        # And save it in the scene for the overlay to use it
        scene.demo_tool_cursor = ground_position
        scene.demo_tool_radius = self.radius

        # Request a redraw of the area because the overlay changed
        context.area.tag_redraw()
        return {'FINISHED'}

    def get_mouse_ray(self, context, event):
        """get the ray from the viewport and mouse"""
        region, rv3d = context.region, context.region_data
        coord = event.mouse_region_x, event.mouse_region_y
        ray_direction = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
        ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
        return ray_origin, ray_direction

# -------------------------------------------------------------------

class DemoTool(Operator):
    """Operator called by the DemoTool tool when clicking"""
    bl_idname = "advanced_blender_addon.demo_tool"
    bl_label = "Demo Tool Action"

    def invoke(self, context, event):
        x = event.mouse_region_x
        y = event.mouse_region_y
        self.report({'INFO'}, f"DemoTool at position ({x},{y})!")
        return {'FINISHED'}

# -------------------------------------------------------------------

classes = (
    ResetProfiling,
    ComputeCentroid,
    UpdateDemoOverlay,
    DemoTool,
)
register, unregister = bpy.utils.register_classes_factory(classes)
