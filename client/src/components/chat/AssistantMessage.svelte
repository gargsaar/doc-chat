<script lang="ts">
	import { marked } from 'marked';
	import classnames from 'classnames';
	import { scoreConversation } from '$s/chat';
	import Icon from '$c/Icon.svelte';

	export let content = '';
	let score = 0;

	const klass = 'border rounded-full inline-block cursor-pointer hover:bg-slate-100 dark:hover:bg-slate-600 transition-colors text-slate-600 dark:text-slate-300';
	$: upKlass = classnames(klass, {
		'bg-green-100 dark:bg-green-900 border-green-300 dark:border-green-700 text-green-600 dark:text-green-400': score === 1
	});
	$: downKlass = classnames(klass, {
		'bg-red-100 dark:bg-red-900 border-red-300 dark:border-red-700 text-red-600 dark:text-red-400': score === -1
	});

	async function applyScore(_score: number) {
		if (score !== 0) {
			return;
		}
		score = _score;
		return scoreConversation(_score);
	}
</script>

<div class="flex flex-col mb-3">
	<!-- Message Only -->
	<div class="flex items-start">
		<div class="message bg-white dark:bg-slate-700 text-slate-900 dark:text-slate-100 border border-slate-200 dark:border-slate-600 rounded-2xl rounded-bl-md px-3 py-2.5 max-w-xs lg:max-w-md shadow-sm text-sm">
			{@html marked(content, { breaks: true, gfm: true })}
		</div>
	</div>
	
	<!-- Rating Buttons -->
	<div class="flex items-center gap-1.5 mt-1.5">
		{#if score >= 0}
			<button class={upKlass} style="line-height: 12px; padding: 5px;" on:click={() => applyScore(1)} title="Good response">
				<Icon name="thumb_up" outlined />
			</button>
		{/if}
		{#if score <= 0}
			<button class={downKlass} style="line-height: 12px; padding: 5px;" on:click={() => applyScore(-1)} title="Poor response">
				<Icon name="thumb_down" outlined />
			</button>
		{/if}
	</div>
</div>

<style>
	.message :global(p) {
		margin: 0;
		line-height: 1.5;
		color: rgb(248 250 252) !important; /* Always white text */
		font-size: 0.875rem; /* 14px */
	}
	
	.message :global(*) {
		color: rgb(248 250 252) !important; /* Force all text to white */
	}
	
	.message :global(p + p) {
		margin-top: 0.5rem;
	}
	
	.message :global(code) {
		background-color: rgb(241 245 249); /* slate-100 */
		color: rgb(71 85 105); /* slate-600 */
		padding: 0.125rem 0.3rem;
		border-radius: 0.25rem;
		font-size: 0.8rem;
		font-family: ui-monospace, SFMono-Regular, 'SF Mono', Consolas, 'Liberation Mono', Menlo, monospace;
	}
	
	:global(.dark) .message :global(code) {
		background-color: rgb(51 65 85); /* slate-700 */
		color: rgb(203 213 225); /* slate-300 */
	}
	
	.message :global(pre) {
		background-color: rgb(248 250 252); /* slate-50 */
		color: rgb(15 23 42); /* slate-900 */
		padding: 0.75rem;
		border-radius: 0.5rem;
		overflow-x: auto;
		margin: 0.5rem 0;
		border: 1px solid rgb(226 232 240); /* slate-200 */
		font-size: 0.8rem;
	}
	
	:global(.dark) .message :global(pre) {
		background-color: rgb(30 41 59); /* slate-800 */
		color: rgb(248 250 252); /* slate-50 */
		border-color: rgb(71 85 105); /* slate-600 */
	}
	
	.message :global(ul), .message :global(ol) {
		margin: 0.5rem 0;
		padding-left: 1.125rem;
		color: rgb(15 23 42); /* slate-900 */
		font-size: 0.875rem;
	}
	
	:global(.dark) .message :global(ul), :global(.dark) .message :global(ol) {
		color: rgb(248 250 252); /* slate-50 */
	}
	
	.message :global(li) {
		margin: 0.25rem 0;
		line-height: 1.5;
	}
	
	.message :global(strong) {
		font-weight: 600;
		color: rgb(15 23 42); /* slate-900 */
	}
	
	:global(.dark) .message :global(strong) {
		color: rgb(248 250 252); /* slate-50 */
	}
	
	.message :global(em) {
		font-style: italic;
	}
	
	.message :global(blockquote) {
		border-left: 4px solid rgb(203 213 225); /* slate-300 */
		padding-left: 0.75rem;
		margin: 0.5rem 0;
		font-style: italic;
		color: rgb(71 85 105); /* slate-600 */
	}
	
	:global(.dark) .message :global(blockquote) {
		border-left-color: rgb(71 85 105); /* slate-600 */
		color: rgb(203 213 225); /* slate-300 */
	}
</style>
