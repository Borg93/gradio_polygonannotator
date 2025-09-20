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
