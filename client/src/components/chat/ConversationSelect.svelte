<script lang="ts">
	import type { Conversation } from '$s/chat';
	import { onMount } from 'svelte';
	import { setActiveConversationId } from '$s/chat';

	export let conversations: Conversation[] = [];
	let isOpen = false;

	async function handleClick(conversation: Conversation) {
		isOpen = false;

		setActiveConversationId(conversation.id);
	}

	onMount(() => {
		window.addEventListener('click', (e: any) => {
			if (e.target && !e.target.closest('.relative')) {
				isOpen = false;
			}
		});
	});
</script>

<div class="relative inline-block text-left">
	<div>
		<button
			on:click={() => (isOpen = !isOpen)}
			type="button"
			class="inline-flex items-center justify-center px-3 py-1.5 text-sm font-medium text-slate-600 dark:text-slate-300 bg-slate-100 dark:bg-slate-700 border border-slate-200 dark:border-slate-600 rounded-md hover:bg-slate-200 dark:hover:bg-slate-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
			id="options-menu"
			aria-haspopup="true"
			aria-expanded="true"
		>
			<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
			</svg>
			History
			<svg
				class="ml-1 h-4 w-4"
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 20 20"
				fill="currentColor"
				aria-hidden="true"
			>
				<path
					fill-rule="evenodd"
					d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
					clip-rule="evenodd"
				/>
			</svg>
		</button>
	</div>

	{#if isOpen}
		<div
			class="origin-top-right overflow-y-auto absolute right-0 mt-1.5 w-52 rounded-lg shadow-lg bg-white dark:bg-slate-700 ring-1 ring-black ring-opacity-5 dark:ring-slate-600 z-50"
			style="max-width: 280px; max-height: 220px;"
		>
			<div class="py-1" role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
				{#each conversations as conversation (conversation)}
					<button
						class="block w-full text-left px-3 py-2.5 text-sm text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-600 transition-colors border-b border-slate-100 dark:border-slate-600 last:border-b-0"
						on:click={() => handleClick(conversation)}
						role="menuitem"
					>
						<div class="font-medium">Chat {conversation.id}</div>
						<div class="text-xs text-slate-500 dark:text-slate-400 mt-1">
							{new Date(conversation.created_at || Date.now()).toLocaleDateString()}
						</div>
					</button>
				{/each}
				{#if conversations.length === 0}
					<div class="px-3 py-2.5 text-sm text-slate-500 dark:text-slate-400 text-center">
						No chat history yet
					</div>
				{/if}
			</div>
		</div>
	{/if}
</div>
