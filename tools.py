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
from bpy.types import WorkSpaceTool

from . import operators as ops
from . import overlays

# Tools are UI states that can be activated through the T panel
# in the 3D view. They don't hold logic, they just set-up connections
# between events/keys and operators which are enabled when the tool
# gets activated.
# They can draw a setting UI on the top bar of the 3d view, and enable
# some overlay widget.

# -------------------------------------------------------------------

class DemoTool(WorkSpaceTool):
    bl_space_type = 'VIEW_3D'
    bl_context_mode = 'OBJECT'

    bl_idname = "advanced_blender_addon.demo_tool"
    bl_label = "Demo Tool"
    bl_description = "Just a mock demo tool to show of it works"

    # The icon displayed in the T panel
    bl_icon = "ops.generic.select_circle"

    # This overlay will be activated only when the tool is turned on
    # while otherwise overlays stays activated all the time.
    bl_widget = overlays.DemoToolOverlay.bl_idname

    # The keymap is the core of the tool, it tells when to call which
    # operator.
    bl_keymap = (
        (ops.DemoTool.bl_idname,
            {"type": 'LEFTMOUSE', "value": 'PRESS'},
            {"properties": []}),

        (ops.UpdateDemoOverlay.bl_idname,
            {"type": 'MOUSEMOVE', "value": 'ANY'},
            {"properties": []}),
    )

    def draw_settings(context, layout, tool):
        # Settings are what is displayed in the top bar. They don't belong
        # to the tool itself but rather to the operators it calls.
        props = tool.operator_properties(ops.UpdateDemoOverlay.bl_idname)
        layout.prop(props, "radius")

# -------------------------------------------------------------------

def register():
    bpy.utils.register_tool(DemoTool)

def unregister():
    bpy.utils.unregister_tool(DemoTool)
    
