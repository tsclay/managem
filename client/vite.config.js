import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import preprocess from 'svelte-preprocess';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte({
			preprocess: preprocess()
		})],
	server: {
		proxy: {
			'/login': 'http://localhost:4001',
			'/logout':  'http://localhost:4001',
			'/content':  'http://localhost:4001',
			'/images':  'http://localhost:4001',
			'/galleries':  'http://localhost:4001',
			'/settings':  'http://localhost:4001',
			'/csrf-token': 'http://localhost:4001',
			'/auth-check': 'http://localhost:4001',
			'/static': 'http://localhost:4001'
		}
	}
})
