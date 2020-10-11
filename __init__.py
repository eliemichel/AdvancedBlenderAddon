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

# When loaded is already in local, we know this is called by "Reload plugins"
if locals().get('loaded') or True:
    loaded = False
    from importlib import reload
    from sys import modules
    import os

    for i in range(3): # Try up to three times, in case of ordering errors
        err = False
        modules[__name__] = reload(modules[__name__])
        submodules = list(modules.items())
        for name, module in submodules:
            if name.startswith(f"{__package__}."):
                if module.__file__ is None:
                    # This is a namespace, no need to do anything
                    continue
                elif not os.path.isfile(module.__file__):
                    # File has been removed
                    del modules[name]
                    del globals()[name]
                else:
                    print(f"Reloading: {module}")
                    try:
                        globals()[name] = reload(module)
                    except Exception as e:
                        print(e)
                        err = True
        if not err:
            break
        #del reload, modules

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
