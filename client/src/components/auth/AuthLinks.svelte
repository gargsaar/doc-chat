<script lang="ts">
	import { auth } from '$s/auth';
</script>

{#if $auth.user}
	<a
		class="font-medium text-slate-300 hover:text-red-400 transition-all duration-300 hover:scale-105 px-3 py-2 rounded-lg hover:bg-red-500/10"
		href="/auth/signout">
		<span class="hidden sm:inline">Sign Out</span>
		<span class="sm:hidden">Out</span>
	</a>
{:else}
	<a
		class="font-medium text-slate-300 hover:text-blue-400 transition-all duration-300 hover:scale-105 px-3 py-2 rounded-lg hover:bg-blue-500/10"
		href="/auth/signin">
		<span class="hidden sm:inline">Login</span>
		<span class="sm:hidden">Login</span>
	</a>
	<a
		class="font-medium bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-all duration-300 hover:scale-105 hover:shadow-lg"
		href="/auth/signup">
		<span class="hidden sm:inline">Sign Up</span>
		<span class="sm:hidden">Sign Up</span>
	</a>
{/if}
