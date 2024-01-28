<script>
  import Webcam from "./Webcam.svelte";
  import TailwindCss from './lib/TailwindCSS.svelte';
  import { SyncLoader } from 'svelte-loading-spinners';
  import './app.css';
  import MyPane from './MyPane.svelte';

  let webcamComponent;
  let isScanning = false;

  async function scan() {
    if (isScanning) {
      isScanning = false;
      return
    }
    isScanning = true;
    const capturedImage = webcamComponent.captureImage();
    console.log(capturedImage); 
    setTimeout(() => {
      isScanning = false;
    }, 5000);
  }
</script>

<div class="carousel">
<div class="carousel-item snap-start relative w-screen h-full overflow-hidden">
  <Webcam bind:this={webcamComponent} />

  <button on:click={scan} class="scan-button absolute flex items-center justify-center z-50 w-3/4 h-16 max-w-lg -translate-x-1/2 bg-purple-600 rounded-full left-1/2 bottom-4 mb-16 focus:outline-none">
    {#if isScanning}
    <SyncLoader size="55" color="#FFFFFF" unit="px" duration="1s" />
  {:else}
    <h1 class="text-2xl font-bold dark:text-white">Scan</h1>
  {/if}
  </button>  
</div>

  <div class="flex items-center w-screen h-full">
    {#if isScanning}
    <MyPane class="z-10">
      <div class="container">
        <div class="header">
          <h1 class="text-4xl font-bold loading">Give us a second</h1>
        </div>
  
        <div class="image">
          <p>Image</p>
        </div>  
  
        <div class="calories">
          <p>Calories</p>
        </div>  
  
        <div class="carbs">
          <p>Carbs</p>
        </div>
  
        <div class="fats">
          <p>Fats</p>
        </div>
  
        <div class="protein">
          <p>Protein</p>
        </div>
  
      </div>
    </MyPane>
    {/if}
  </div>

</div>


<TailwindCss/>

