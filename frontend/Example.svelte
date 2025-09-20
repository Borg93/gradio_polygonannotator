<script lang="ts">
	import type { FileData } from "@gradio/client";

	export let value: null | { image: FileData; polygons: Array<{id: string, coordinates: number[][], color: string}> };
	export let type: "gallery" | "table";
	export let selected = false;
	export const index: number = 0;
</script>

{#if value?.image}
	<div
		class="container"
		class:table={type === "table"}
		class:gallery={type === "gallery"}
		class:selected
	>
		<img src={value.image.url || value.image.path} alt="" />
		{#if value.polygons && value.polygons.length > 0}
			<div class="polygon-count">
				{value.polygons.length} polygon{value.polygons.length !== 1 ? 's' : ''}
			</div>
		{/if}
	</div>
{/if}

<style>
	.container :global(img) {
		width: 100%;
		height: 100%;
	}

	.container.selected {
		border-color: var(--border-color-accent);
	}

	.container.table {
		margin: 0 auto;
		border: 2px solid var(--border-color-primary);
		border-radius: var(--radius-lg);
		overflow: hidden;
		width: var(--size-20);
		height: var(--size-20);
		object-fit: cover;
	}

	.container.gallery {
		height: var(--size-20);
		max-height: var(--size-20);
		object-fit: cover;
	}
	.container img {
		object-fit: cover;
	}

	.polygon-count {
		position: absolute;
		bottom: 4px;
		right: 4px;
		background: rgba(0, 0, 0, 0.7);
		color: white;
		padding: 2px 6px;
		border-radius: 3px;
		font-size: 11px;
		font-weight: 500;
	}

	.container {
		position: relative;
	}
</style>
