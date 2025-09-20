<svelte:options accessors={true} />

<script lang="ts">
    import { onMount, onDestroy, tick } from "svelte";
    import * as PIXI from "pixi.js";
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
    let app: PIXI.Application;
    let imageSprite: PIXI.Sprite | null = null;
    let polygonGraphics: Map<string, PIXI.Graphics> = new Map();
    let selectedPolygonIds: string[] = [];
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
                drawPolygonPath(graphics, polygon, imageSprite!, selectedMaskAlpha, strokeWidth, selectedStrokeAlpha);
            } else {
                drawPolygonPath(graphics, polygon, imageSprite!, originalMaskAlpha, strokeWidth, originalStrokeAlpha);
            }
        });
    }

    async function initPixiApp() {
        if (!canvasContainer) return;

        const containerWidth = canvasContainer.clientWidth || 800;
        const containerHeight = canvasContainer.clientHeight || 600;

        app = new PIXI.Application();
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
    }

    async function renderAnnotations() {
        if (!app || !value) return;

        app.stage.removeChildren();
        polygonGraphics.clear();
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
                    const texture = PIXI.Texture.from(loadedImage);
                    imageSprite = new PIXI.Sprite(texture);

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

                    app.stage.addChild(imageSprite);
                } catch (error) {
                    console.error("Failed to load image:", error);
                    return;
                }
            }
        }

        if (value.polygons && value.polygons.length > 0 && imageSprite) {
            value.polygons.forEach((polygon) => {
                const graphics = new PIXI.Graphics();

                let color = 0xff0000;
                try {
                    if (polygon.color) {
                        const colorStr = polygon.color.replace("#", "");
                        color = parseInt(colorStr, 16);
                    }
                } catch (e) {
                    console.error("Error parsing color:", e);
                }

                const polygonMaskOpacity = polygon.mask_opacity ?? 0.2;
                const selectedMaskAlpha = polygon.selected_mask_opacity ?? 0.5;
                const polygonStrokeOpacity = polygon.stroke_opacity ?? 0.6;
                const selectedStrokeAlpha = polygon.selected_stroke_opacity ?? 1.0;
                const strokeWidth = polygon.stroke_width ?? 0.7;
                const initialMaskAlpha = selectedPolygonIds.includes(polygon.id)
                    ? selectedMaskAlpha
                    : polygonMaskOpacity;
                const initialStrokeAlpha = selectedPolygonIds.includes(polygon.id)
                    ? selectedStrokeAlpha
                    : polygonStrokeOpacity;

                if (polygon.coordinates && polygon.coordinates.length > 0) {
                    const displayCoords = polygon.coordinates.map((coord) => {
                        return [
                            (coord[0] / (imageRect.naturalWidth - 1)) *
                                imageRect.width +
                                imageRect.left,
                            (coord[1] / (imageRect.naturalHeight - 1)) *
                                imageRect.height +
                                imageRect.top,
                        ];
                    });

                    graphics.poly(displayCoords.flat());
                    graphics.fill({ color: color, alpha: initialMaskAlpha });
                    graphics.stroke({ width: strokeWidth, color: color, alpha: initialStrokeAlpha });
                }

                graphics.eventMode = "static";
                graphics.cursor = "pointer";

                const originalMaskAlpha = polygonMaskOpacity;
                const hoverMaskAlpha = Math.min(polygonMaskOpacity + 0.1, 1.0);
                const hoverStrokeAlpha = Math.min(polygonStrokeOpacity + 0.2, 1.0);

                graphics.on("pointerover", () => {
                    if (!selectedPolygonIds.includes(polygon.id)) {
                        graphics.clear();
                        drawPolygonPath(
                            graphics,
                            polygon,
                            imageSprite!,
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
                            imageSprite!,
                            originalMaskAlpha,
                            strokeWidth,
                            polygonStrokeOpacity,
                        );
                    }
                });

                graphics.on("pointerdown", (event) => {
                    // Check if Ctrl/Cmd key is held for multi-selection
                    const isMultiSelect = event.ctrlKey || event.metaKey;

                    if (selectedPolygonIds.includes(polygon.id)) {
                        // Deselect this polygon
                        const newSelectedIds = selectedPolygonIds.filter(
                            (id) => id !== polygon.id,
                        );
                        updateSelection(newSelectedIds);
                        selectedPolygonIds = newSelectedIds;

                        // Dispatch deselection event to Gradio
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

                    // Select polygon
                    let newSelectedIds: string[];
                    if (isMultiSelect) {
                        // Add to existing selection
                        newSelectedIds = [...selectedPolygonIds, polygon.id];
                    } else {
                        // Replace selection
                        newSelectedIds = [polygon.id];
                    }

                    updateSelection(newSelectedIds);
                    selectedPolygonIds = newSelectedIds;

                    // Dispatch select event to Gradio
                    gradio.dispatch("select", {
                        index: value.polygons.findIndex(
                            (p) => p.id === polygon.id,
                        ),
                        value: newSelectedIds,
                    });
                });

                app.stage.addChild(graphics);
                polygonGraphics.set(polygon.id, graphics);
            });
        }
    }

    function drawPolygonPath(
        graphics: PIXI.Graphics,
        polygon: any,
        imageSprite: PIXI.Sprite,
        maskAlpha: number = 0.2,
        strokeWidth: number = 0.7,
        strokeAlpha: number = 0.6,
    ) {
        if (polygon.coordinates && polygon.coordinates.length > 0) {
            // Transform coordinates from natural image space to display space
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
                console.error("Error parsing color in drawPolygonPath:", e);
            }

            // Use Pixi.js 8 drawing API
            graphics.poly(displayCoords.flat());
            graphics.fill({ color: color, alpha: maskAlpha });
            graphics.stroke({ width: strokeWidth, color: color, alpha: strokeAlpha });
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
            app.destroy(true, { children: true, texture: true });
        }
    });

    // Handle canvas resize
    async function handleResize() {
        if (!canvasContainer || !app) return;

        const newWidth = canvasContainer.clientWidth;
        const newHeight = canvasContainer.clientHeight;

        if (newWidth !== app.screen.width || newHeight !== app.screen.height) {
            app.renderer.resize(newWidth, newHeight);
            // Re-render annotations with updated canvas dimensions
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
