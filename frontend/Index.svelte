<svelte:options accessors={true} />

<script lang="ts">
    import { onMount, onDestroy, tick } from "svelte";
    import {
        Application,
        Container,
        Graphics,
        Text,
        Sprite,
        Texture,
        TextStyle,
    } from "pixi.js";
    import type { Gradio } from "@gradio/utils";
    import { Block, BlockLabel } from "@gradio/atoms";
    import { Image as ImageIcon } from "@gradio/icons";
    import { StatusTracker } from "@gradio/statustracker";
    import type { LoadingStatus } from "@gradio/statustracker";
    import type { FileData } from "@gradio/client";

    export let elem_id = "";
    export let elem_classes: string[] = [];
    export let visible: boolean | "hidden" = true;
    export let value: {
        image: FileData;
        polygons: Array<{
            id: string;
            coordinates: number[][];
            color: string;
            mask_opacity?: number;
            stroke_width?: number;
            stroke_opacity?: number;
            selected_mask_opacity?: number;
            selected_stroke_opacity?: number;
            display_text?: string | null;
            display_font_size?: number | null;
            display_text_color?: string;
        }>;
        selected_polygons?: string[] | null;
    } | null = null;
    export let label: string;
    export let show_label: boolean;
    export let height: number | string | undefined = undefined;
    export let width: number | string | undefined = undefined;
    export let container = true;
    export let scale: number | null = null;
    export let min_width: number | undefined = undefined;
    export let loading_status: LoadingStatus;
    export let root: string;

    export let gradio: Gradio<{
        change: never;
        upload: never;
        clear: never;
        select: { index: number | null; value: any };
        clear_status: LoadingStatus;
    }>;

    let canvasContainer: HTMLDivElement;
    let app: Application;
    let imageSprite: Sprite | null = null;
    let polygonGraphics: Map<string, Graphics> = new Map();
    let polygonTexts: Map<string, Text> = new Map();
    let textContainer: Container | null = null;
    let selectedPolygonIds: string[] = [];
    let viewportContainer: Container | null = null;
    let isDragging = false;
    let lastPointerPosition = { x: 0, y: 0 };
    let initialScale = 1;
    let initialPosition = { x: 0, y: 0 };
    let minScale = 0.5;
    let maxScale = 3;

    type ImageRect = {
        left: number;
        top: number;
        right: number;
        bottom: number;
        width: number;
        height: number;
        naturalWidth: number;
        naturalHeight: number;
    };

    let imageRect: ImageRect = {
        left: 0,
        top: 0,
        right: 1,
        bottom: 1,
        width: 1,
        height: 1,
        naturalWidth: 2,
        naturalHeight: 2,
    };

    $: (value, handleValueChange());

    async function handleValueChange() {
        if (!app || !value) return;
        selectedPolygonIds = value.selected_polygons || [];
        await renderAnnotations();
    }

    function updateSelection(newSelectedIds: string[]) {
        if (!value || !imageSprite) return;

        polygonGraphics.forEach((graphics, polygonId) => {
            const polygon = value.polygons.find((p) => p.id === polygonId);
            if (!polygon) return;

            const originalMaskAlpha = polygon.mask_opacity ?? 0.2;
            const selectedMaskAlpha = polygon.selected_mask_opacity ?? 0.5;
            const originalStrokeAlpha = polygon.stroke_opacity ?? 0.6;
            const selectedStrokeAlpha = polygon.selected_stroke_opacity ?? 1.0;
            const strokeWidth = polygon.stroke_width ?? 0.7;

            graphics.clear();
            if (newSelectedIds.includes(polygonId)) {
                drawPolygonPath(
                    graphics,
                    polygon,
                    selectedMaskAlpha,
                    strokeWidth,
                    selectedStrokeAlpha,
                );
            } else {
                drawPolygonPath(
                    graphics,
                    polygon,
                    originalMaskAlpha,
                    strokeWidth,
                    originalStrokeAlpha,
                );
            }
        });
    }

    function handlePolygonSelection(polygonId: string, event: any) {
        if (!value) return;

        const isMultiSelect = event.ctrlKey || event.metaKey;

        if (selectedPolygonIds.includes(polygonId)) {
            const newSelectedIds = selectedPolygonIds.filter(
                (id) => id !== polygonId,
            );
            updateSelection(newSelectedIds);
            selectedPolygonIds = newSelectedIds;

            gradio.dispatch("select", {
                index:
                    newSelectedIds.length > 0
                        ? value.polygons.findIndex(
                              (p) =>
                                  p.id ===
                                  newSelectedIds[
                                      newSelectedIds.length - 1
                                  ],
                          )
                        : null,
                value:
                    newSelectedIds.length > 0
                        ? newSelectedIds
                        : null,
            });
            return;
        }

        let newSelectedIds: string[];
        if (isMultiSelect) {
            newSelectedIds = [...selectedPolygonIds, polygonId];
        } else {
            newSelectedIds = [polygonId];
        }

        updateSelection(newSelectedIds);
        selectedPolygonIds = newSelectedIds;

        gradio.dispatch("select", {
            index: value.polygons.findIndex(
                (p) => p.id === polygonId,
            ),
            value: newSelectedIds,
        });
    }

    async function initPixiApp() {
        if (!canvasContainer) return;

        const containerWidth = canvasContainer.clientWidth || 800;
        const containerHeight = canvasContainer.clientHeight || 600;

        app = new Application();
        await app.init({
            width: containerWidth,
            height: containerHeight,
            backgroundColor: 0xf0f0f0,
            antialias: true,
            resolution: window.devicePixelRatio || 1,
            autoDensity: true,
        });

        canvasContainer.appendChild(app.canvas as HTMLCanvasElement);

        app.stage.eventMode = "static";
        app.stage.hitArea = app.screen;

        viewportContainer = new Container();
        viewportContainer.eventMode = "static";
        app.stage.addChild(viewportContainer);

        setupControls();
    }

    function setupControls() {
        if (!app || !viewportContainer) return;

        window.addEventListener("keydown", handleKeydown);

        app.stage.on("pointerdown", (event) => {
            if (event.button === 1 || (event.button === 0 && event.shiftKey)) {
                isDragging = true;
                lastPointerPosition = { x: event.global.x, y: event.global.y };
                app.canvas.style.cursor = "grabbing";
            }
        });

        app.stage.on("pointermove", (event) => {
            if (isDragging && viewportContainer) {
                const dx = event.global.x - lastPointerPosition.x;
                const dy = event.global.y - lastPointerPosition.y;

                viewportContainer.x += dx;
                viewportContainer.y += dy;

                lastPointerPosition = { x: event.global.x, y: event.global.y };
            }
        });

        app.stage.on("pointerup", () => {
            isDragging = false;
            app.canvas.style.cursor = "default";
        });

        app.stage.on("pointerupoutside", () => {
            isDragging = false;
            app.canvas.style.cursor = "default";
        });

        app.canvas.addEventListener("wheel", handleWheel, { passive: false });
    }

    function handleKeydown(event: KeyboardEvent) {
        if (!viewportContainer) return;

        switch(event.key) {
            case "=":
            case "+":
                zoomIn();
                event.preventDefault();
                break;
            case "-":
            case "_":
                zoomOut();
                event.preventDefault();
                break;
            case "0":
                if (event.ctrlKey || event.metaKey) {
                    resetView();
                    event.preventDefault();
                }
                break;
            case "ArrowLeft":
                viewportContainer!.x += 20;
                event.preventDefault();
                break;
            case "ArrowRight":
                viewportContainer!.x -= 20;
                event.preventDefault();
                break;
            case "ArrowUp":
                viewportContainer!.y += 20;
                event.preventDefault();
                break;
            case "ArrowDown":
                viewportContainer!.y -= 20;
                event.preventDefault();
                break;
        }
    }

    function handleWheel(event: WheelEvent) {
        if (!viewportContainer || !app) return;

        event.preventDefault();

        const delta = event.deltaY < 0 ? 1.05 : 0.95;
        const newScale = viewportContainer!.scale.x * delta;

        if (newScale >= minScale && newScale <= maxScale) {
            const worldPos = {
                x: (event.offsetX - viewportContainer!.x) / viewportContainer!.scale.x,
                y: (event.offsetY - viewportContainer!.y) / viewportContainer!.scale.y,
            };

            viewportContainer!.scale.x = newScale;
            viewportContainer!.scale.y = newScale;

            viewportContainer!.x = event.offsetX - worldPos.x * newScale;
            viewportContainer!.y = event.offsetY - worldPos.y * newScale;
        }
    }

    function zoomIn() {
        if (!viewportContainer || !app) return;

        const newScale = Math.min(viewportContainer!.scale.x * 1.1, maxScale);
        const center = { x: app.screen.width / 2, y: app.screen.height / 2 };

        const worldPos = {
            x: (center.x - viewportContainer!.x) / viewportContainer!.scale.x,
            y: (center.y - viewportContainer!.y) / viewportContainer!.scale.y,
        };

        viewportContainer!.scale.x = newScale;
        viewportContainer!.scale.y = newScale;

        viewportContainer!.x = center.x - worldPos.x * newScale;
        viewportContainer!.y = center.y - worldPos.y * newScale;
    }

    function zoomOut() {
        if (!viewportContainer || !app) return;

        const newScale = Math.max(viewportContainer!.scale.x * 0.9, minScale);
        const center = { x: app.screen.width / 2, y: app.screen.height / 2 };

        const worldPos = {
            x: (center.x - viewportContainer!.x) / viewportContainer!.scale.x,
            y: (center.y - viewportContainer!.y) / viewportContainer!.scale.y,
        };

        viewportContainer!.scale.x = newScale;
        viewportContainer!.scale.y = newScale;

        viewportContainer!.x = center.x - worldPos.x * newScale;
        viewportContainer!.y = center.y - worldPos.y * newScale;
    }

    function resetView() {
        if (!viewportContainer) return;

        viewportContainer!.scale.x = initialScale;
        viewportContainer!.scale.y = initialScale;
        viewportContainer!.x = initialPosition.x;
        viewportContainer!.y = initialPosition.y;
    }

    async function renderAnnotations() {
        if (!app || !value || !viewportContainer) return;

        viewportContainer!.removeChildren();
        polygonGraphics.clear();
        polygonTexts.forEach((text) => text.destroy());
        polygonTexts.clear();

        textContainer = new Container();
        textContainer.zIndex = 1000;
        viewportContainer!.sortableChildren = true;
        viewportContainer!.addChild(textContainer);

        if (value.image) {
            let imageUrl = "";

            if (typeof value.image === "string") {
                imageUrl = value.image;
            } else if (value.image.url) {
                imageUrl = value.image.url;
            } else if (value.image.path) {
                if (root && !value.image.path.startsWith("http")) {
                    imageUrl = `${root}/file=${value.image.path}`;
                } else {
                    imageUrl = value.image.path;
                }
            }

            if (imageUrl) {
                try {
                    const img = new Image();
                    img.crossOrigin = "anonymous";

                    const imageLoadPromise = new Promise<HTMLImageElement>(
                        (resolve, reject) => {
                            img.onload = () => resolve(img);
                            img.onerror = reject;
                            img.src = imageUrl;
                        },
                    );

                    const loadedImage = await imageLoadPromise;
                    const texture = Texture.from(loadedImage);
                    imageSprite = new Sprite(texture);

                    const scaleX = app.screen.width / texture.width;
                    const scaleY = app.screen.height / texture.height;
                    const scale = Math.min(scaleX, scaleY);

                    imageSprite.scale.set(scale);

                    const displayWidth = texture.width * scale;
                    const displayHeight = texture.height * scale;

                    imageSprite.x = (app.screen.width - displayWidth) / 2;
                    imageSprite.y = (app.screen.height - displayHeight) / 2;

                    imageRect = {
                        left: imageSprite.x,
                        top: imageSprite.y,
                        right: imageSprite.x + displayWidth,
                        bottom: imageSprite.y + displayHeight,
                        width: displayWidth,
                        height: displayHeight,
                        naturalWidth: texture.width,
                        naturalHeight: texture.height,
                    };

                    viewportContainer!.addChild(imageSprite);

                    initialScale = 1;
                    initialPosition.x = 0;
                    initialPosition.y = 0;
                    viewportContainer!.scale.x = 1;
                    viewportContainer!.scale.y = 1;
                    viewportContainer!.x = 0;
                    viewportContainer!.y = 0;
                } catch (error) {
                    return;
                }
            }
        }

        if (value.polygons && value.polygons.length > 0 && imageSprite) {
            value.polygons.forEach((polygon) => {
                const graphics = new Graphics();

                let color = 0xff0000;
                try {
                    if (polygon.color) {
                        const colorStr = polygon.color.replace("#", "");
                        color = parseInt(colorStr, 16);
                    }
                } catch (e) {
                    color = 0xff0000;
                }

                const polygonMaskOpacity = polygon.mask_opacity ?? 0.2;
                const selectedMaskAlpha = polygon.selected_mask_opacity ?? 0.5;
                const polygonStrokeOpacity = polygon.stroke_opacity ?? 0.6;
                const selectedStrokeAlpha =
                    polygon.selected_stroke_opacity ?? 1.0;
                const strokeWidth = polygon.stroke_width ?? 0.7;
                const initialMaskAlpha = selectedPolygonIds.includes(polygon.id)
                    ? selectedMaskAlpha
                    : polygonMaskOpacity;
                const initialStrokeAlpha = selectedPolygonIds.includes(
                    polygon.id,
                )
                    ? selectedStrokeAlpha
                    : polygonStrokeOpacity;

                if (polygon.coordinates && polygon.coordinates.length > 0) {
                    drawPolygonPath(
                        graphics,
                        polygon,
                        initialMaskAlpha,
                        strokeWidth,
                        initialStrokeAlpha,
                    );
                }

                graphics.eventMode = "static";
                graphics.cursor = "pointer";

                const originalMaskAlpha = polygonMaskOpacity;
                const hoverMaskAlpha = Math.min(polygonMaskOpacity + 0.1, 1.0);
                const hoverStrokeAlpha = Math.min(
                    polygonStrokeOpacity + 0.2,
                    1.0,
                );

                graphics.on("pointerover", () => {
                    if (!selectedPolygonIds.includes(polygon.id)) {
                        graphics.clear();
                        drawPolygonPath(
                            graphics,
                            polygon,
                            hoverMaskAlpha,
                            strokeWidth,
                            hoverStrokeAlpha,
                        );
                    }
                });

                graphics.on("pointerout", () => {
                    if (!selectedPolygonIds.includes(polygon.id)) {
                        graphics.clear();
                        drawPolygonPath(
                            graphics,
                            polygon,
                            originalMaskAlpha,
                            strokeWidth,
                            polygonStrokeOpacity,
                        );
                    }
                });

                graphics.on("pointerdown", (event) => {
                    handlePolygonSelection(polygon.id, event);
                });

                viewportContainer!.addChild(graphics);
                polygonGraphics.set(polygon.id, graphics);

                if (polygon.display_text && polygon.display_font_size && polygon.display_font_size > 0) {
                    const text = createPolygonText(polygon);
                    const center = calculatePolygonCenter(polygon.coordinates);

                    text.anchor.set(0.5, 0.5);
                    text.x = center.x;
                    text.y = center.y;

                    text.eventMode = "static";
                    text.cursor = "pointer";

                    text.on("pointerdown", (event) => {
                        handlePolygonSelection(polygon.id, event);
                    });

                    textContainer!.addChild(text);
                    polygonTexts.set(polygon.id, text);
                }
            });
        }
    }

    function createPolygonText(polygon: any): Text {
        const style = new TextStyle({
            fontSize: polygon.display_font_size || 14,
            fill: polygon.display_text_color || "#000000",
            fontWeight: "bold",
            align: "center"
        });

        return new Text({
            text: polygon.display_text,
            style: style
        });
    }

    function calculatePolygonCenter(coordinates: number[][]): { x: number; y: number } {
        const displayCoords = coordinates.map((coord) => [
            (coord[0] / (imageRect.naturalWidth - 1)) * imageRect.width + imageRect.left,
            (coord[1] / (imageRect.naturalHeight - 1)) * imageRect.height + imageRect.top,
        ]);

        let centerX = 0;
        let centerY = 0;
        displayCoords.forEach((coord) => {
            centerX += coord[0];
            centerY += coord[1];
        });

        return {
            x: centerX / displayCoords.length,
            y: centerY / displayCoords.length
        };
    }

    function drawPolygonPath(
        graphics: Graphics,
        polygon: any,
        maskAlpha: number = 0.2,
        strokeWidth: number = 0.7,
        strokeAlpha: number = 0.6,
    ) {
        if (polygon.coordinates && polygon.coordinates.length > 0) {
            const displayCoords = polygon.coordinates.map((coord: number[]) => {
                return [
                    (coord[0] / (imageRect.naturalWidth - 1)) *
                        imageRect.width +
                        imageRect.left,
                    (coord[1] / (imageRect.naturalHeight - 1)) *
                        imageRect.height +
                        imageRect.top,
                ];
            });

            let color = 0xff0000;
            try {
                if (polygon.color) {
                    const colorStr = polygon.color.replace("#", "");
                    color = parseInt(colorStr, 16);
                }
            } catch (e) {
                color = 0xff0000;
            }

            graphics.poly(displayCoords.flat());
            graphics.fill({ color: color, alpha: maskAlpha });
            graphics.stroke({
                width: strokeWidth,
                color: color,
                alpha: strokeAlpha,
            });
        }
    }

    onMount(async () => {
        await tick();
        await initPixiApp();
        if (value) {
            await renderAnnotations();
        }
    });

    onDestroy(() => {
        if (app) {
            app.canvas.removeEventListener("wheel", handleWheel);
            window.removeEventListener("keydown", handleKeydown);
            app.destroy(true, { children: true, texture: true });
        }
    });

    async function handleResize() {
        if (!canvasContainer || !app) return;

        const newWidth = canvasContainer.clientWidth;
        const newHeight = canvasContainer.clientHeight;

        if (newWidth !== app.screen.width || newHeight !== app.screen.height) {
            app.renderer.resize(newWidth, newHeight);
            await renderAnnotations();
        }
    }

    $: if (canvasContainer) {
        handleResize();
    }

    $: (value, gradio.dispatch("change"));
</script>

<Block
    {visible}
    variant={"solid"}
    padding={false}
    {elem_id}
    {elem_classes}
    allow_overflow={false}
    {container}
    {scale}
    {min_width}
    {height}
    {width}
>
    <StatusTracker
        autoscroll={gradio.autoscroll}
        i18n={gradio.i18n}
        {...loading_status}
        on:clear_status={() => gradio.dispatch("clear_status", loading_status)}
    />

    <BlockLabel
        {show_label}
        Icon={ImageIcon}
        label={label || "Image Annotations"}
    />

    <div class="container">
        <div class="canvas-container" bind:this={canvasContainer} />
    </div>
</Block>

<style>
    .container {
        display: flex;
        position: relative;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 100%;
    }

    .canvas-container {
        position: relative;
        width: 100%;
        height: 100%;
        min-height: 400px;
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #f0f0f0;
    }

    :global(.canvas-container canvas) {
        display: block;
        width: 100%;
        height: 100%;
        object-fit: contain;
    }
</style>
