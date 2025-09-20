
# `gradio_polygonannotator`
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.1.0%20-%20orange"> <a href="https://github.com/yourusername/gradio-polygonannotator/issues" target="_blank"><img alt="Static Badge" src="https://img.shields.io/badge/Issues-white?logo=github&logoColor=black"></a> 

Interactive polygon annotation component for Gradio with multi-selection, hover effects, and customizable appearance

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
    """Handle polygon selection and display info"""
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
    gr.Markdown("""
    # PolygonAnnotator - Interactive Polygon Selection

    Click on polygons to select them. Use **Ctrl/Cmd+Click** for multiple selections.
    Click selected polygons to deselect.
    """)

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

## `PolygonAnnotator`

### Initialization

<table>
<thead>
<tr>
<th align="left">name</th>
<th align="left" style="width: 25%;">type</th>
<th align="left">default</th>
<th align="left">description</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><code>value</code></td>
<td align="left" style="width: 25%;">

```python
dict | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Dictionary containing 'image' (FileData), 'polygons' (list with id, coordinates, color, opacities),</td>
</tr>

<tr>
<td align="left"><code>label</code></td>
<td align="left" style="width: 25%;">

```python
str | I18nData | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Component label shown above the annotator.</td>
</tr>

<tr>
<td align="left"><code>every</code></td>
<td align="left" style="width: 25%;">

```python
Timer | float | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Continuously calls `value` to recalculate it if `value` is a function.</td>
</tr>

<tr>
<td align="left"><code>inputs</code></td>
<td align="left" style="width: 25%;">

```python
Component | Sequence[Component] | set[Component] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Components used as inputs to calculate `value` if it's a function.</td>
</tr>

<tr>
<td align="left"><code>show_label</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Whether to display the label.</td>
</tr>

<tr>
<td align="left"><code>show_download_button</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">Whether to show image download button.</td>
</tr>

<tr>
<td align="left"><code>height</code></td>
<td align="left" style="width: 25%;">

```python
int | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Component height in pixels or CSS units.</td>
</tr>

<tr>
<td align="left"><code>width</code></td>
<td align="left" style="width: 25%;">

```python
int | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Component width in pixels or CSS units.</td>
</tr>

<tr>
<td align="left"><code>container</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">Whether to wrap component in a container with padding.</td>
</tr>

<tr>
<td align="left"><code>scale</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Relative size compared to adjacent components.</td>
</tr>

<tr>
<td align="left"><code>min_width</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>160</code></td>
<td align="left">Minimum pixel width before wrapping.</td>
</tr>

<tr>
<td align="left"><code>interactive</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Whether users can interact with polygons (selection/deselection).</td>
</tr>

<tr>
<td align="left"><code>visible</code></td>
<td align="left" style="width: 25%;">

```python
bool | Literal["hidden"]
```

</td>
<td align="left"><code>True</code></td>
<td align="left">Whether component is visible ("hidden" keeps it in DOM but invisible).</td>
</tr>

<tr>
<td align="left"><code>elem_id</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">HTML DOM id for CSS targeting.</td>
</tr>

<tr>
<td align="left"><code>elem_classes</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">HTML DOM classes for CSS targeting.</td>
</tr>

<tr>
<td align="left"><code>render</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">Whether to render the component immediately.</td>
</tr>

<tr>
<td align="left"><code>key</code></td>
<td align="left" style="width: 25%;">

```python
int | str | tuple[int | str, ...] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Key for maintaining component identity across re-renders.</td>
</tr>

<tr>
<td align="left"><code>preserved_by_key</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | str | None
```

</td>
<td align="left"><code>"value"</code></td>
<td align="left">Parameters preserved across re-renders with same key.</td>
</tr>
</tbody></table>


### Events

| name | description |
|:-----|:------------|
| `clear` | This listener is triggered when the user clears the PolygonAnnotator using the clear button for the component. |
| `change` | Triggered when the value of the PolygonAnnotator changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input. |
| `upload` | This listener is triggered when the user uploads a file into the PolygonAnnotator. |
| `select` | Event listener for when the user selects or deselects the PolygonAnnotator. Uses event data gradio.SelectData to carry `value` referring to the label of the PolygonAnnotator, and `selected` to refer to state of the PolygonAnnotator. See EventData documentation on how to use this event data |



### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As output:** Is passed, dictionary with image path, polygon data including coordinates, colors, opacities,.
- **As input:** Should return, dictionary containing 'image' (file path or URL), 'polygons' (list of polygon dictionaries.

 ```python
 def predict(
     value: dict | None
 ) -> dict | None:
     return value
 ```
 
