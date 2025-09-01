<script lang="ts">
	export let isOpen = false;
	export let title = 'Confirm Action';
	export let message = 'Are you sure you want to proceed?';
	export let confirmText = 'Confirm';
	export let cancelText = 'Cancel';
	export let onConfirm: () => void = () => {};
	export let onCancel: () => void = () => {};
	export let isDangerous = false;

	function handleConfirm() {
		onConfirm();
		isOpen = false;
	}

	function handleCancel() {
		onCancel();
		isOpen = false;
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape') {
			handleCancel();
		}
		if (event.key === 'Enter') {
			handleConfirm();
		}
	}

	function handleBackdropClick(event: MouseEvent) {
		if (event.target === event.currentTarget) {
			handleCancel();
		}
	}
</script>

<svelte:window on:keydown={handleKeydown} />

{#if isOpen}
	<!-- Backdrop -->
	<div 
		class="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
		on:click={handleBackdropClick}
		role="dialog"
		aria-modal="true"
		aria-labelledby="modal-title"
	>
		<!-- Modal -->
		<div class="glass-card rounded-2xl p-6 max-w-md w-full mx-4 transform transition-all duration-300 scale-100">
			<!-- Icon -->
			<div class="flex items-center justify-center w-12 h-12 mx-auto mb-4 rounded-full {isDangerous ? 'bg-red-100 dark:bg-red-900/30' : 'bg-blue-100 dark:bg-blue-900/30'}">
				{#if isDangerous}
					<svg class="w-6 h-6 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
					</svg>
				{:else}
					<svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
					</svg>
				{/if}
			</div>

			<!-- Title -->
			<h3 id="modal-title" class="text-lg font-semibold text-gray-900 dark:text-white text-center mb-2">
				{title}
			</h3>

			<!-- Message -->
			<p class="text-sm text-gray-600 dark:text-gray-300 text-center mb-6">
				{message}
			</p>

			<!-- Actions -->
			<div class="flex space-x-3">
				<button
					type="button"
					class="flex-1 px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
					on:click={handleCancel}
				>
					{cancelText}
				</button>
				<button
					type="button"
					class="flex-1 px-4 py-2 text-sm font-medium text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors {isDangerous 
						? 'bg-red-600 hover:bg-red-700 focus:ring-red-500' 
						: 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500'}"
					on:click={handleConfirm}
				>
					{confirmText}
				</button>
			</div>
		</div>
	</div>
{/if}

<style>
	/* Add smooth animation when modal appears */
	.glass-card {
		animation: modalAppear 0.3s ease-out;
	}

	@keyframes modalAppear {
		from {
			opacity: 0;
			transform: scale(0.9) translateY(-10px);
		}
		to {
			opacity: 1;
			transform: scale(1) translateY(0);
		}
	}
</style>
