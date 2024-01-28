import { svelte } from '@sveltejs/vite-plugin-svelte';
import mkcert from 'vite-plugin-mkcert';

export default {
  plugins: [svelte(), mkcert()],
  server: {
    https: true
  }
};
