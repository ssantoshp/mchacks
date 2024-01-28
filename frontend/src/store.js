// src/store.js
import { writable } from 'svelte/store';

export const resultReleased = writable(false);
export const isScanning = writable(false);
