/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}', 'node_modules/preline/dist/*.js'],
	theme: {
		extend: {
			fontFamily: {
				'sans': [
					'ui-sans-serif', 
					'system-ui', 
					'-apple-system', 
					'BlinkMacSystemFont', 
					'Segoe UI', 
					'Roboto', 
					'Inter', 
					'Helvetica Neue', 
					'Arial', 
					'Noto Sans', 
					'sans-serif', 
					'Apple Color Emoji', 
					'Segoe UI Emoji', 
					'Segoe UI Symbol', 
					'Noto Color Emoji'
				],
			},
			fontSize: {
				'xs': ['0.75rem', { lineHeight: '1.125rem' }],    // 12px
				'sm': ['0.875rem', { lineHeight: '1.25rem' }],    // 14px  
				'base': ['1rem', { lineHeight: '1.5rem' }],       // 16px
				'lg': ['1.125rem', { lineHeight: '1.75rem' }],    // 18px
				'xl': ['1.25rem', { lineHeight: '1.875rem' }],    // 20px
				'2xl': ['1.5rem', { lineHeight: '2.25rem' }],     // 24px
				'3xl': ['1.875rem', { lineHeight: '2.5rem' }],    // 30px
				'4xl': ['2.25rem', { lineHeight: '2.75rem' }],    // 36px
			}
		}
	},
	plugins: [require('preline/plugin')]
};
