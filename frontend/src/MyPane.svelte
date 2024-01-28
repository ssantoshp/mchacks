<!-- MyPane.svelte -->
<script>
    import { onMount, onDestroy } from 'svelte';
    import { CupertinoPane } from 'cupertino-pane/dist/cupertino-pane.esm';
    import { resultReleased, isScanning } from './store.js';
  
    let paneElement; // Reference to the DOM element
    let myPane; // Instance of CupertinoPane
  
    onMount(() => {
      myPane = new CupertinoPane(paneElement, {
        // Cupertino Pane options
        buttonClose: true,
        from: 'bottom',
        initialBreak: 'middle',
        breaks: {
          middle: { enabled: true, height: 300 },
          bottom: { enabled: true, height: 100 },
        },
      });
  

      myPane.present({ animate: true });

      myPane.on('onDidDismiss', (e) => {
      resultReleased.set(false);
      isScanning.set(false);
    });

    });


  
    onDestroy(() => {
      myPane.destroy();
    });
  </script>
  
  <div bind:this={paneElement}>
    <slot></slot>
  </div>
  
  