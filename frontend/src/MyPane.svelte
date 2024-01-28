<!-- MyPane.svelte -->
<script>
    import { onMount, onDestroy } from 'svelte';
    import { CupertinoPane } from 'cupertino-pane/dist/cupertino-pane.esm';
  
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
    });
  
    onDestroy(() => {
      myPane.destroy();
    });
  </script>
  
  <div bind:this={paneElement}>
    <!-- Slot for custom content -->
    <slot></slot>
  </div>
  
  <style>
    .pane {
      /* Styles for your pane container */
    }
  </style>
  