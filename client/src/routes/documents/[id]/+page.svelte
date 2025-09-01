<script lang="ts">
	import type { PageData } from './$types';
	import { beforeNavigate } from '$app/navigation';
	import { resetAll, sendMessage } from '$s/chat/index';
	import PdfViewer from '$c/PdfViewer.svelte';
	import ChatPanel from '$c/chat/ChatPanel.svelte';

	export let data: PageData;

	const document = data.document;
	const documentUrl = data.documentUrl;

	// PDF panel state
	let isPdfCollapsed = false;
	let showPdfOnMobile = false;
	let isPdfFullscreen = false;

	function handleSubmit(content: string, useStreaming: boolean) {
		sendMessage({ role: 'user', content }, { useStreaming, documentId: document.id });
	}

	function togglePdfPanel() {
		if (isPdfFullscreen) {
			isPdfFullscreen = false;
		}
		isPdfCollapsed = !isPdfCollapsed;
	}

	function toggleMobilePdf() {
		showPdfOnMobile = !showPdfOnMobile;
	}

	function togglePdfFullscreen() {
		isPdfFullscreen = !isPdfFullscreen;
		if (isPdfFullscreen) {
			isPdfCollapsed = false;
		}
	}

	// Truncate filename for display
	function truncateFilename(filename: string, maxLength: number = 30): string {
		if (filename.length <= maxLength) return filename;
		
		const extension = filename.split('.').pop();
		const nameWithoutExt = filename.substring(0, filename.lastIndexOf('.'));
		
		if (extension) {
			const maxNameLength = maxLength - extension.length - 4;
			return nameWithoutExt.substring(0, maxNameLength) + '...' + '.' + extension;
		}
		
		return filename.substring(0, maxLength - 3) + '...';
	}

	beforeNavigate(resetAll);
</script>

{#if data.error}
	<div class="p-4 bg-red-100 border border-red-400 text-red-700 rounded">
		Error: {data.error}
	</div>
{/if}

{#if document}
	<div class="chat-container h-full flex relative bg-slate-900 overflow-hidden gap-0 md:gap-2" style="height: calc(100vh - 120px);">
		<!-- Chat Panel - Full width on mobile, responsive on desktop -->
		<div class="chat-panel transition-all duration-300 ease-in-out border border-slate-700 rounded-lg overflow-hidden w-full {isPdfFullscreen ? 'md:w-0 md:opacity-0 md:min-w-0' : (isPdfCollapsed ? 'md:w-full' : 'md:w-2/5')}">
			{#if !isPdfFullscreen}
				<ChatPanel 
					documentId={document.id} 
					documentName={document.name} 
					onSubmit={handleSubmit}
					{isPdfCollapsed}
					{togglePdfPanel}
					{toggleMobilePdf}
				/>
			{/if}
		</div>

		<!-- Desktop PDF Panel - Hidden on mobile, visible on desktop -->
		<div class="hidden md:flex pdf-panel transition-all duration-300 ease-in-out bg-slate-800 border border-slate-700 rounded-lg overflow-hidden {isPdfCollapsed ? 'w-0 opacity-0 min-w-0' : (isPdfFullscreen ? 'w-full' : 'w-3/5')}">
			{#if !isPdfCollapsed}
				<div class="h-full flex flex-col w-full">
					<!-- PDF Header -->
					<div class="flex items-center justify-between p-2.5 bg-slate-700 border-b border-slate-600">
						<div class="flex items-center gap-2 min-w-0">
							<svg class="w-3.5 h-3.5 text-red-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
							</svg>
							<h3 class="text-white font-medium text-xs truncate" title={document.name}>
								{truncateFilename(document.name, 40)}
							</h3>
						</div>
						<div class="flex items-center gap-1.5">
							<!-- Fullscreen Toggle -->
							<button 
								on:click={togglePdfFullscreen}
								class="p-1 text-slate-400 hover:text-white hover:bg-slate-600 rounded transition-colors"
								title={isPdfFullscreen ? "Exit Fullscreen" : "Fullscreen"}
							>
								{#if isPdfFullscreen}
									<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
									</svg>
								{:else}
									<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"/>
									</svg>
								{/if}
							</button>
							
							<!-- Close PDF Button -->
							{#if !isPdfFullscreen}
								<button 
									on:click={togglePdfPanel}
									class="p-1 text-slate-400 hover:text-white hover:bg-slate-600 rounded transition-colors"
									title="Close PDF"
								>
									<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
									</svg>
								</button>
							{/if}
						</div>
					</div>
					<!-- PDF Content -->
					<div class="flex-1 overflow-hidden bg-gray-100">
						<PdfViewer url={documentUrl} />
					</div>
				</div>
			{/if}
		</div>

		<!-- Mobile PDF Overlay -->
		{#if showPdfOnMobile}
			<div class="md:hidden fixed inset-0 z-50 bg-black bg-opacity-50" on:click={toggleMobilePdf}>
				<div class="bg-white h-full w-full flex flex-col" on:click|stopPropagation>
					<!-- Mobile PDF Header -->
					<div class="flex items-center justify-between p-3 bg-slate-700 text-white border-b border-slate-600 flex-shrink-0">
						<div class="flex items-center gap-2 min-w-0">
							<svg class="w-4 h-4 text-red-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
							</svg>
							<h3 class="font-medium text-sm truncate" title={document.name}>
								{truncateFilename(document.name, 30)}
							</h3>
						</div>
						<button 
							on:click={toggleMobilePdf} 
							class="p-1.5 text-slate-300 hover:text-white hover:bg-slate-600 rounded transition-colors"
							title="Close PDF"
						>
							<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
							</svg>
						</button>
					</div>
					<!-- Mobile PDF Content -->
					<div class="flex-1 overflow-hidden bg-gray-100">
						<PdfViewer url={documentUrl} />
					</div>
				</div>
			</div>
		{/if}
	</div>
{/if}
