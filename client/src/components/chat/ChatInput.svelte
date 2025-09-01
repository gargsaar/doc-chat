<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	let value = '';

	const dispatch = createEventDispatcher();
	function handleKeyDown(event: KeyboardEvent) {
		const isCombo = event.shiftKey || event.ctrlKey || event.altKey || event.metaKey;
		if (event.key !== 'Enter' || isCombo) {
			return;
		}

		if (event.key === 'Enter' && !isCombo && value.trim() === '') {
			event.preventDefault();
			return;
		}

		event.preventDefault();
		dispatch('submit', value.trim());
		value = '';
	}

	function handleSend() {
		if (value.trim()) {
			dispatch('submit', value.trim());
			value = '';
		}
	}

	$: height = Math.min((value.match(/\n/g)?.length || 0) * 20 + 40, 100);
</script>

<div class="flex items-end gap-2.5 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-600 rounded-xl px-3 py-2.5 shadow-sm">
	<textarea
		class="flex-1 resize-none bg-transparent border-0 outline-none placeholder-slate-400 dark:placeholder-slate-500 text-slate-900 dark:text-slate-100 text-sm leading-5"
		style:height={height + 'px'}
		bind:value
		on:keydown={handleKeyDown}
		placeholder="Ask a question about this document..."
		rows="1"
	></textarea>
	<button
		on:click={handleSend}
		disabled={!value.trim()}
		class="p-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 dark:disabled:bg-slate-600 disabled:cursor-not-allowed text-white rounded-lg transition-colors flex-shrink-0 self-end"
		title="Send message (Enter)"
	>
		<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
		</svg>
	</button>
</div>
