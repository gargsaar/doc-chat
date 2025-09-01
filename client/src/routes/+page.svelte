<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { auth, signin, signup, clearErrors } from '$s/auth';
	import TextInput from '$c/TextInput.svelte';
	import Button from '$c/Button.svelte';
	import Alert from '$c/Alert.svelte';
	import DocChatLogo from '$c/DocChatLogo.svelte';

	let activeTab = 'signin'; // 'signin' or 'signup'
	let email = '';
	let password = '';
	let passwordConfirm = '';
	let passwordMismatch = false;

	function handleSignIn() {
		signin(email, password);
	}

	function handleSignUp() {
		if (password !== passwordConfirm) {
			passwordMismatch = true;
			return;
		}
		passwordMismatch = false;
		signup(email, password);
	}

	function switchTab(tab) {
		activeTab = tab;
		email = '';
		password = '';
		passwordConfirm = '';
		passwordMismatch = false;
		clearErrors();
	}

	$: if ($auth.user) {
		goto('/documents');
	}

	// Reset password mismatch when passwords change
	$: if (password || passwordConfirm) {
		passwordMismatch = false;
	}

	onMount(() => {
		if ($auth.user) {
			goto('/documents');
		}
	});
</script>

<svelte:head>
	<title>DocChat - AI-Powered Document Conversations</title>
	<meta name="description" content="Transform your documents into interactive conversations with AI" />
</svelte:head>

<div class="bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 py-8 px-6 lg:px-8">
	<!-- Background decorative elements -->
	<div class="absolute inset-0 overflow-hidden">
		<div class="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl"></div>
		<div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl"></div>
		<div class="absolute top-3/4 left-3/4 w-64 h-64 bg-cyan-500/20 rounded-full blur-2xl"></div>
	</div>

	<div class="relative w-full max-w-6xl mx-auto grid lg:grid-cols-2 gap-8 lg:gap-12 items-center">
		<!-- Left side - Branding and Features (Hidden on mobile) -->
		<div class="hidden lg:block text-left space-y-8">
			<div class="space-y-6">
				<h1 class="text-5xl lg:text-4xl font-bold text-white leading-tight">
					Welcome to
					<span class="bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent block">
						DocChat
					</span>
				</h1>
				<p class="text-xl text-slate-300 leading-relaxed">
					Transform your documents into interactive conversations. Upload PDFs and chat with your content using advanced AI.
				</p>
			</div>

			<div class="space-y-4">
				<div class="flex items-center gap-3 text-slate-300">
					<div class="w-8 h-8 bg-blue-500/20 rounded-full flex items-center justify-center">
						<svg class="w-4 h-4 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
							<path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
						</svg>
					</div>
					<span>Upload and analyze any PDF document</span>
				</div>
				<div class="flex items-center gap-3 text-slate-300">
					<div class="w-8 h-8 bg-blue-500/20 rounded-full flex items-center justify-center">
						<svg class="w-4 h-4 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
							<path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
						</svg>
					</div>
					<span>Ask questions and get instant answers</span>
				</div>
				<div class="flex items-center gap-3 text-slate-300">
					<div class="w-8 h-8 bg-blue-500/20 rounded-full flex items-center justify-center">
						<svg class="w-4 h-4 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
							<path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
						</svg>
					</div>
					<span>Powered by advanced AI technology</span>
				</div>
				<div class="flex items-center gap-3 text-slate-300">
					<div class="w-8 h-8 bg-blue-500/20 rounded-full flex items-center justify-center">
						<svg class="w-4 h-4 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
							<path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
						</svg>
					</div>
					<span>Secure authentication powered by modern encryption</span>
				</div>
			</div>

			<div class="text-slate-400 text-sm">
				Join thousands of users who are already transforming how they work with documents
			</div>
		</div>

		<!-- Right side - Auth Form -->
		<div class="w-full max-w-md mx-auto lg:mx-0 lg:col-span-1">
			<div class="glass-card rounded-2xl p-6 shadow-2xl">
				<!-- Tab Navigation -->
				<div class="flex bg-slate-800/50 rounded-xl p-1 mb-6">
					<button
						class="flex-1 py-2.5 px-4 rounded-lg font-medium transition-all duration-300 {activeTab === 'signin' ? 'bg-blue-600 text-white shadow-lg' : 'text-slate-400 hover:text-white'}"
						on:click={() => switchTab('signin')}
					>
						Sign In
					</button>
					<button
						class="flex-1 py-2.5 px-4 rounded-lg font-medium transition-all duration-300 {activeTab === 'signup' ? 'bg-blue-600 text-white shadow-lg' : 'text-slate-400 hover:text-white'}"
						on:click={() => switchTab('signup')}
					>
						Sign Up
					</button>
				</div>

				<!-- Form Header -->
				<div class="text-center mb-5">
					<h2 class="text-xl font-bold text-white mb-1">
						{activeTab === 'signin' ? 'Welcome Back' : 'Get Started'}
					</h2>
					<p class="text-slate-400 text-sm">
						{activeTab === 'signin' 
							? 'Continue your document conversations' 
							: 'Create your account in seconds'}
					</p>
				</div>

				<!-- Form Content -->
				{#if activeTab === 'signin'}
					<form on:submit|preventDefault={handleSignIn} class="space-y-4">
						<div class="space-y-1">
							<label for="email" class="block text-sm font-medium text-slate-300">Email</label>
							<TextInput 
								bind:value={email} 
								type="email" 
								placeholder="Enter your email"
							/>
						</div>

						<div class="space-y-1">
							<label for="password" class="block text-sm font-medium text-slate-300">Password</label>
							<TextInput 
								bind:value={password} 
								type="password" 
								placeholder="Enter your password"
							/>
						</div>

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

						<Button loading={$auth.loading} className="w-full">
							{#if !$auth.loading}
								Sign In to DocChat
							{/if}
						</Button>
					</form>
				{:else}
					<form on:submit|preventDefault={handleSignUp} class="space-y-4">
						<div class="space-y-1">
							<label for="email" class="block text-sm font-medium text-slate-300">Email</label>
							<TextInput 
								bind:value={email} 
								type="email" 
								placeholder="Enter your email"
							/>
						</div>

						<div class="space-y-1">
							<label for="password" class="block text-sm font-medium text-slate-300">Password</label>
							<TextInput 
								bind:value={password} 
								type="password" 
								placeholder="Create a password"
							/>
						</div>

						<div class="space-y-1">
							<label for="passwordConfirm" class="block text-sm font-medium text-slate-300">Confirm Password</label>
							<TextInput 
								bind:value={passwordConfirm} 
								type="password" 
								placeholder="Confirm your password"
							/>
						</div>

						{#if passwordMismatch}
							<Alert>
								<div class="flex items-center gap-2">
									<svg class="w-4 h-4 text-red-400" fill="currentColor" viewBox="0 0 20 20">
										<path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
									</svg>
									<span class="text-red-300">Passwords do not match</span>
								</div>
							</Alert>
						{/if}

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

						<Button loading={$auth.loading} className="w-full">
							{#if !$auth.loading}
								Create Account
							{/if}
						</Button>
					</form>
				{/if}

				<!-- Footer -->
				<div class="text-center mt-4 pt-4 border-t border-slate-600">
					<p class="text-slate-400 text-xs">
						By continuing, you agree to our Terms of Service
					</p>
				</div>
			</div>
		</div>
	</div>
</div>
