<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import * as pdfjs from 'pdfjs-dist';

	pdfjs.GlobalWorkerOptions.workerSrc =
		'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.5.141/pdf.worker.min.js';

	export let url = '';
	let canvasContainer: HTMLDivElement;

	async function renderPage(page: pdfjs.PDFPageProxy) {
		const viewport = page.getViewport({ scale: 1.0 });

		const wrapper = document.createElement('div');
		wrapper.style.marginBottom = '16px';
		wrapper.style.position = 'relative';
		wrapper.style.width = '100%';
		wrapper.style.maxWidth = '100%';
		wrapper.id = `page-${page._pageIndex + 1}`;
		
		const canvas = document.createElement('canvas');
		const ctx = canvas.getContext('2d');

		if (!ctx) {
			return;
		}

		// Calculate scale to fit container width
		const containerWidth = canvasContainer.clientWidth - 32; // Account for padding
		const scale = Math.min(1.2, containerWidth / viewport.width);
		const scaledViewport = page.getViewport({ scale });

		canvas.height = scaledViewport.height;
		canvas.width = scaledViewport.width;
		canvas.style.width = '100%';
		canvas.style.height = 'auto';
		canvas.style.maxWidth = '100%';
		
		wrapper.appendChild(canvas);
		canvasContainer.appendChild(wrapper);

		page.render({
			canvasContext: ctx,
			viewport: scaledViewport
		});

		const textLayer = document.createElement('div');
		textLayer.className = 'textLayer';
		textLayer.style.width = '100%';
		textLayer.style.height = scaledViewport.height + 'px';
		const textContent = await page.getTextContent();
		pdfjs.renderTextLayer({
			textContentSource: textContent,
			viewport: scaledViewport,
			container: textLayer
		});

		wrapper.appendChild(textLayer);
	}

	let destroyed = false;
	onMount(async () => {
		const pdfDoc = await pdfjs.getDocument(url).promise;

		if (destroyed) {
			return;
		}

		for (let num = 1; num <= pdfDoc.numPages; num++) {
			pdfDoc.getPage(num).then(renderPage);
		}
	});

	onDestroy(() => {
		destroyed = true;
	});
</script>

<div class="pdf-container">
	<div bind:this={canvasContainer} class="pdf-wrapper" style="--scale-factor: 1.2" />
</div>

<style>
	.pdf-container {
		height: 100%;
		overflow: hidden;
		background: #f8fafc;
		border-radius: 0.5rem;
	}
	.pdf-wrapper {
		height: 100%;
		background: #f1f5f9;
		padding: 1rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		overflow-y: auto;
		overflow-x: hidden;
	}
	
	:global(.dark) .pdf-container {
		background: #0f172a;
	}
	
	:global(.dark) .pdf-wrapper {
		background: #1e293b;
	}
	
	.pdf-wrapper::-webkit-scrollbar {
		width: 8px;
	}
	
	.pdf-wrapper::-webkit-scrollbar-track {
		background: transparent;
	}
	
	.pdf-wrapper::-webkit-scrollbar-thumb {
		background-color: rgba(0, 0, 0, 0.2);
		border-radius: 4px;
	}
	
	.pdf-wrapper::-webkit-scrollbar-thumb:hover {
		background-color: rgba(0, 0, 0, 0.3);
	}
	
	:global(.dark) .pdf-wrapper::-webkit-scrollbar-thumb {
		background-color: rgba(255, 255, 255, 0.2);
	}
	
	:global(.dark) .pdf-wrapper::-webkit-scrollbar-thumb:hover {
		background-color: rgba(255, 255, 255, 0.3);
	}
</style>
