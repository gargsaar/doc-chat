<script lang="ts">
	import { goto, beforeNavigate } from '$app/navigation';
	import TextInput from '$c/TextInput.svelte';
	import Button from '$c/Button.svelte';
	import { auth, signin, clearErrors } from '$s/auth';
	import Alert from '$c/Alert.svelte';
	import DocChatLogo from '$c/DocChatLogo.svelte';

	let email = '';
	let password = '';

	function handleSubmit() {
		signin(email, password);
	}

	$: if ($auth.user) {
		goto('/');
	}

	beforeNavigate(clearErrors);
</script>

<svelte:head>
	<title>Sign In - DocChat</title>
</svelte:head>

<div class="min-h-screen gradient-bg flex items-center justify-center px-4 py-12">
	<!-- Background decorative elements -->
	<div class="absolute inset-0 overflow-hidden">
		<div class="absolute -top-1/2 -left-1/2 w-full h-full bg-blue-500/10 rounded-full blur-3xl"></div>
		<div class="absolute -bottom-1/2 -right-1/2 w-full h-full bg-purple-500/10 rounded-full blur-3xl"></div>
	</div>

	<div class="relative w-full max-w-md">
		<!-- Logo/Header Section -->
		<div class="text-center mb-8">
			<div class="flex justify-center mb-4">
				<DocChatLogo size="lg" />
			</div>
			<h1 class="text-xl font-bold text-white mb-2">Welcome Back</h1>
			<p class="text-slate-400">Sign in to continue chatting with your documents</p>
		</div>

		<!-- Main Form Card -->
		<div class="glass-card rounded-2xl p-8 shadow-2xl">
			<form on:submit|preventDefault={handleSubmit} class="space-y-6">
				<!-- Email Field -->
				<div class="space-y-2">
					<label for="email" class="block text-sm font-medium text-slate-300">Email Address</label>
					<TextInput 
						bind:value={email} 
						type="email" 
						placeholder="Enter your email"
					/>
				</div>

				<!-- Password Field -->
				<div class="space-y-2">
					<label for="password" class="block text-sm font-medium text-slate-300">Password</label>
					<TextInput 
						bind:value={password} 
						type="password" 
						placeholder="Enter your password"
					/>
				</div>

				<!-- Error Display -->
				{#if $auth.error}
					<Alert>
						<div class="flex items-center gap-2">
							<svg class="w-4 h-4 text-red-400" fill="currentColor" viewBox="0 0 20 20">
								<path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
							</svg>
							<span class="text-red-300">{$auth.error}</span>
						</div>
					</Alert>
				{/if}

				<!-- Submit Button -->
				<Button loading={$auth.loading} className="w-full">
					{#if !$auth.loading}
						<span class="flex items-center gap-2">
							<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
								<path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd"/>
							</svg>
							Sign In
						</span>
					{/if}
				</Button>

				<!-- Divider -->
				<div class="relative">
					<div class="absolute inset-0 flex items-center">
						<div class="w-full border-t border-slate-600"></div>
					</div>
					<div class="relative flex justify-center text-sm">
						<span class="px-4 bg-slate-800/50 text-slate-400">New to DocChat?</span>
					</div>
				</div>

				<!-- Sign Up Link -->
				<div class="text-center">
					<a 
						class="inline-flex items-center gap-2 text-blue-400 hover:text-blue-300 font-medium transition-colors duration-300 hover:underline" 
						href="/auth/signup"
					>
						<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
							<path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"/>
						</svg>
						Create an account
					</a>
				</div>
			</form>
		</div>

		<!-- Footer -->
		<div class="text-center mt-8">
			<p class="text-slate-500 text-sm">
				Secure authentication powered by modern encryption
			</p>
		</div>
	</div>
</div>
