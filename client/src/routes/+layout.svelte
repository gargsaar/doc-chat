<script lang="ts">
	import '../app.css';
	import 'material-icons/iconfont/material-icons.css';
	import { onMount } from 'svelte';
	import Navbar from '$c/Navbar.svelte';
	import ErrorModal from '$c/ErrorModal.svelte';
	import { getUser, auth } from '$s/auth';

	export const ssr = false;

	$: user = $auth.user;

	onMount(() => {
		if (user === null) {
			getUser();
		}
	});
</script>

<ErrorModal />
<div class="min-h-screen bg-slate-900">
	<Navbar />
	<main class="container mx-auto px-4 py-8">
		<slot />
	</main>
</div>
