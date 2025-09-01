<script lang="ts">
	import classNames from 'classnames';
	export let disabled = false;
	export let className = '';
	export let loading = false;
</script>

<button
	type="submit"
	class={classNames(
		'btn-enhanced w-full py-4 px-6 inline-flex justify-center items-center gap-3 rounded-xl border border-transparent font-semibold text-white focus:outline-none focus:ring-4 focus:ring-blue-500/50 transition-all text-sm disabled:opacity-50 disabled:cursor-not-allowed relative overflow-hidden',
		className
	)}
	disabled={disabled || loading}>
	{#if loading}
		<div class="spinner"></div>
		Loading...
	{:else}
		<slot />
	{/if}
</button>
