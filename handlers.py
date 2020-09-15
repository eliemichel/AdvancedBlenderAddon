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
from bpy.app.handlers import load_post, persistent

# Handlers are callback functions "hooked" to some events of Blender's
# internal loop. They are called whenever some event occurs.
# The full list of available handlers can be found here:
# https://docs.blender.org/api/current/bpy.app.handlers.html

# -------------------------------------------------------------------

# Make sure to make this persistent otherwise handlers get reset prior
# to loading new files.
@persistent
def advanced_blender_addon_on_load(scene):
	if scene is not None:
		# Typically, you'll initialize some stuff here, or reset any
		# global state.
		print("A scene has been loaded!")

# -------------------------------------------------------------------

def remove_handler(handlers_list, cb):
	"""Remove any handler with the same name from a given handlers list"""
	to_remove = [h for h in handlers_list if h.__name__ == cb.__name__]
	for h in to_remove:
		handlers_list.remove(h)

def register():
	unregister() # remove handlers if they were present already
	load_post.append(advanced_blender_addon_on_load)

def unregister():
	remove_handler(load_post, advanced_blender_addon_on_load)
