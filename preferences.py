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
from bpy.types import AddonPreferences
from bpy.props import FloatProperty

addon_idname = __package__.split(".")[0]

# -------------------------------------------------------------------

def getPreferences(context=None):
    """Get the preferences of this add-on (guessed from the __package__
    name, which should always be fine)."""
    if context is None:
        context = bpy.context
    return context.preferences.addons[addon_idname].preferences

# -------------------------------------------------------------------
# See more examples at
# https://docs.blender.org/api/current/bpy.types.AddonPreferences.html

class AdvancedBlenderAddonPreferences(AddonPreferences):
    bl_idname = addon_idname

    some_preference: FloatProperty(
        name="Some Preference",
        description="This is a global setting, saved in user preferences rather than in .blend files.",
        default=3.14
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Add here some user settings.")
        layout.prop(self, "some_preference")

# -------------------------------------------------------------------

classes = (AdvancedBlenderAddonPreferences,)
register, unregister = bpy.utils.register_classes_factory(classes)
