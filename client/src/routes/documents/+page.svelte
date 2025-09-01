<script lang="ts">
	import type { PageData } from './$types';
	import AuthGuard from '$c/AuthGuard.svelte';
	import ConfirmModal from '$c/ConfirmModal.svelte';
	import { deleteDocument, documents as documentsStore } from '$s/documents';

	export let data: PageData;

	const documents = data.documents || [];
	
	// Sort documents by created_on date, latest first
	$: sortedDocuments = documents.sort((a, b) => {
		const dateA = new Date(a.created_on || a.id).getTime();
		const dateB = new Date(b.created_on || b.id).getTime();
		return dateB - dateA;
	});
	
	// Function to format date
	function formatDate(dateString: string) {
		if (!dateString) return 'N/A';
		try {
			return new Date(dateString).toLocaleDateString('en-US', {
				year: 'numeric',
				month: 'short',
				day: 'numeric'
			});
		} catch {
			return 'N/A';
		}
	}
	
	// Function to truncate filename
	function truncateFilename(filename: string, maxLength: number = 50): string {
		if (filename.length <= maxLength) return filename;
		
		const extension = filename.split('.').pop();
		const nameWithoutExt = filename.substring(0, filename.lastIndexOf('.'));
		
		if (extension) {
			const maxNameLength = maxLength - extension.length - 4; // 4 for "..." and "."
			return nameWithoutExt.substring(0, maxNameLength) + '...' + '.' + extension;
		}
		
		return filename.substring(0, maxLength - 3) + '...';
	}
	
	// Modal state
	let showDeleteModal = false;
	let documentToDelete: { id: string; name: string } | null = null;
	
	// Function to show delete confirmation
	function showDeleteConfirmation(documentId: string, documentName: string) {
		documentToDelete = { id: documentId, name: documentName };
		showDeleteModal = true;
	}
	
	// Function to handle confirmed deletion
	async function handleConfirmDelete() {
		if (!documentToDelete) return;
		
		try {
			console.log(`Deleting document: ${documentToDelete.id}`);
			await deleteDocument(documentToDelete.id);
			console.log('Document deleted successfully');
			// Refresh the page to show updated list
			location.reload();
		} catch (error) {
			console.error('Delete failed:', error);
			alert(`Failed to delete document: ${error}`);
		} finally {
			documentToDelete = null;
		}
	}
	
	// Function to handle cancel deletion
	function handleCancelDelete() {
		documentToDelete = null;
	}
</script>

<AuthGuard />
<div class="px-2 sm:px-4 py-6">
	<!-- Show error if any -->
	{#if $documentsStore.error}
		<div class="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
			Error: {$documentsStore.error}
		</div>
	{/if}
	
	<div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-3">
		<h2 class="text-xl md:text-2xl font-semibold text-white">Your Documents</h2>
		<div>
			<a
				href="/documents/new"
				class="py-2.5 px-4 inline-flex justify-center items-center gap-2 rounded-lg border border-transparent font-medium bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all dark:focus:ring-offset-gray-800 text-sm"
				>Upload Doc</a
			>
		</div>
	</div>

	<div class="flex flex-col max-w-full">
		<div class="overflow-x-auto">
			<div class="inline-block min-w-full align-middle">
				<div class="border rounded-lg overflow-hidden max-h-80 overflow-y-auto">
					<table class="w-full divide-y divide-gray-200 dark:divide-gray-700">
						<thead class="bg-gray-50 dark:bg-gray-800 sticky top-0">
							<tr>
								<th
									scope="col"
									class="px-4 md:px-6 py-3.5 text-left text-sm font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Name</th
								>
								<th
									scope="col"
									class="px-4 md:px-6 py-3.5 text-left text-sm font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider hidden sm:table-cell">Date</th
								>
								<th
									scope="col"
									class="px-4 md:px-6 py-3.5 text-right text-sm font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Action</th
								>
							</tr>
						</thead>

						<tbody class="divide-y divide-gray-200 dark:divide-gray-700">
							{#each sortedDocuments as document}
								<tr class="hover:bg-gray-100 dark:hover:bg-gray-700">
									<td
										class="px-4 md:px-6 py-4 text-sm font-medium text-gray-800 dark:text-gray-200"
										title={document.name}
									>
										<div class="flex flex-col">
											<span class="truncate max-w-xs text-sm">
												{truncateFilename(document.name, 40)}
											</span>
											<span class="text-xs text-gray-500 dark:text-gray-400 sm:hidden mt-1">
												{formatDate(document.created_on || document.id)}
											</span>
										</div>
									</td>
									<td class="px-4 md:px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-gray-200 hidden sm:table-cell"
										>{formatDate(document.created_on || document.id)}</td
									>
									<td class="px-4 md:px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
										<div class="flex flex-col sm:flex-row sm:justify-end gap-2">
											<a class="text-blue-600 hover:text-blue-700 text-sm py-2 px-3 rounded-md bg-blue-50 dark:bg-blue-900/20 text-center font-medium transition-colors" href="/documents/{document.id}"
												>Chat</a
											>
											<button 
												class="text-red-600 hover:text-red-700 transition-colors text-sm py-2 px-3 rounded-md bg-red-50 dark:bg-red-900/20 font-medium"
												on:click={() => showDeleteConfirmation(document.id, document.name)}
											>
												Delete
											</button>
										</div>
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			</div>
		</div>
	</div>
</div>

<!-- Delete Confirmation Modal -->
<ConfirmModal
	bind:isOpen={showDeleteModal}
	title="Delete Document"
	message={documentToDelete ? `Are you sure you want to delete "${documentToDelete.name}"? This action cannot be undone and will remove the document, its embeddings, and all associated data.` : ''}
	confirmText="Delete"
	cancelText="Cancel"
	isDangerous={true}
	onConfirm={handleConfirmDelete}
	onCancel={handleCancelDelete}
/>
