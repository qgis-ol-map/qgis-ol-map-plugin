# QGIS Open Layers Map

Export QGIS projects as interactive OpenLayers web maps with support for multiple layer types and preserved styling.

## Overview

The QGIS Open Layers Map plugin allows you to export your QGIS projects as interactive web maps using OpenLayers. It preserves your project's styling, supports various layer types, and generates a complete web application that can be shared or deployed anywhere.

## Features

- **Multiple Layer Support**: XYZ tiles, GeoJSON, WMS, WFS, and GeoTIFFs
- **Style Preservation**: Maintains your QGIS project styling in the web map
- **Interactive Web Maps**: Generated maps are fully interactive with pan, zoom, and layer controls
- **Easy Deployment**: Creates self-contained web applications
- **Configurable Output**: Customizable export options and settings

## Installation

### From QGIS Plugin Repository (Recommended)

1. Open QGIS
2. Go to **Plugins** → **Manage and Install Plugins**
3. Search for "QGIS Open Layers Map"
4. Click **Install Plugin**

### Manual Installation

1. Download the plugin from the [GitHub repository](https://github.com/qgis-ol-map/qgis-ol-map-plugin)
2. Extract the ZIP file to your QGIS plugins directory:
   - **Windows**: `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins`
   - **macOS**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins`
   - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins`
3. Restart QGIS
4. Enable the plugin in **Plugins** → **Manage and Install Plugins** → **Installed**

## Quick Start

1. Open your QGIS project with the layers you want to export
2. Go to **Plugins** → **QGIS Open Layers Map**
3. Configure your export settings in the dialog
4. Choose an output directory
5. Click **Export** to generate your web map
6. Open the generated `index.html` file in a web browser

## Supported Layer Types

| Layer Type | Support Status | Notes |
|------------|----------------|-------|
| XYZ Tiles | ✅ Full | Supports min/max zoom levels |
| GeoJSON | ✅ Full | Vector data with styling |
| WMS | ✅ Full | Web Map Service layers |
| WFS | ✅ Full | Web Feature Service layers with styling |
| GeoTIFF | ✅ Full | Raster data |

## Configuration Options

- **Output Directory**: Where to save the generated web map
- **Project Title**: Title for the web map
- **Layer Selection**: Choose which layers to include
- **Zoom Levels**: Configure min/max zoom for tile layers
- **Styling Options**: Customize map appearance

## Generated Output

The plugin creates a complete web application with:

- `index.html` - Main web map page
- `config.json` - Map configuration
- `data/` - Exported layer data
- `css/` - Styling files
- `js/` - JavaScript libraries and map logic

## Deployment

The generated web map is self-contained and can be:

- Opened directly in a web browser
- Deployed to any web server
- Hosted on GitHub Pages, Netlify, or similar platforms
- Embedded in existing websites

## Requirements

- **QGIS Version**: 3.0 or higher
- **Python**: 3.6+ (included with QGIS)
- **Web Browser**: Modern browser with JavaScript support

## Troubleshooting

### Common Issues

**Plugin doesn't appear in menu**
- Ensure the plugin is enabled in Plugin Manager
- Check QGIS version compatibility

**Export fails with error**
- Verify all layer sources are accessible
- Check file permissions in output directory
- Review QGIS message log for detailed errors

**Web map doesn't display correctly**
- Ensure all files were exported completely
- Check browser console for JavaScript errors
- Verify layer data integrity

**Styling not preserved**
- Some advanced QGIS styling may not translate directly
- Check supported styling options in documentation

## Development

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Building from Source

```bash
git clone https://github.com/qgis-ol-map/qgis-ol-map-plugin.git
cd qgis-ol-map-plugin
make
```

### Running Tests

```bash
make test
```

## License

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

## Support

- **Issues**: [GitHub Issues](https://github.com/qgis-ol-map/qgis-ol-map-plugin/issues)
- **Documentation**: [Project Wiki](https://github.com/qgis-ol-map/qgis-ol-map-plugin/wiki)
- **Email**: qgis@wiktor.latanowicz.com

## Changelog

### Version 0.1
- Initial release
- Support for XYZ tiles, GeoJSON, WMS, WFS, and GeoTIFFs
- Style preservation
- Configurable zoom levels
- Web map generation

## Author

**Wiktor Latanowicz**
- Email: qgis@wiktor.latanowicz.com
- GitHub: [qgis-ol-map](https://github.com/qgis-ol-map)