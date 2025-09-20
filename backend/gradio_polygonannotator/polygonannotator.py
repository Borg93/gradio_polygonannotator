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
    coordinates: List[List[float]]  # [[x1,y1], [x2,y2], ...]
    color: str  # hex color like "#FF0000"
    mask_opacity: Optional[float] = 0.2  # fill opacity from 0.0 to 1.0, default 0.2
    stroke_width: Optional[float] = 0.7  # stroke width in pixels, default 0.7
    stroke_opacity: Optional[float] = 0.6  # stroke opacity from 0.0 to 1.0, default 0.6
    selected_mask_opacity: Optional[float] = 0.5  # mask opacity when selected, default 0.5
    selected_stroke_opacity: Optional[float] = 1.0  # stroke opacity when selected, default 1.0


class PolygonAnnotatorData(GradioModel):
    image: FileData
    polygons: List[Polygon]
    selected_polygons: Optional[List[str]] = None  # List of IDs of the currently selected polygons


class PolygonAnnotator(Component):
    """
    Interactive polygon annotation component for visualizing and selecting polygon regions on images.

    The PolygonAnnotator displays an image with customizable polygon overlays that users can interact with.
    Features include multi-selection with Ctrl/Cmd+click, hover effects, and customizable appearance including
    stroke width, opacity settings for both fill and stroke, with separate settings for selected states.

    Perfect for:
    - Document layout analysis and region selection
    - Image segmentation visualization
    - Interactive annotation review and editing
    - Object detection result visualization
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
        """
        Parameters:
            value: Dictionary containing 'image' (FileData), 'polygons' (list with id, coordinates, color, opacities),
                and optionally 'selected_polygons' (list of selected IDs).
            label: Component label shown above the annotator.
            every: Continuously calls `value` to recalculate it if `value` is a function.
            inputs: Components used as inputs to calculate `value` if it's a function.
            show_label: Whether to display the label.
            show_download_button: Whether to show image download button.
            height: Component height in pixels or CSS units.
            width: Component width in pixels or CSS units.
            container: Whether to wrap component in a container with padding.
            scale: Relative size compared to adjacent components.
            min_width: Minimum pixel width before wrapping.
            interactive: Whether users can interact with polygons (selection/deselection).
            visible: Whether component is visible ("hidden" keeps it in DOM but invisible).
            elem_id: HTML DOM id for CSS targeting.
            elem_classes: HTML DOM classes for CSS targeting.
            render: Whether to render the component immediately.
            key: Key for maintaining component identity across re-renders.
            preserved_by_key: Parameters preserved across re-renders with same key.
        """
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
        """
        Parameters:
            payload: The component data containing image and polygon annotations.
        Returns:
            Dictionary with image path, polygon data including coordinates, colors, opacities,
            and the list of currently selected polygon IDs.
        """
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
                    "selected_stroke_opacity": p.selected_stroke_opacity
                }
                for p in payload.polygons
            ],
            "selected_polygons": payload.selected_polygons
        }

    def postprocess(self, value: dict | None) -> PolygonAnnotatorData | None:
        """
        Parameters:
            value: Dictionary containing 'image' (file path or URL), 'polygons' (list of polygon dictionaries
                   with id, coordinates, color, mask_opacity, stroke_width, stroke_opacity, and selection opacity settings),
                   and optionally 'selected_polygons' (list of selected polygon IDs).
        Returns:
            Processed component data ready for display.
        """
        if value is None:
            return None

        # Handle the image path
        image_path = value.get("image")
        if isinstance(image_path, str):
            image_data = FileData(path=image_path)
        else:
            return None

        # Handle polygons
        polygons = []
        for poly in value.get("polygons", []):
            polygons.append(
                Polygon(
                    id=poly["id"],
                    coordinates=poly["coordinates"],
                    color=poly.get("color", "#FF0000"),
                    mask_opacity=poly.get("mask_opacity", poly.get("opacity", 0.2)),  # Support old 'opacity' key for backwards compatibility
                    stroke_width=poly.get("stroke_width", 0.7),
                    stroke_opacity=poly.get("stroke_opacity", 0.6),
                    selected_mask_opacity=poly.get("selected_mask_opacity", 0.5),
                    selected_stroke_opacity=poly.get("selected_stroke_opacity", 1.0)
                )
            )

        return PolygonAnnotatorData(
            image=image_data,
            polygons=polygons,
            selected_polygons=value.get("selected_polygons")
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
                    "stroke_opacity": 0.6
                }
            ]
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
                    "stroke_opacity": 0.6
                },
                {
                    "id": "polygon2",
                    "coordinates": [[200, 100], [300, 100], [250, 200]],
                    "color": "#00FF00",
                    "mask_opacity": 0.2,
                    "stroke_width": 1,
                    "stroke_opacity": 0.8
                }
            ]
        }
