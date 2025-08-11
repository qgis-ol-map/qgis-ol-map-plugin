from typing import Any
from qgis._core import QgsLayerTreeLayer
import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)


def extract_color(value: str) -> str:
    r, g, b, a, *_ = value.split(",")
    a_float = float(a) / 255

    return f"rgb({r} {g} {b} / {a_float:.2f})"


def to_bool(value: str) -> bool:
    return value.lower()[:1] in ("1", "t", "y")


def extract_unit(value: str) -> str:
    if value.lower() == "point":
        return "pt"
    if value.lower() == "mm":
        return "mm"
    return "px"


STYLE_MAPPING: dict[str, tuple[str, str]] = {
    "symbol_size": (
        "./renderer-v2/symbols/symbol[@type='marker']/layer/Option/Option[@name='size']",
        "value",
    ),
    "symbol_size_unit": (
        "./renderer-v2/symbols/symbol[@type='marker']/layer/Option/Option[@name='size_unit']",
        "value",
    ),
    "symbol_fill_color": (
        "./renderer-v2/symbols/symbol[@type='marker']/layer/Option/Option[@name='color']",
        "value",
    ),
    "symbol_stroke_color": (
        "./renderer-v2/symbols/symbol[@type='marker']/layer/Option/Option[@name='outline_color']",
        "value",
    ),
    "symbol_stroke_width": (
        "./renderer-v2/symbols/symbol[@type='marker']/layer/Option/Option[@name='outline_width']",
        "value",
    ),
    "symbol_stroke_width_unit": (
        "./renderer-v2/symbols/symbol[@type='marker']/layer/Option/Option[@name='outline_width_unit']",
        "value",
    ),
    "label_text_field": (
        "./labeling/settings/text-style",
        "fieldName",
    ),
    "label_text_color": (
        "./labeling/settings/text-style",
        "textColor",
    ),
    "label_font_family": (
        "./labeling/settings/text-style",
        "fontFamily",
    ),
    "label_font_size": (
        "./labeling/settings/text-style",
        "fontSize",
    ),
    "label_font_size_unit": (
        "./labeling/settings/text-style",
        "fontSizeUnit",
    ),
    "label_font_weight": (
        "./labeling/settings/text-style",
        "fontWeight",
    ),
    "label_font_italic": (
        "./labeling/settings/text-style",
        "fontItalic",
    ),
    "label_outline_enabled": (
        "./labeling/settings/text-style/text-buffer",
        "bufferDraw",
    ),
    "label_outline_color": (
        "./labeling/settings/text-style/text-buffer",
        "bufferColor",
    ),
    "label_outline_width": (
        "./labeling/settings/text-style/text-buffer",
        "bufferSize",
    ),
    "label_outline_width_unit": (
        "./labeling/settings/text-style/text-buffer",
        "bufferSizeUnits",
    ),
    "polygon_fill_color": (
        "./renderer-v2/symbols/symbol[@type='fill']/layer/Option/Option[@name='color']",
        "value",
    ),
    "polygon_stroke_color": (
        "./renderer-v2/symbols/symbol[@type='fill']/layer/Option/Option[@name='outline_color']",
        "value",
    ),
    "polygon_stroke_width": (
        "./renderer-v2/symbols/symbol[@type='fill']/layer/Option/Option[@name='outline_width']",
        "value",
    ),
    "polygon_stroke_width_unit": (
        "./renderer-v2/symbols/symbol[@type='fill']/layer/Option/Option[@name='outline_width_unit']",
        "value",
    ),
    "line_stroke_color": (
        "./renderer-v2/symbols/symbol[@type='line']/layer/Option/Option[@name='line_color']",
        "value",
    ),
    "line_stroke_width": (
        "./renderer-v2/symbols/symbol[@type='line']/layer/Option/Option[@name='line_width']",
        "value",
    ),
    "line_stroke_width_unit": (
        "./renderer-v2/symbols/symbol[@type='line']/layer/Option/Option[@name='line_width_unit']",
        "value",
    ),
}

VALUE_CONVERTERS = {
    "symbol_size": float,
    "symbol_size_unit": extract_unit,
    "symbol_fill_color": extract_color,
    "symbol_stroke_color": extract_color,
    "symbol_stroke_width": float,
    "symbol_stroke_width_unit": extract_unit,
    "label_text_field": str,
    "label_text_color": extract_color,
    "label_font_family": str,
    "label_font_size": float,
    "label_font_size_unit": extract_unit,
    "label_font_weight": float,
    "label_font_italic": to_bool,
    "label_outline_enabled": to_bool,
    "label_outline_color": extract_color,
    "label_outline_width": float,
    "label_outline_width_unit": extract_unit,
    "polygon_fill_color": extract_color,
    "polygon_stroke_color": extract_color,
    "polygon_stroke_width": float,
    "polygon_stroke_width_unit": extract_unit,
    "line_stroke_color": extract_color,
    "line_stroke_width": float,
    "line_stroke_width_unit": extract_unit,
}


def extract_style(layer: QgsLayerTreeLayer) -> dict[str, Any]:
    style_manager = layer.layer().styleManager()
    style_name = style_manager.styles()[0]
    style = style_manager.style(style_name)
    xml_string = style.xmlData()

    root = ET.fromstring(xml_string)

    result: dict[str, Any] = {}
    for target, (source_xpath, field) in STYLE_MAPPING.items():
        el = root.find(source_xpath)
        if el is None:
            logger.warning("Cannot find field %s", source_xpath)
            continue

        converter = VALUE_CONVERTERS[target]
        result[target] = converter(el.attrib[field])

    return result
