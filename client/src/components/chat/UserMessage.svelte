<script lang="ts">
	import { marked } from 'marked';

	export let content = '';
</script>

<div class="flex justify-end mb-3">
	<div class="message bg-blue-600 text-white rounded-2xl rounded-br-md px-3 py-2.5 max-w-xs lg:max-w-md shadow-sm text-sm">
		{@html marked(content, { breaks: true, gfm: true })}
	</div>
</div>

<style>
	.message :global(p) {
		margin: 0;
		line-height: 1.5;
		font-size: 0.875rem; /* 14px */
	}
	
	.message :global(p + p) {
		margin-top: 0.5rem;
	}
	
	.message :global(code) {
		background-color: rgba(255, 255, 255, 0.2);
		padding: 0.125rem 0.3rem;
		border-radius: 0.25rem;
		font-size: 0.8rem;
		font-family: ui-monospace, SFMono-Regular, 'SF Mono', Consolas, 'Liberation Mono', Menlo, monospace;
	}
	
	.message :global(pre) {
		background-color: rgba(255, 255, 255, 0.1);
		padding: 0.5rem;
		border-radius: 0.375rem;
		overflow-x: auto;
		margin: 0.375rem 0;
		font-size: 0.8rem;
		font-family: ui-monospace, SFMono-Regular, 'SF Mono', Consolas, 'Liberation Mono', Menlo, monospace;
	}
	
	.message :global(ul), .message :global(ol) {
		margin: 0.375rem 0;
		padding-left: 1.125rem;
		font-size: 0.875rem;
	}
	
	.message :global(li) {
		margin: 0.125rem 0;
	}
</style>
