from qgis.core import QgsCoordinateTransform, QgsCoordinateReferenceSystem, QgsProject

from qgis.gui import QgsMapCanvas


def extract_center(qgis_instance, map_canvas: QgsMapCanvas):
    """Converts a point geometry to EPSG:4326"""

    crs_source = qgis_instance.crs()
    center_point = map_canvas.center()
    crs_destination = QgsCoordinateReferenceSystem("EPSG:4326")
    transform = QgsCoordinateTransform(crs_source, crs_destination, qgis_instance)
    transformed_point = transform.transform(center_point)

    return {
        "crs": "EPSG:4326",
        "x": transformed_point.x(),
        "y": transformed_point.y(),
    }


def scale_to_zoom(scale: float) -> int:
    # source https://wiki.openstreetmap.org/wiki/Zoom_levels
    scale_to_zoom: dict[int, int] = {
        500000000: 0,
        250000000: 1,
        150000000: 2,
        70000000: 3,
        35000000: 4,
        15000000: 5,
        10000000: 6,
        4000000: 7,
        2000000: 8,
        1000000: 9,
        500000: 10,
        250000: 11,
        150000: 12,
        70000: 13,
        35000: 14,
        15000: 15,
        8000: 16,
        4000: 17,
        2000: 18,
        1000: 19,
        500: 20,
    }

    closest_scale = min(scale_to_zoom.keys(), key=lambda x: abs(x - scale))
    return scale_to_zoom[closest_scale]


def extract_zoom(map_canvas: QgsMapCanvas) -> int:
    return scale_to_zoom(map_canvas.scale())


def export_viewport(qgis_instance: QgsProject, map_canvas: QgsMapCanvas):
    return {
        "center": extract_center(qgis_instance, map_canvas),
        "zoom": extract_zoom(map_canvas),
    }
