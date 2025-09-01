<script lang="ts">
	import DocChatLogo from '$c/DocChatLogo.svelte';
	import { auth } from '$s/auth';
	
	let isMenuOpen = false;

	$: user = $auth.user;
	
	function toggleMenu() {
		isMenuOpen = !isMenuOpen;
	}
	
	function closeMenu() {
		isMenuOpen = false;
	}
</script>

<header class="modern-header mb-2 sticky top-0 z-50 w-full py-4">
	<nav
		class="max-w-7xl w-full mx-auto px-4 sm:flex sm:items-center sm:justify-between"
		aria-label="Global"
	>
		<div class="flex items-center justify-between">
			<a class="flex-none hover:scale-105 transition-transform duration-300" href="/">
				<DocChatLogo size="md" />
			</a>
			
			<!-- Hamburger button for mobile -->
			{#if user}
				<button
					type="button"
					class="sm:hidden p-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 transition-all duration-300"
					on:click={toggleMenu}
					aria-expanded={isMenuOpen}
					aria-label="Toggle navigation menu"
				>
					<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						{#if isMenuOpen}
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
						{:else}
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
						{/if}
					</svg>
				</button>
			{/if}
		</div>
		
		<!-- Desktop navigation -->
		<div class="hidden sm:flex flex-row items-center gap-4 mt-5 sm:justify-end sm:mt-0 sm:pl-5">
			{#if user}
				<a
					class="font-medium text-sm text-slate-300 hover:text-blue-400 transition-all duration-300 hover:scale-105"
					href="/documents">
					Documents
				</a>
				<a
					class="font-medium text-sm text-slate-300 hover:text-red-400 transition-all duration-300 hover:scale-105 px-2.5 py-1.5 rounded-lg hover:bg-red-500/10"
					href="/auth/signout">
					Sign Out
				</a>
			{/if}
		</div>
	</nav>
	
	<!-- Mobile navigation menu -->
	{#if user && isMenuOpen}
		<div class="sm:hidden mt-3 px-4 pb-3 border-t border-slate-700">
			<div class="flex flex-col space-y-2 pt-3">
				<a
					class="block font-medium text-sm text-slate-300 hover:text-blue-400 transition-all duration-300 py-2 px-2.5 rounded-lg hover:bg-slate-800"
					href="/documents"
					on:click={closeMenu}>
					Documents
				</a>
				<a
					class="block font-medium text-sm text-slate-300 hover:text-red-400 transition-all duration-300 py-2 px-2.5 rounded-lg hover:bg-red-500/10"
					href="/auth/signout"
					on:click={closeMenu}>
					Sign Out
				</a>
			</div>
		</div>
	{/if}
</header>
