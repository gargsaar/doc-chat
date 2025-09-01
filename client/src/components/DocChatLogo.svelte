<script lang="ts">
	export let size = 'md'; // 'sm', 'md', 'lg'
	export let showText = true;
	
	$: logoSize = size === 'sm' ? 'w-8 h-8' : size === 'lg' ? 'w-16 h-16' : 'w-12 h-12';
	$: textSize = size === 'sm' ? 'text-lg' : size === 'lg' ? 'text-3xl' : 'text-2xl';
</script>

<div class="flex items-center gap-3">
	<!-- Logo Icon -->
	<div class="relative {logoSize}">
		<!-- Speech bubble background -->
		<div class="absolute inset-0 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl shadow-lg"></div>
		<!-- Document/D icon -->
		<div class="relative w-full h-full flex items-center justify-center">
			<svg class="w-2/3 h-2/3 text-white font-bold" viewBox="0 0 24 24" fill="currentColor">
				<path d="M6 2C4.9 2 4 2.9 4 4V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V8L14 2H6ZM6 4H13V9H18V20H6V4Z"/>
			</svg>
		</div>
		<!-- Chat indicator dot -->
		<div class="absolute -bottom-1 -right-1 w-3 h-3 bg-green-400 rounded-full border-2 border-white shadow-sm"></div>
	</div>
	
	{#if showText}
		<span class="font-bold text-white {textSize} tracking-tight">
			DocChat
		</span>
	{/if}
</div>
