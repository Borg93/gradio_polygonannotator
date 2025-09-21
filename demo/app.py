import gradio as gr
from gradio_polygonannotator import PolygonAnnotator

example_data = {
    "image": "https://images.unsplash.com/photo-1544816155-12df9643f363?w=800&h=1200",
    "polygons": [
        {
            "id": "complex_header",
            "coordinates": [
                [150, 120],
                [200, 100],
                [350, 110],
                [450, 95],
                [600, 120],
                [620, 180],
                [580, 220],
                [400, 240],
                [250, 235],
                [180, 200],
                [140, 160],
            ],
            "color": "#FF0000",
            "mask_opacity": 0.3,
            "stroke_width": 1.2,
            "stroke_opacity": 0.8,
            "selected_mask_opacity": 0.6,
            "selected_stroke_opacity": 1.0,
            "display_text": "Complex Header",
            "display_font_size": 14,
            "display_text_color": "#FFFFFF",
        },
        {
            "id": "overlapping_ribbon",
            "coordinates": [
                [300, 150],
                [550, 160],
                [580, 200],
                [650, 220],
                [680, 280],
                [620, 320],
                [500, 340],
                [350, 330],
                [200, 310],
                [180, 270],
                [220, 220],
                [280, 190],
            ],
            "color": "#00FF00",
            "mask_opacity": 0.25,
            "stroke_width": 1.5,
            "stroke_opacity": 0.7,
            "selected_mask_opacity": 0.5,
            "selected_stroke_opacity": 1.0,
            "display_text": "Overlapping Ribbon",
            "display_font_size": 14,
            "display_text_color": "#000000",
        },
        {
            "id": "irregular_content",
            "coordinates": [
                [120, 380],
                [250, 350],
                [400, 370],
                [550, 390],
                [720, 420],
                [750, 500],
                [780, 650],
                [720, 800],
                [650, 920],
                [500, 950],
                [300, 940],
                [150, 900],
                [80, 750],
                [90, 600],
                [110, 450],
            ],
            "color": "#0000FF",
            "mask_opacity": 0.2,
            "stroke_width": 0.8,
            "stroke_opacity": 0.6,
            "selected_mask_opacity": 0.4,
            "selected_stroke_opacity": 0.9,
            "display_text": "Irregular Content",
            "display_font_size": 14,
            "display_text_color": "#FFFF00",
        },
        {
            "id": "star_shaped",
            "coordinates": [
                [400, 850],
                [450, 900],
                [520, 910],
                [480, 970],
                [500, 1040],
                [400, 1000],
                [300, 1040],
                [320, 970],
                [280, 910],
                [350, 900],
            ],
            "color": "#FF00FF",
            "mask_opacity": 0.35,
            "stroke_width": 2.0,
            "stroke_opacity": 0.9,
            "selected_mask_opacity": 0.7,
            "selected_stroke_opacity": 1.0,
            "display_text": "Star Shape",
            "display_font_size": 14,
            "display_text_color": "#FFFFFF",
        },
        {
            "id": "overlapping_triangle",
            "coordinates": [
                [480, 600],
                [650, 750],
                [720, 850],
                [600, 920],
                [450, 880],
                [350, 800],
                [380, 700],
            ],
            "color": "#FFAA00",
            "mask_opacity": 0.28,
            "stroke_width": 1.8,
            "stroke_opacity": 0.75,
            "selected_mask_opacity": 0.55,
            "selected_stroke_opacity": 1.0,
            "display_text": "Triangle",
            "display_font_size": 14,
            "display_text_color": "#000000",
        },
    ],
}

polygon_table = [
    ["complex_header", "Complex Header", "#FF0000", 0.3, 1.2, 0.8],
    ["overlapping_ribbon", "Overlapping Ribbon", "#00FF00", 0.25, 1.5, 0.7],
    ["irregular_content", "Irregular Content", "#0000FF", 0.2, 0.8, 0.6],
    ["star_shaped", "Star Shape", "#FF00FF", 0.35, 2.0, 0.9],
    ["overlapping_triangle", "Triangle", "#FFAA00", 0.28, 1.8, 0.75],
]


def process_viewer_selection(data, evt: gr.SelectData):
    if evt.value and data:
        selected_ids = evt.value if isinstance(evt.value, list) else [evt.value]

        highlighted_table = []
        for row in polygon_table:
            if row[0] in selected_ids:
                highlighted_row = [
                    f"→ {row[0]} ←",
                    f"→ {row[1]} ←",
                    f"→ {row[2]} ←",
                    f"→ {row[3]} ←",
                    f"→ {row[4]} ←",
                    f"→ {row[5]} ←",
                ]
                highlighted_table.append(highlighted_row)
            else:
                highlighted_table.append(row)

        info_lines = [f"Selected {len(selected_ids)} polygon(s):"]
        for selected_id in selected_ids:
            selected_polygon = next(
                (p for p in data["polygons"] if p["id"] == selected_id), None
            )
            if selected_polygon:
                info_lines.append(
                    f"• {selected_id}: {selected_polygon['color']}, mask: {selected_polygon.get('mask_opacity', 0.2)}, stroke: {selected_polygon.get('stroke_width', 0.7)}px"
                )

        info_text = "\n".join(info_lines)
        return info_text, highlighted_table

    return "No polygons selected", polygon_table


def process_dataframe_selection(selected_data, evt: gr.SelectData):
    if evt.index is not None and evt.index[0] < len(polygon_table):
        selected_row = polygon_table[evt.index[0]]
        polygon_id = selected_row[0]

        updated_data = example_data.copy()
        updated_data["selected_polygons"] = [polygon_id]

        highlighted_table = []
        for i, row in enumerate(polygon_table):
            if i == evt.index[0]:
                highlighted_row = [
                    f"→ {row[0]} ←",
                    f"→ {row[1]} ←",
                    f"→ {row[2]} ←",
                    f"→ {row[3]} ←",
                    f"→ {row[4]} ←",
                    f"→ {row[5]} ←",
                ]
                highlighted_table.append(highlighted_row)
            else:
                highlighted_table.append(row)

        info_text = f"Selected polygon: {polygon_id}\nName: {selected_row[1]}\nColor: {selected_row[2]}\nMask Opacity: {selected_row[3]}\nStroke Width: {selected_row[4]}\nStroke Opacity: {selected_row[5]}"
        return updated_data, info_text, highlighted_table

    updated_data = example_data.copy()
    updated_data["selected_polygons"] = []
    return updated_data, "No polygons selected", polygon_table


def clear_selection():
    updated_data = example_data.copy()
    updated_data["selected_polygons"] = []
    return updated_data, "No polygons selected", polygon_table


def select_polygon_by_id(polygon_id):
    if not polygon_id or polygon_id.strip() == "":
        updated_data = example_data.copy()
        updated_data["selected_polygons"] = []
        return updated_data, "No polygons selected", polygon_table

    polygon_ids = [id.strip() for id in polygon_id.split(",") if id.strip()]
    valid_ids = [p["id"] for p in example_data["polygons"]]

    valid_selected_ids = [id for id in polygon_ids if id in valid_ids]
    invalid_ids = [id for id in polygon_ids if id not in valid_ids]

    if not valid_selected_ids:
        updated_data = example_data.copy()
        updated_data["selected_polygons"] = []
        error_msg = f"Invalid polygon ID(s): {', '.join(invalid_ids)}. Valid IDs: {', '.join(valid_ids)}"
        return updated_data, error_msg, polygon_table

    updated_data = example_data.copy()
    updated_data["selected_polygons"] = valid_selected_ids

    highlighted_table = []
    for row in polygon_table:
        if row[0] in valid_selected_ids:
            highlighted_row = [
                f"→ {row[0]} ←",
                f"→ {row[1]} ←",
                f"→ {row[2]} ←",
                f"→ {row[3]} ←",
                f"→ {row[4]} ←",
                f"→ {row[5]} ←",
            ]
            highlighted_table.append(highlighted_row)
        else:
            highlighted_table.append(row)

    info_lines = [f"Selected {len(valid_selected_ids)} polygon(s):"]
    for selected_id in valid_selected_ids:
        selected_polygon = next(
            (p for p in example_data["polygons"] if p["id"] == selected_id), None
        )
        if selected_polygon:
            info_lines.append(
                f"• {selected_id}: {selected_polygon['color']}, mask: {selected_polygon.get('mask_opacity', 0.2)}, stroke: {selected_polygon.get('stroke_width', 0.7)}px"
            )

    if invalid_ids:
        info_lines.append(f"\nInvalid IDs: {', '.join(invalid_ids)}")

    info_text = "\n".join(info_lines)
    return updated_data, info_text, highlighted_table


def toggle_text_display(current_data, show_text):
    if not current_data:
        return current_data

    updated_data = current_data.copy()
    updated_data["polygons"] = []

    for polygon in current_data.get("polygons", []):
        updated_polygon = polygon.copy()
        if not show_text:
            updated_polygon["display_font_size"] = 0
        else:
            original_polygon = next(
                (p for p in example_data["polygons"] if p["id"] == polygon["id"]), None
            )
            if original_polygon:
                updated_polygon["display_text"] = original_polygon.get(
                    "display_text", polygon["id"]
                )
                updated_polygon["display_font_size"] = original_polygon.get(
                    "display_font_size", 14
                )
                updated_polygon["display_text_color"] = original_polygon.get(
                    "display_text_color", "#000000"
                )

        updated_data["polygons"].append(updated_polygon)

    return updated_data


with gr.Blocks() as demo:
    gr.Markdown("""
    # PolygonAnnotator - Advanced Interactive Demo

    ## 🎮 Controls & Hotkeys

    ### Selection
    - **Click** on polygons or text labels to select/deselect
    - **Ctrl/Cmd+Click** for multiple selection
    - **Click dataframe rows** to select polygons
    - **Enter polygon IDs** manually in the textbox

    ### Navigation
    - **Mouse Wheel** - Zoom in/out at cursor position
    - **+/=** - Zoom in (10%)
    - **-** - Zoom out (10%)
    - **Ctrl/Cmd+0** - Reset view to original
    - **Arrow Keys** - Pan view (↑↓←→)
    - **Middle Mouse / Shift+Drag** - Pan view with mouse

    ### Features
    - **Clear button** to deselect all
    - **Toggle text display** checkbox for polygon labels
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
                value="Click on a polygon to see its information",
            )

            polygon_dataframe = gr.Dataframe(
                value=polygon_table,
                headers=["ID", "Name", "Color", "Mask", "Stroke W", "Stroke O"],
                label="Polygon Data (Click rows to select)",
                interactive=True,
            )

            clear_button = gr.Button("🗑️ Clear All Selections", variant="secondary")

            # Add text display toggle
            with gr.Row():
                show_text_checkbox = gr.Checkbox(
                    label="Show Polygon Text",
                    value=True,
                    info="Toggle text display on polygons",
                )

            with gr.Row():
                polygon_id_input = gr.Textbox(
                    label="Select by Polygon ID(s)",
                    placeholder="Enter single ID or comma-separated IDs (e.g., 'date_line' or 'date_line, salutation')",
                    scale=3,
                )
                select_button = gr.Button("Select", variant="primary", scale=1)

            gr.Markdown("""
            ### Features Demonstrated

            #### 🎨 Visual Customization
            - Different **mask opacity** for each polygon fill
            - Variable **stroke width** (0.5px to 1.5px)
            - Custom **stroke opacity** for borders
            - Enhanced appearance when selected
            - **Text labels** with customizable colors and sizes

            #### 🖱️ Interaction Methods
            1. **Direct Click**: Click polygons in the viewer
            2. **Multi-Selection**: Ctrl/Cmd+Click for multiple
            3. **Dataframe**: Click table rows
            4. **Text Input**: Type polygon IDs
            5. **Clear All**: Reset selection
            6. **Text Toggle**: Show/hide polygon labels

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
            - Toggle text display to see labels on polygons
            """)

    # Handle selection events
    poly_annotator.select(
        process_viewer_selection,
        inputs=[poly_annotator],
        outputs=[selected_info, polygon_dataframe],
    )

    polygon_dataframe.select(
        process_dataframe_selection,
        inputs=[polygon_dataframe],
        outputs=[poly_annotator, selected_info, polygon_dataframe],
    )

    clear_button.click(
        clear_selection, outputs=[poly_annotator, selected_info, polygon_dataframe]
    )

    select_button.click(
        select_polygon_by_id,
        inputs=[polygon_id_input],
        outputs=[poly_annotator, selected_info, polygon_dataframe],
    )

    # Also allow Enter key in textbox
    polygon_id_input.submit(
        select_polygon_by_id,
        inputs=[polygon_id_input],
        outputs=[poly_annotator, selected_info, polygon_dataframe],
    )

    # Handle text display toggle
    show_text_checkbox.change(
        toggle_text_display,
        inputs=[poly_annotator, show_text_checkbox],
        outputs=[poly_annotator],
    )

if __name__ == "__main__":
    demo.launch()
