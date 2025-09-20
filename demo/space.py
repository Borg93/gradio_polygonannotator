
import gradio as gr
from app import demo as app
import os

_docs = {'PolygonAnnotator': {'description': 'Interactive polygon annotation component for visualizing and selecting polygon regions on images.\n\nThe PolygonAnnotator displays an image with customizable polygon overlays that users can interact with.\nFeatures include multi-selection with Ctrl/Cmd+click, hover effects, and customizable appearance including\nstroke width, opacity settings for both fill and stroke, with separate settings for selected states.\n\nPerfect for:\n- Document layout analysis and region selection\n- Image segmentation visualization\n- Interactive annotation review and editing\n- Object detection result visualization', 'members': {'__init__': {'value': {'type': 'dict | None', 'default': 'None', 'description': "Dictionary containing 'image' (FileData), 'polygons' (list with id, coordinates, color, opacities),"}, 'label': {'type': 'str | I18nData | None', 'default': 'None', 'description': 'Component label shown above the annotator.'}, 'every': {'type': 'Timer | float | None', 'default': 'None', 'description': 'Continuously calls `value` to recalculate it if `value` is a function.'}, 'inputs': {'type': 'Component | Sequence[Component] | set[Component] | None', 'default': 'None', 'description': "Components used as inputs to calculate `value` if it's a function."}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'Whether to display the label.'}, 'show_download_button': {'type': 'bool', 'default': 'True', 'description': 'Whether to show image download button.'}, 'height': {'type': 'int | str | None', 'default': 'None', 'description': 'Component height in pixels or CSS units.'}, 'width': {'type': 'int | str | None', 'default': 'None', 'description': 'Component width in pixels or CSS units.'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'Whether to wrap component in a container with padding.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'Relative size compared to adjacent components.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'Minimum pixel width before wrapping.'}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': 'Whether users can interact with polygons (selection/deselection).'}, 'visible': {'type': 'bool | Literal["hidden"]', 'default': 'True', 'description': 'Whether component is visible ("hidden" keeps it in DOM but invisible).'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'HTML DOM id for CSS targeting.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'HTML DOM classes for CSS targeting.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'Whether to render the component immediately.'}, 'key': {'type': 'int | str | tuple[int | str, ...] | None', 'default': 'None', 'description': 'Key for maintaining component identity across re-renders.'}, 'preserved_by_key': {'type': 'list[str] | str | None', 'default': '"value"', 'description': 'Parameters preserved across re-renders with same key.'}}, 'postprocess': {'value': {'type': 'dict | None', 'description': "Dictionary containing 'image' (file path or URL), 'polygons' (list of polygon dictionaries"}}, 'preprocess': {'return': {'type': 'dict | None', 'description': 'Dictionary with image path, polygon data including coordinates, colors, opacities,'}, 'value': None}}, 'events': {'clear': {'type': None, 'default': None, 'description': 'This listener is triggered when the user clears the PolygonAnnotator using the clear button for the component.'}, 'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the PolygonAnnotator changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'upload': {'type': None, 'default': None, 'description': 'This listener is triggered when the user uploads a file into the PolygonAnnotator.'}, 'select': {'type': None, 'default': None, 'description': 'Event listener for when the user selects or deselects the PolygonAnnotator. Uses event data gradio.SelectData to carry `value` referring to the label of the PolygonAnnotator, and `selected` to refer to state of the PolygonAnnotator. See EventData documentation on how to use this event data'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'PolygonAnnotator': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_polygonannotator`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.1.0%20-%20orange"> <a href="https://github.com/yourusername/gradio-polygonannotator/issues" target="_blank"><img alt="Static Badge" src="https://img.shields.io/badge/Issues-white?logo=github&logoColor=black"></a> 
</div>

Interactive polygon annotation component for Gradio with multi-selection, hover effects, and customizable appearance
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_polygonannotator
```

## Usage

```python
import gradio as gr
from gradio_polygonannotator import PolygonAnnotator

# Example with document regions
example_data = {
    "image": "https://images.unsplash.com/photo-1544816155-12df9643f363?w=800&h=1200",
    "polygons": [
        {
            "id": "title",
            "coordinates": [[180, 150], [580, 150], [580, 200], [180, 200]],
            "color": "#FF6B6B",
            "mask_opacity": 0.15,
            "stroke_width": 1.0,
            "stroke_opacity": 0.8,
        },
        {
            "id": "paragraph_1",
            "coordinates": [[100, 400], [750, 400], [750, 600], [100, 600]],
            "color": "#4ECDC4",
            "mask_opacity": 0.15,
            "stroke_width": 0.7,
            "stroke_opacity": 0.6,
        },
        {
            "id": "paragraph_2",
            "coordinates": [[100, 650], [750, 650], [750, 950], [100, 950]],
            "color": "#4ECDC4",
            "mask_opacity": 0.15,
            "stroke_width": 0.7,
            "stroke_opacity": 0.6,
        },
        {
            "id": "signature",
            "coordinates": [[400, 1020], [650, 1020], [650, 1080], [400, 1080]],
            "color": "#FFE66D",
            "mask_opacity": 0.2,
            "stroke_width": 1.5,
            "stroke_opacity": 0.8,
        }
    ]
}

def handle_selection(data, evt: gr.SelectData):
    \"\"\"Handle polygon selection and display info\"\"\"
    if evt.value and data:
        selected_ids = evt.value if isinstance(evt.value, list) else [evt.value]
        info = f"Selected {len(selected_ids)} polygon(s):\n"
        for poly_id in selected_ids:
            polygon = next((p for p in data["polygons"] if p["id"] == poly_id), None)
            if polygon:
                info += f"• {poly_id}\n"
        return info
    return "Click on polygons to select them. Use Ctrl/Cmd+Click for multi-selection."

with gr.Blocks() as demo:
    gr.Markdown(\"\"\"
    # PolygonAnnotator - Interactive Polygon Selection

    Click on polygons to select them. Use **Ctrl/Cmd+Click** for multiple selections.
    Click selected polygons to deselect.
    \"\"\")

    with gr.Row():
        with gr.Column(scale=3):
            annotator = PolygonAnnotator(
                value=example_data,
                label="Document with Region Annotations",
                height=600,
            )

        with gr.Column(scale=1):
            selected_info = gr.Textbox(
                label="Selected Regions",
                lines=6,
                value="Click on polygons to select them. Use Ctrl/Cmd+Click for multi-selection."
            )

    # Handle selection events
    annotator.select(
        handle_selection,
        inputs=[annotator],
        outputs=[selected_info]
    )

if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `PolygonAnnotator`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["PolygonAnnotator"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["PolygonAnnotator"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, dictionary with image path, polygon data including coordinates, colors, opacities,.
- **As output:** Should return, dictionary containing 'image' (file path or URL), 'polygons' (list of polygon dictionaries.

 ```python
def predict(
    value: dict | None
) -> dict | None:
    return value
```
""", elem_classes=["md-custom", "PolygonAnnotator-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          PolygonAnnotator: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
