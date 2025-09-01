<script lang="ts">
	import { onMount } from 'svelte';
	import {
		store,
		resetError,
		fetchConversations,
		createConversation,
		getActiveConversation
	} from '$s/chat';
	import Alert from '$c/Alert.svelte';
	import ChatInput from '$c/chat/ChatInput.svelte';
	import ChatList from '$c/chat/ChatList.svelte';
	import ConversationSelect from '$c/chat/ConversationSelect.svelte';

	export let onSubmit: (text: string, useStreaming: boolean) => void;
	export let documentId: number;
	export let documentName: string = '';
	export let isPdfCollapsed: boolean = false;
	export let togglePdfPanel: () => void;
	export let toggleMobilePdf: () => void;

	let useStreaming = !!localStorage.getItem('streaming');

	$: localStorage.setItem('streaming', useStreaming ? 'true' : '');
	$: activeConversation = $store.activeConversationId ? getActiveConversation() : null;

	function handleSubmit(event: CustomEvent<string>) {
		if (onSubmit) {
			onSubmit(event.detail, useStreaming);
		}
	}

	function handleNewChat() {
		createConversation(documentId);
	}

	// Truncate filename for display
	function truncateFilename(filename: string, maxLength: number = 25): string {
		if (filename.length <= maxLength) return filename;
		
		const extension = filename.split('.').pop();
		const nameWithoutExt = filename.substring(0, filename.lastIndexOf('.'));
		
		if (extension) {
			const maxNameLength = maxLength - extension.length - 4;
			return nameWithoutExt.substring(0, maxNameLength) + '...' + '.' + extension;
		}
		
		return filename.substring(0, maxLength - 3) + '...';
	}

	onMount(() => {
		fetchConversations(documentId);
	});
</script>

<div
	style="height: calc(100vh - 120px);"
	class="flex flex-col h-full bg-white dark:bg-slate-800 md:border-r border-slate-200 dark:border-slate-700"
>
	<!-- Chat Header -->
	<div class="border-b border-slate-200 dark:border-slate-700 px-4 py-3 bg-white dark:bg-slate-800">
		<div class="flex items-center justify-between">
			<div class="flex items-center gap-2 min-w-0 flex-1">
				<p class="text-base font-semibold text-slate-900 dark:text-white truncate" title={documentName}>
					{truncateFilename(documentName, 20)}
				</p>
			</div>
			<div class="flex items-center gap-2 flex-shrink-0">
				<div class="relative hidden sm:block">
					<ConversationSelect conversations={$store.conversations} />
				</div>
				<button 
					class="text-sm bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-lg font-medium transition-colors whitespace-nowrap" 
					on:click={handleNewChat}
				>
					<span class="hidden sm:inline">New Chat</span>
					<span class="sm:hidden">New</span>
				</button>
				
				<!-- Mobile PDF Button -->
				<button 
					on:click={toggleMobilePdf}
					class="md:hidden p-2 text-slate-600 dark:text-slate-400 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-colors flex-shrink-0"
					title="View PDF"
				>
					<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
					</svg>
				</button>
				
				<!-- Desktop Collapse/Expand Button -->
				<button 
					on:click={togglePdfPanel}
					class="hidden md:block p-2 text-slate-600 dark:text-slate-400 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-colors flex-shrink-0"
					title={isPdfCollapsed ? "Show PDF" : "Hide PDF"}
				>
					{#if isPdfCollapsed}
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
						</svg>
					{:else}
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19l7-7-7-7"/>
						</svg>
					{/if}
				</button>
			</div>
		</div>
		
		<!-- Mobile History Dropdown -->
		<div class="sm:hidden mt-2">
			<ConversationSelect conversations={$store.conversations} />
		</div>
	</div>

	<!-- Chat Messages -->
	<div class="flex-1 overflow-y-auto px-3 py-3 bg-slate-50 dark:bg-slate-900">
		<ChatList messages={activeConversation?.messages || []} />
		
		{#if $store.error && $store.error.length < 200}
			<div class="mb-3">
				<Alert type="error" onDismiss={resetError}>
					{$store.error}
				</Alert>
			</div>
		{/if}
	</div>

	<!-- Chat Input -->
	<div class="border-t border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-3">
		<ChatInput on:submit={handleSubmit} />
	</div>
</div>
