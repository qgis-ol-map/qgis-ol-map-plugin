from qgis._core import (
    QgsLayerTreeGroup,
    QgsLayerTreeLayer,
    QgsLayerTree,
    QgsLayerTreeNode,
    QgsCoordinateReferenceSystem,
    Qgis,
)
from typing import Any
from pathlib import Path
import json
from .layer_exporter import layer_to_dict


JsonDict = dict[str, Any]


class ProjectExporter:
    def __init__(self, root: QgsLayerTree) -> None:
        self.root = root

    def export(self, target_path: str):
        data = self.to_dict()
        path = Path(target_path)
        with path.open("w") as f:
            json.dump(data, f, indent=4)

    def to_dict(self) -> JsonDict:
        return {
            "epsgs": self.epsgs_to_dict(
                [layerNode.layer().crs() for layerNode in self.root.findLayers()]
            ),
            "layers": self.children_to_dict(self.root.children()),
        }

    def layer_to_dict(self, layerNode: QgsLayerTreeLayer) -> JsonDict:
        return layer_to_dict(self.root, layerNode)

    def group_to_dict(self, groupNode: QgsLayerTreeGroup) -> JsonDict:
        return {
            "type": "group",
            "title": groupNode.name(),
            "visible": groupNode.isVisible(),
            "layers": self.children_to_dict(groupNode.children()),
        }

    def _child_to_id_and_dict(self, child: QgsLayerTreeNode) -> tuple[str, JsonDict]:
        if isinstance(child, QgsLayerTreeGroup):
            return (child.name(), self.group_to_dict(child))
        if isinstance(child, QgsLayerTreeLayer):
            return (child.layerId(), self.layer_to_dict(child))
        raise ValueError(f"Node of unsupported type: {child}")

    def children_to_dict(self, children: list[QgsLayerTreeNode]) -> dict[str, JsonDict]:
        return dict(self._child_to_id_and_dict(child) for child in children)

    def epsgs_to_dict(
        self, epsgs: list[QgsCoordinateReferenceSystem]
    ) -> dict[str, str]:
        return {epsg.authid(): self.epsg_to_str(epsg) for epsg in epsgs}

    def epsg_to_str(self, epsg: QgsCoordinateReferenceSystem) -> str:
        proj4_str = epsg.toProj4()
        if epsg.axisOrdering() == [
            Qgis.CrsAxisDirection.North,
            Qgis.CrsAxisDirection.East,
        ]:
            proj4_str += " +axis=neu"
        return proj4_str
