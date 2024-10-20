<script lang="ts">
	import { ipcRenderer } from 'electron';
	import type { IpcRendererEvent } from 'electron';

	async function toggleDarkMode() {
		await ipcRenderer.send("requestToggle")
		await ipcRenderer.on("receiveToggle", (_event: IpcRendererEvent, shouldUseDarkColors: boolean) => {
			console.log(shouldUseDarkColors)
		});
	}

	async function resetToSystem() {
		ipcRenderer.send("requestSystem")
	}
</script>

<button on:click={toggleDarkMode}>
	Toggle Dark Mode
</button>

<button on:click={resetToSystem}>
	Reset To System
</button>