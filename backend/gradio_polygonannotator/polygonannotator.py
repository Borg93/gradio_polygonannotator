"""gr.PolygonAnnotator() component for interactive polygon annotations."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Literal, List, Optional

from gradio_client import handle_file

from gradio.components.base import Component
from gradio.data_classes import FileData, GradioModel
from gradio.events import Events
from gradio.i18n import I18nData

if TYPE_CHECKING:
    from gradio.components import Timer


class Polygon(GradioModel):
    id: str
    coordinates: List[List[float]]
    color: str
    mask_opacity: Optional[float] = 0.2
    stroke_width: Optional[float] = 0.7
    stroke_opacity: Optional[float] = 0.6
    selected_mask_opacity: Optional[float] = 0.5
    selected_stroke_opacity: Optional[float] = 1.0
    display_text: Optional[str] = None
    display_font_size: Optional[float] = None
    display_text_color: Optional[str] = "#000000"


class PolygonAnnotatorData(GradioModel):
    image: FileData
    polygons: List[Polygon]
    selected_polygons: Optional[List[str]] = None


class PolygonAnnotator(Component):
    """
    Interactive polygon annotation component for visualizing and selecting polygon regions on images.
    """

    EVENTS = [
        Events.clear,
        Events.change,
        Events.upload,
        Events.select,
    ]

    data_model = PolygonAnnotatorData

    def __init__(
        self,
        value: dict | None = None,
        *,
        label: str | I18nData | None = None,
        every: Timer | float | None = None,
        inputs: Component | Sequence[Component] | set[Component] | None = None,
        show_label: bool | None = None,
        show_download_button: bool = True,
        height: int | str | None = None,
        width: int | str | None = None,
        container: bool = True,
        scale: int | None = None,
        min_width: int = 160,
        interactive: bool | None = None,
        visible: bool | Literal["hidden"] = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | tuple[int | str, ...] | None = None,
        preserved_by_key: list[str] | str | None = "value",
    ):
        self.show_download_button = show_download_button
        self.height = height
        self.width = width
        super().__init__(
            label=label,
            every=every,
            inputs=inputs,
            show_label=show_label,
            container=container,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            key=key,
            preserved_by_key=preserved_by_key,
            value=value,
        )

    def preprocess(self, payload: PolygonAnnotatorData | None) -> dict | None:
        if payload is None:
            return None
        return {
            "image": payload.image.path,
            "polygons": [
                {
                    "id": p.id,
                    "coordinates": p.coordinates,
                    "color": p.color,
                    "mask_opacity": p.mask_opacity,
                    "stroke_width": p.stroke_width,
                    "stroke_opacity": p.stroke_opacity,
                    "selected_mask_opacity": p.selected_mask_opacity,
                    "selected_stroke_opacity": p.selected_stroke_opacity,
                    "display_text": p.display_text,
                    "display_font_size": p.display_font_size,
                    "display_text_color": p.display_text_color,
                }
                for p in payload.polygons
            ],
            "selected_polygons": payload.selected_polygons,
        }

    def postprocess(self, value: dict | None) -> PolygonAnnotatorData | None:
        if value is None:
            return None

        image_path = value.get("image")
        if isinstance(image_path, str):
            image_data = FileData(path=image_path)
        else:
            return None

        polygons = []
        for poly in value.get("polygons", []):
            polygons.append(
                Polygon(
                    id=poly["id"],
                    coordinates=poly["coordinates"],
                    color=poly.get("color", "#FF0000"),
                    mask_opacity=poly.get("mask_opacity", poly.get("opacity", 0.2)),
                    stroke_width=poly.get("stroke_width", 0.7),
                    stroke_opacity=poly.get("stroke_opacity", 0.6),
                    selected_mask_opacity=poly.get("selected_mask_opacity", 0.5),
                    selected_stroke_opacity=poly.get("selected_stroke_opacity", 1.0),
                    display_text=poly.get("display_text", None),
                    display_font_size=poly.get("display_font_size", None),
                    display_text_color=poly.get("display_text_color", "#000000"),
                )
            )

        return PolygonAnnotatorData(
            image=image_data,
            polygons=polygons,
            selected_polygons=value.get("selected_polygons"),
        )

    def example_payload(self) -> Any:
        return {
            "image": handle_file(
                "https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png"
            ),
            "polygons": [
                {
                    "id": "polygon1",
                    "coordinates": [[50, 50], [150, 50], [150, 150], [50, 150]],
                    "color": "#FF0000",
                    "mask_opacity": 0.2,
                    "stroke_width": 0.7,
                    "stroke_opacity": 0.6,
                }
            ],
        }

    def example_value(self) -> Any:
        return {
            "image": "https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png",
            "polygons": [
                {
                    "id": "polygon1",
                    "coordinates": [[50, 50], [150, 50], [150, 150], [50, 150]],
                    "color": "#FF0000",
                    "mask_opacity": 0.2,
                    "stroke_width": 0.7,
                    "stroke_opacity": 0.6,
                },
                {
                    "id": "polygon2",
                    "coordinates": [[200, 100], [300, 100], [250, 200]],
                    "color": "#00FF00",
                    "mask_opacity": 0.2,
                    "stroke_width": 1,
                    "stroke_opacity": 0.8,
                },
            ],
        }
