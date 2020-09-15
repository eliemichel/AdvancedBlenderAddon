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

bl_info = {
    "name": "Advanced Blender Addon Demo",
    "author": "Élie Michel <elie.michel@exppad.com>",
    "version": (0, 1, 0),
    "blender": (2, 90, 0),
    "location": "Properties > Scene",
    "description": "An example of advanced add-on for Blender",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "https://github.com/eliemichel/AdvancedBlenderAddon",
    "support": "COMMUNITY",
    "category": "3D view",
}

# -------------------------------------------------------------------
# This section is dedicated to make the "Reload Scripts" operator of
# Blender truly work to be able to update the add-on while developping.
# This feature only reloads this __init__ file, so we force reloading all
# other files here.

def list_all_modules():
    """List all python files, to drive hot reloading in Blender
    NB: this does not recurse in subdirectories"""
    import pathlib
    import os
    d = pathlib.Path(__file__).parent.absolute()
    (_, _, filenames) = next(os.walk(d))
    return [f[:-3] for f in filenames if f.endswith(".py") and f != "__init__.py"]

def reload_all_modules():
    """Reload all modules from the current directory"""
    print("Reloading submodules...")
    import importlib
    modules = list_all_modules()
    for i in range(5):
        # try and reach a fixed point, needed because we don't
        # know in which order the modules import each others
        for mod_name in modules:
            mod = locals().get(mod_name)
            try:
                if mod is None:
                    mod = importlib.import_module('.' + mod_name, __name__)
                importlib.reload(mod)
            except Exception as e:
                print(f"Exception while reloading {mod_name}:\n{e}")
                pass

# When bpy is already in local, we know this is called by "Reload plugins"
if "bpy" in locals():
    reload_all_modules()

# -------------------------------------------------------------------

import bpy
from . import preferences
from . import properties
from . import operators
from . import panels
from . import overlays
from . import tools
from . import handlers

def register():
    preferences.register()
    properties.register()
    operators.register()
    panels.register()
    overlays.register()
    tools.register()
    handlers.register()
    
def unregister():
    preferences.unregister()
    properties.unregister()
    operators.unregister()
    panels.unregister()
    overlays.unregister()
    tools.unregister()
    handlers.unregister()
