# `gradio_polygonannotator`

## PolygonAnnotator - Interactive Polygon Selection for Gradio

A powerful Gradio custom component for interactive polygon annotations on images. Perfect for document layout analysis, image segmentation visualization, and interactive annotation workflows.

### Features

- 🖱️ **Interactive Selection**: Click to select/deselect polygons
- ⌨️ **Multi-Selection**: Ctrl/Cmd+Click for selecting multiple polygons
- ✨ **Hover Effects**: Visual feedback on mouse hover
- 🎨 **Customizable Appearance**: Control fill opacity, stroke width, and colors
- 🎯 **Separate Selection States**: Different visual states for selected polygons
- 📱 **Responsive**: Automatically adjusts to container size

## Installation

```bash
uv pip install gradio_polygonannotator
```

## Usage

```python
import gradio as gr
from gradio_polygonannotator import PolygonAnnotator

# Example data with polygons
example = {
    "image": "path/to/image.jpg",
    "polygons": [
        {
            "id": "polygon1",
            "coordinates": [[100, 100], [200, 100], [200, 200], [100, 200]],
            "color": "#FF6B6B",
            "mask_opacity": 0.2,
            "stroke_width": 1.0,
            "stroke_opacity": 0.8,
        }
    ]
}

def handle_selection(data, evt: gr.SelectData):
    """Handle polygon selection"""
    if evt.value:
        selected_ids = evt.value if isinstance(evt.value, list) else [evt.value]
        return f"Selected: {', '.join(selected_ids)}"
    return "No selection"

with gr.Blocks() as demo:
    annotator = PolygonAnnotator(
        value=example,
        label="Interactive Polygon Annotator",
        height=600
    )
    info = gr.Textbox(label="Selection Info")

    annotator.select(handle_selection, inputs=[annotator], outputs=[info])

demo.launch()
```

## API Reference

### PolygonAnnotator

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | dict | None | Dictionary containing image and polygon data |
| `label` | str | None | Component label |
| `height` | int/str | None | Component height |
| `width` | int/str | None | Component width |
| `interactive` | bool | True | Enable polygon interaction |
| `show_label` | bool | True | Show component label |
| `container` | bool | True | Wrap in container |
| `scale` | int | None | Relative size in layout |
| `min_width` | int | 160 | Minimum width in pixels |

#### Value Format

```python
{
    "image": FileData or str,  # Image file or URL
    "polygons": [
        {
            "id": str,  # Unique polygon identifier
            "coordinates": [[x, y], ...],  # Polygon vertices
            "color": str,  # Hex color (e.g., "#FF0000")
            "mask_opacity": float,  # Fill opacity (0-1)
            "stroke_width": float,  # Border width in pixels
            "stroke_opacity": float,  # Border opacity (0-1)
            "selected_mask_opacity": float,  # Fill opacity when selected
            "selected_stroke_opacity": float,  # Border opacity when selected
        }
    ],
    "selected_polygons": [str, ...]  # Currently selected polygon IDs
}
```

#### Events

| Event | Description | Event Data |
|-------|-------------|------------|
| `select` | Fired when polygons are selected/deselected | `evt.value`: List of selected polygon IDs |
| `change` | Fired when component value changes | Updated component value |

## Advanced Features

### Custom Selection States

Control visual appearance for different states:

```python
polygon = {
    "id": "region1",
    "coordinates": [[0, 0], [100, 0], [100, 100], [0, 100]],
    "color": "#4ECDC4",
    "mask_opacity": 0.15,  # Normal fill opacity
    "stroke_opacity": 0.6,  # Normal border opacity
    "selected_mask_opacity": 0.5,  # Fill when selected
    "selected_stroke_opacity": 1.0,  # Border when selected
}
```

### Programmatic Selection

Set selected polygons programmatically:

```python
annotator.value = {
    "image": image_data,
    "polygons": polygon_list,
    "selected_polygons": ["polygon1", "polygon2"]  # Pre-select polygons
}
```

## Development

### Building the Component

```bash
# Build the component
gradio cc build

# Install the built wheel
uv pip install dist/gradio_polygonannotator-*.whl
```

### Development Mode

```bash
# Install in development mode for testing
cd polygonannotator
uv pip install -e .

# Run the simple demo (for documentation)
uv run demo/app.py

# Run the full-featured demo
uv run demo.py
```

## License

Apache-2.0