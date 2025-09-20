import gradio as gr
from gradio_polygonannotator import PolygonAnnotator
from typing import Literal

example_data = {
    "image": "https://images.unsplash.com/photo-1544816155-12df9643f363?w=800&h=1200",
    "polygons": [
        {
            "id": "date_line",
            "coordinates": [[180, 150], [580, 150], [580, 200], [180, 200]],
            "color": "#FF0000",
            "mask_opacity": 0.2,
            "stroke_width": 0.7,
            "stroke_opacity": 0.6,
            "selected_mask_opacity": 0.5,
            "selected_stroke_opacity": 1.0
        },
        {
            "id": "salutation",
            "coordinates": [[180, 280], [680, 280], [680, 340], [180, 340]],
            "color": "#00FF00",
            "mask_opacity": 0.2,
            "stroke_width": 1.0,
            "stroke_opacity": 0.6,
            "selected_mask_opacity": 0.4,
            "selected_stroke_opacity": 0.9
        },
        {
            "id": "main_text_block",
            "coordinates": [[100, 400], [750, 400], [750, 950], [100, 950]],
            "color": "#0000FF",
            "mask_opacity": 0.15,
            "stroke_width": 0.5,
            "stroke_opacity": 0.5,
            "selected_mask_opacity": 0.4,
            "selected_stroke_opacity": 0.8
        },
        {
            "id": "closing_signature",
            "coordinates": [[400, 1020], [650, 1020], [650, 1080], [400, 1080]],
            "color": "#FFFF00",
            "mask_opacity": 0.25,
            "stroke_width": 1.5,
            "stroke_opacity": 0.7,
            "selected_mask_opacity": 0.6,
            "selected_stroke_opacity": 1.0
        }
    ]
}

# Create dataframe data from polygon information
polygon_table = [
    ["date_line", "Date Line", "#FF0000", 0.2, 0.7, 0.6],
    ["salutation", "Salutation", "#00FF00", 0.2, 1.0, 0.6],
    ["main_text_block", "Main Text Block", "#0000FF", 0.15, 0.5, 0.5],
    ["closing_signature", "Closing/Signature", "#FFFF00", 0.25, 1.5, 0.7]
]

def process_viewer_selection(data, evt: gr.SelectData):
    """Handle polygon selection from viewer and update dataframe selection"""
    if evt.value and data:
        selected_ids = evt.value if isinstance(evt.value, list) else [evt.value]

        # Create highlighted dataframe data
        highlighted_table = []
        for row in polygon_table:
            if row[0] in selected_ids:  # If this is a selected row
                # Add highlighting markers to the selected row
                highlighted_row = [f"→ {row[0]} ←", f"→ {row[1]} ←", f"→ {row[2]} ←", f"→ {row[3]} ←", f"→ {row[4]} ←", f"→ {row[5]} ←"]
                highlighted_table.append(highlighted_row)
            else:
                highlighted_table.append(row)

        # Create info text for all selected polygons
        info_lines = [f"Selected {len(selected_ids)} polygon(s):"]
        for selected_id in selected_ids:
            selected_polygon = next((p for p in data["polygons"] if p["id"] == selected_id), None)
            if selected_polygon:
                info_lines.append(f"• {selected_id}: {selected_polygon['color']}, mask: {selected_polygon.get('mask_opacity', 0.2)}, stroke: {selected_polygon.get('stroke_width', 0.7)}px")

        info_text = "\n".join(info_lines)
        return info_text, highlighted_table

    return "No polygons selected", polygon_table

def process_dataframe_selection(selected_data, evt: gr.SelectData):
    """Handle row selection from dataframe and update viewer selection"""
    if evt.index is not None and evt.index[0] < len(polygon_table):
        selected_row = polygon_table[evt.index[0]]
        polygon_id = selected_row[0]

        # Update the viewer data with the selected polygon
        updated_data = example_data.copy()
        updated_data["selected_polygons"] = [polygon_id]

        info_text = f"Selected polygon: {polygon_id}\nName: {selected_row[1]}\nColor: {selected_row[2]}\nMask Opacity: {selected_row[3]}\nStroke Width: {selected_row[4]}\nStroke Opacity: {selected_row[5]}"
        return updated_data, info_text

    # Deselection
    updated_data = example_data.copy()
    updated_data["selected_polygons"] = []
    return updated_data, "No polygons selected"

def clear_selection():
    """Clear polygon selection"""
    updated_data = example_data.copy()
    updated_data["selected_polygons"] = []
    return updated_data, "No polygons selected", polygon_table

def select_polygon_by_id(polygon_id):
    """Select polygon by ID from textbox input"""
    if not polygon_id or polygon_id.strip() == "":
        # Empty input - clear selection
        updated_data = example_data.copy()
        updated_data["selected_polygons"] = []
        return updated_data, "No polygons selected", polygon_table

    # Handle multiple IDs (comma-separated)
    polygon_ids = [id.strip() for id in polygon_id.split(",") if id.strip()]
    valid_ids = [p["id"] for p in example_data["polygons"]]

    # Filter to only valid IDs
    valid_selected_ids = [id for id in polygon_ids if id in valid_ids]
    invalid_ids = [id for id in polygon_ids if id not in valid_ids]

    if not valid_selected_ids:
        # No valid IDs
        updated_data = example_data.copy()
        updated_data["selected_polygons"] = []
        error_msg = f"Invalid polygon ID(s): {', '.join(invalid_ids)}. Valid IDs: {', '.join(valid_ids)}"
        return updated_data, error_msg, polygon_table

    # Valid IDs - select polygons
    updated_data = example_data.copy()
    updated_data["selected_polygons"] = valid_selected_ids

    # Create highlighted dataframe data
    highlighted_table = []
    for row in polygon_table:
        if row[0] in valid_selected_ids:  # If this is a selected row
            # Add highlighting markers to the selected row
            highlighted_row = [f"→ {row[0]} ←", f"→ {row[1]} ←", f"→ {row[2]} ←", f"→ {row[3]} ←", f"→ {row[4]} ←", f"→ {row[5]} ←"]
            highlighted_table.append(highlighted_row)
        else:
            highlighted_table.append(row)

    # Create info text
    info_lines = [f"Selected {len(valid_selected_ids)} polygon(s):"]
    for selected_id in valid_selected_ids:
        selected_polygon = next((p for p in example_data["polygons"] if p["id"] == selected_id), None)
        if selected_polygon:
            info_lines.append(f"• {selected_id}: {selected_polygon['color']}, mask: {selected_polygon.get('mask_opacity', 0.2)}, stroke: {selected_polygon.get('stroke_width', 0.7)}px")

    if invalid_ids:
        info_lines.append(f"\nInvalid IDs: {', '.join(invalid_ids)}")

    info_text = "\n".join(info_lines)
    return updated_data, info_text, highlighted_table

with gr.Blocks() as demo:
    gr.Markdown("""
    # PolygonAnnotator - Advanced Interactive Demo

    This demo showcases all the features of the PolygonAnnotator component:
    - **Click** on polygons to select/deselect them
    - **Ctrl/Cmd+Click** for multiple selection
    - **Click dataframe rows** to select polygons
    - **Enter polygon IDs** manually in the textbox
    - **Clear button** to deselect all
    """)

    with gr.Row():
        with gr.Column(scale=2):
            poly_annotator = PolygonAnnotator(
                value=example_data,
                label="Document with Interactive Polygon Annotations",
                height=600,
            )

        with gr.Column(scale=1):
            selected_info = gr.Textbox(
                label="Selected Polygon Information",
                lines=5,
                value="Click on a polygon to see its information"
            )

            polygon_dataframe = gr.Dataframe(
                value=polygon_table,
                headers=["ID", "Name", "Color", "Mask", "Stroke W", "Stroke O"],
                label="Polygon Data (Click rows to select)",
                datatype=[Literal["str", "str", "str", "number", "number", "number"]],
                interactive=True
            )

            clear_button = gr.Button("🗑️ Clear All Selections", variant="secondary")

            with gr.Row():
                polygon_id_input = gr.Textbox(
                    label="Select by Polygon ID(s)",
                    placeholder="Enter single ID or comma-separated IDs (e.g., 'date_line' or 'date_line, salutation')",
                    scale=3
                )
                select_button = gr.Button("Select", variant="primary", scale=1)

            gr.Markdown("""
            ### Features Demonstrated

            #### 🎨 Visual Customization
            - Different **mask opacity** for each polygon fill
            - Variable **stroke width** (0.5px to 1.5px)
            - Custom **stroke opacity** for borders
            - Enhanced appearance when selected

            #### 🖱️ Interaction Methods
            1. **Direct Click**: Click polygons in the viewer
            2. **Multi-Selection**: Ctrl/Cmd+Click for multiple
            3. **Dataframe**: Click table rows
            4. **Text Input**: Type polygon IDs
            5. **Clear All**: Reset selection

            #### 📝 Polygon IDs
            - `date_line` - Red header area
            - `salutation` - Green greeting section
            - `main_text_block` - Blue main content
            - `closing_signature` - Yellow signature area

            #### 💡 Tips
            - Hover over polygons for visual feedback
            - Selected polygons have increased opacity
            - Use comma-separated IDs for batch selection
            - Click selected polygons to deselect them
            """)

    # Handle selection events
    poly_annotator.select(
        process_viewer_selection,
        inputs=[poly_annotator],
        outputs=[selected_info, polygon_dataframe]
    )

    polygon_dataframe.select(
        process_dataframe_selection,
        inputs=[polygon_dataframe],
        outputs=[poly_annotator, selected_info]
    )

    clear_button.click(
        clear_selection,
        outputs=[poly_annotator, selected_info, polygon_dataframe]
    )

    select_button.click(
        select_polygon_by_id,
        inputs=[polygon_id_input],
        outputs=[poly_annotator, selected_info, polygon_dataframe]
    )

    # Also allow Enter key in textbox
    polygon_id_input.submit(
        select_polygon_by_id,
        inputs=[polygon_id_input],
        outputs=[poly_annotator, selected_info, polygon_dataframe]
    )

if __name__ == "__main__":
    demo.launch()
