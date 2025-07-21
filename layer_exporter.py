from qgis._core import QgsLayerTreeLayer
from typing import Any
from urllib.parse import parse_qs

JsonDict = dict[str, Any]


def layer_to_dict(layerNode: QgsLayerTreeLayer) -> JsonDict:
    try:
        if is_xyz_layer(layerNode):
            return xyz_layer_to_dict(layerNode)
        if is_wmts_layer(layerNode):
            return wmts_layer_to_dict(layerNode)
        if is_wms_layer(layerNode):
            return wms_layer_to_dict(layerNode)

        error = {
            "error": "Unknown layer type",
        }
    except Exception as ex:
        error = {
            "error": str(ex),
        }

    return {
        "type": "unknown",
        **layer_commons_to_dict(layerNode),
        **error,
    }

def layer_commons_to_dict(layerNode: QgsLayerTreeLayer) -> JsonDict:
    layer = layerNode.layer()
    return {
        "title": layer.name(),
        "opacity": layer.opacity(),
        "visible": layerNode.isVisible(),
        "crs": layer.crs().authid(),
    }


def is_xyz_layer(layerNode: QgsLayerTreeLayer) -> bool:
    layer = layerNode.layer()
    providerType = layer.providerType().lower()
    if providerType != "wms":
        return False

    source = layer.source()
    layer_props = parse_qs(source)

    if "type" in layer_props and layer_props["type"][0] == "xyz":
        return True

    return False


def is_wmts_layer(layerNode: QgsLayerTreeLayer) -> bool:
    layer = layerNode.layer()
    providerType = layer.providerType().lower()
    if providerType != "wms":
        return False

    source = layer.source()
    layer_props = parse_qs(source)

    if "tileMatrixSet" in layer_props and "url" in layer_props:
        return True

    return False


def is_wms_layer(layerNode: QgsLayerTreeLayer) -> bool:
    layer = layerNode.layer()
    providerType = layer.providerType().lower()
    if providerType != "wms":
        return False

    source = layer.source()
    layer_props = parse_qs(source)

    if "url" in layer_props:
        return True

    return False


def xyz_layer_to_dict(layerNode: QgsLayerTreeLayer) -> JsonDict:
    layer = layerNode.layer()
    source = layer.source()
    layer_props = parse_qs(source)
    url = layer_props["url"][0]
    return {
        "type": "xyz",
        **layer_commons_to_dict(layerNode),
        "url": url,
    }


def wmts_layer_to_dict(layerNode: QgsLayerTreeLayer) -> JsonDict:
    layer = layerNode.layer()
    source = layer.source()
    layer_props = parse_qs(source)
    url = layer_props["url"][0].split("?")[0]
    return {
        "type": "wmts",
        **layer_commons_to_dict(layerNode),
        "url": url,
        "layer": layer_props["layers"][0],
        "format": layer_props["format"][0],
    }


def wms_layer_to_dict(layerNode: QgsLayerTreeLayer) -> JsonDict:
    layer = layerNode.layer()
    source = layer.source()
    layer_props = parse_qs(source)
    url = layer_props["url"][0].split("?")[0]
    return {
        "type": "wms",
        **layer_commons_to_dict(layerNode),
        "url": url,
        "layer": layer_props["layers"][0],
        "format": layer_props["format"][0],
    }
