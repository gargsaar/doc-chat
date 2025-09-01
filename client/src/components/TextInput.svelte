<script lang="ts">
	export let type: string = 'text';
	export let value = '';
	export let placeholder = '';

	function typeAction(node: HTMLInputElement) {
		node.type = type;
	}
</script>

<input
	use:typeAction
	bind:value
	{placeholder}
	class="py-4 px-4 block w-full bg-slate-800/50 border border-slate-600 rounded-xl text-white placeholder-slate-400 text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 focus:bg-slate-800/70 transition-all duration-300 backdrop-blur-sm"
	required
/>
