from qgis._core import QgsLayerTreeLayer, QgsLayerTree
from typing import Any, Iterator
from urllib.parse import parse_qs
from .data_exporter import DataExporter
from .style_exporter import extract_style
import logging
from shlex import shlex

JsonDict = dict[str, Any]


def parse_kv_pairs(text, item_sep=",", value_sep="="):
    """Parse key-value pairs from a shell-like text.
    source: https://stackoverflow.com/a/38738997
    """
    # initialize a lexer, in POSIX mode (to properly handle escaping)
    lexer = shlex(text, posix=True)
    # set ',' as whitespace for the lexer
    # (the lexer will use this character to separate words)
    lexer.whitespace = item_sep
    # include '=' as a word character 
    # (this is done so that the lexer returns a list of key-value pairs)
    # (if your option key or value contains any unquoted special character, you will need to add it here)
    lexer.wordchars += value_sep
    # then we separate option keys and values to build the resulting dictionary
    # (maxsplit is required to make sure that '=' in value will not be a problem)
    return dict(word.split(value_sep, maxsplit=1) for word in lexer)



logger = logging.getLogger(__name__)

class LayerExporter:
    def __init__(self, root: QgsLayerTree, counter: Iterator, data_exporter: DataExporter) -> None:
        self.root = root
        self.counter = counter
        self.data_exporter = data_exporter

    def layer_to_dict(self, layerNode: QgsLayerTreeLayer) -> JsonDict:
        try:
            if self.is_xyz_layer(layerNode):
                return self.xyz_layer_to_dict(layerNode)
            if self.is_wmts_layer(layerNode):
                return self.wmts_layer_to_dict(layerNode)
            if self.is_wms_layer(layerNode):
                return self.wms_layer_to_dict(layerNode)
            if self.is_kml_layer(layerNode):
                return self.kml_layer_to_dict(layerNode)
            if self.is_geojson_layer(layerNode):
                return self.geojson_layer_to_dict(layerNode)
            if self.is_wfs_layer(layerNode):
                return self.wfs_layer_to_dict(layerNode)
            if self.is_geotiff_layer(layerNode):
                return self.geotiff_layer_to_dict(layerNode)

            error = {
                "error": "Unknown layer type",
            }
        except Exception as ex:
            error = {
                "error": str(ex),
            }
            logger.exception("Error exporting layer")

        return {
            "type": "unknown",
            **self.layer_commons_to_dict(layerNode),
            **error,
        }

    def determine_z_index(self, layerNode: QgsLayerTreeLayer) -> int:
        layer_order = self.root.layerOrder()
        num_layers = len(layer_order)
        z_index_multiplier = 10

        layer_index = layer_order.index(layerNode.layer())

        return (num_layers - layer_index) * z_index_multiplier

    def layer_commons_to_dict(self, layerNode: QgsLayerTreeLayer) -> JsonDict:
        layer = layerNode.layer()
        return {
            "title": layer.name(),
            "opacity": layer.opacity(),
            "visible": layerNode.isVisible(),
            "zIndex": self.determine_z_index(layerNode),
            "index": next(self.counter),
            "crs": layer.crs().authid(),
        }

    def is_xyz_layer(self, layerNode: QgsLayerTreeLayer) -> bool:
        layer = layerNode.layer()
        providerType = layer.providerType().lower()
        if providerType != "wms":
            return False

        source = layer.source()
        layer_props = parse_qs(source)

        if "type" in layer_props and layer_props["type"][0] == "xyz":
            return True

        return False

    def is_wmts_layer(self, layerNode: QgsLayerTreeLayer) -> bool:
        layer = layerNode.layer()
        providerType = layer.providerType().lower()
        if providerType != "wms":
            return False

        source = layer.source()
        layer_props = parse_qs(source)

        if "tileMatrixSet" in layer_props and "url" in layer_props:
            return True

        return False

    def is_wms_layer(self, layerNode: QgsLayerTreeLayer) -> bool:
        layer = layerNode.layer()
        providerType = layer.providerType().lower()
        if providerType != "wms":
            return False

        source = layer.source()
        layer_props = parse_qs(source)

        if "url" in layer_props:
            return True

        return False

    def is_kml_layer(self, layerNode: QgsLayerTreeLayer) -> bool:
        layer = layerNode.layer()
        providerType = layer.providerType().lower()
        if providerType != "ogr":
            return False

        source = layer.source()
        url = source.split("|")[0]

        if url.lower().endswith(".kml"):
            return True

        return False

    def is_geojson_layer(self, layerNode: QgsLayerTreeLayer) -> bool:
        layer = layerNode.layer()
        providerType = layer.providerType().lower()
        if providerType != "ogr":
            return False

        source = layer.source()
        url = source.split("|")[0]

        if url.lower().endswith(".geojson"):
            return True

        return False

    def is_wfs_layer(self, layerNode: QgsLayerTreeLayer) -> bool:
        layer = layerNode.layer()
        providerType = layer.providerType().lower()
        if providerType == "wfs":
            return True

        return False

    def is_geotiff_layer(self, layerNode: QgsLayerTreeLayer) -> bool:
        layer = layerNode.layer()
        providerType = layer.providerType().lower()
        source = layer.source().lower()
        file_extension = source.split(".")[-1]
        tiff_extensions = ["tif", "tiff"]

        if providerType == "gdal" and file_extension in tiff_extensions:
            return True

        return False

    def xyz_layer_to_dict(self, layerNode: QgsLayerTreeLayer) -> JsonDict:
        layer = layerNode.layer()
        source = layer.source()
        layer_props = parse_qs(source)
        url = layer_props["url"][0]
        return {
            "type": "xyz",
            **self.layer_commons_to_dict(layerNode),
            "url": url,
            "minZoom": layer_props.get("zmin", [None])[0],
            "maxZoom": layer_props.get("zmax", [None])[0],
        }

    def wmts_layer_to_dict(self, layerNode: QgsLayerTreeLayer) -> JsonDict:
        layer = layerNode.layer()
        source = layer.source()
        layer_props = parse_qs(source)
        url = layer_props["url"][0].split("?")[0]
        return {
            "type": "wmts",
            **self.layer_commons_to_dict(layerNode),
            "url": url,
            "layer": layer_props["layers"][0],
            "format": layer_props["format"][0],
        }

    def wms_layer_to_dict(self, layerNode: QgsLayerTreeLayer) -> JsonDict:
        layer = layerNode.layer()
        source = layer.source()
        layer_props = parse_qs(source)
        url = layer_props["url"][0].split("?")[0]
        return {
            "type": "wms",
            **self.layer_commons_to_dict(layerNode),
            "url": url,
            "layer": layer_props["layers"][0],
            "format": layer_props["format"][0],
        }

    def kml_layer_to_dict(self, layerNode: QgsLayerTreeLayer) -> JsonDict:
        layer = layerNode.layer()
        source = layer.source()
        props = source.split("|")
        url = props[0]

        return {
            "type": "kml",
            **self.layer_commons_to_dict(layerNode),
            "url": self.data_exporter.process_url(url),
        }

    def geojson_layer_to_dict(self, layerNode: QgsLayerTreeLayer) -> JsonDict:
        layer = layerNode.layer()
        source = layer.source()
        props = source.split("|")
        url = props[0]

        return {
            "type": "geojson",
            **self.layer_commons_to_dict(layerNode),
            "url": self.data_exporter.process_url(url),
            "style": extract_style(layerNode),
        }

    def wfs_layer_to_dict(self, layerNode: QgsLayerTreeLayer) -> JsonDict:
        layer = layerNode.layer()
        source = layer.source()
        props = parse_kv_pairs(source, item_sep=" ")

        url = props["url"]
        version = props["version"]

        if version not in ("1.0.0", "1.1.0", "2.0.0"):
            version = "1.1.0"

        return {
            "type": "wfs",
            **self.layer_commons_to_dict(layerNode),
            "url": self.data_exporter.process_url(url),
            "style": extract_style(layerNode),
            "layer": props["typename"],
            "version": version,
        }

    def geotiff_layer_to_dict(self, layerNode: QgsLayerTreeLayer) -> JsonDict:
        layer = layerNode.layer()
        url = layer.source()

        return {
            "type": "geotiff",
            **self.layer_commons_to_dict(layerNode),
            "url": self.data_exporter.process_url(url),
        }
