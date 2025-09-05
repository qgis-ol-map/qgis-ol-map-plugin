QGIS Open Layers Map Plugin
===========================

Export QGIS projects as interactive OpenLayers web maps with support for 
multiple layer types and preserved styling.

OVERVIEW
--------
The QGIS Open Layers Map plugin allows you to export your QGIS projects as 
interactive web maps using OpenLayers. It preserves your project's styling, 
supports various layer types, and generates a complete web application that 
can be shared or deployed anywhere.

FEATURES
--------
- Multiple Layer Support: XYZ tiles, GeoJSON, WMS, WFS, and GeoTIFFs
- Style Preservation: Maintains your QGIS project styling in the web map
- Interactive Web Maps: Generated maps are fully interactive
- Easy Deployment: Creates self-contained web applications
- Configurable Output: Customizable export options and settings

INSTALLATION
------------
From QGIS Plugin Repository (Recommended):
1. Open QGIS
2. Go to Plugins → Manage and Install Plugins
3. Search for "QGIS Open Layers Map"
4. Click Install Plugin

Manual Installation:
1. Copy the entire plugin directory to your QGIS plugins directory:
   ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins (Linux)
   ~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins (macOS)
   %APPDATA%\QGIS\QGIS3\profiles\default\python\plugins (Windows)
2. Restart QGIS
3. Enable the plugin in Plugins → Manage and Install Plugins → Installed

QUICK START
-----------
1. Open your QGIS project with the layers you want to export
2. Go to Plugins → QGIS Open Layers Map
3. Configure your export settings in the dialog
4. Choose an output directory
5. Click Export to generate your web map
6. Open the generated index.html file in a web browser

REQUIREMENTS
------------
- QGIS Version: 3.0 or higher
- Python: 3.6+ (included with QGIS)
- Web Browser: Modern browser with JavaScript support

SUPPORT
-------
- Issues: https://github.com/qgis-ol-map/qgis-ol-map-plugin/issues
- Email: qgis@wiktor.latanowicz.com

For detailed documentation, see README.md

Copyright (C) 2025 Wiktor Latanowicz
Licensed under GNU General Public License v2 or later
