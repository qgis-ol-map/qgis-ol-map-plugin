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
from .layer_exporter import LayerExporter
from .data_exporter import DataExporter
from itertools import count

JsonDict = dict[str, Any]


class ProjectExporter:
    def __init__(self, root: QgsLayerTree, target_path: str, data_dir_path: str) -> None:
        self.root = root
        self.counter = count()
        self.layer_exporter = LayerExporter(root, self.counter, DataExporter(data_dir_path))
        self.target_path = target_path

    def export(self):
        data = self.to_dict()
        path = Path(self.target_path)
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
        return self.layer_exporter.layer_to_dict(layerNode)

    def group_to_dict(self, groupNode: QgsLayerTreeGroup) -> JsonDict:
        return {
            "type": "group",
            "title": groupNode.name(),
            "index": next(self.counter),
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
