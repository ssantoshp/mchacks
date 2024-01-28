<script>
  import Webcam from "./Webcam.svelte";
  import TailwindCss from './lib/TailwindCSS.svelte';
  import { SyncLoader } from 'svelte-loading-spinners';
  import './app.css';
  import MyPane from './MyPane.svelte';

  import { SkeletonText } from "@skeleton-elements/svelte";

  let ingredients = [
    "Burger Bun",
    "Beef Patty",
    "Lettuce",
    "Tomato",
    "Onion",
    "Cheese",
    "Ketchup",
    "Pickles",
    "Bacon",
    "Egg",
    "Mushrooms",
  ]

  let cameraSound = new Audio('/src/assets/camera_sound.mp3');
  let effect = "pulse";
  let capturedImage = null;
  let webcamComponent;
  let isScanning = false;

  async function scan() {
    if (isScanning) {
      isScanning = false;
      return;
    }
    cameraSound.play();
    isScanning = true;
    console.log("Scanning...");
    capturedImage = await webcamComponent.captureImage(); 
    console.log(capturedImage);
    setTimeout(() => {
      isScanning = false;
    }, 5000);
  }
</script>

<TailwindCss/>


  <Webcam bind:this={webcamComponent} />

  <button on:click={scan} class="scan-button absolute flex items-center justify-center z-20 w-3/4 h-16 max-w-lg -translate-x-1/2 bg-purple-600 rounded-full left-1/2 bottom-4 mb-16 focus:outline-none">
    {#if isScanning}
    <SyncLoader size="55" color="#FFFFFF" unit="px" duration="1s" />
  {:else}
    <h1 class="text-2xl font-bold dark:text-white">🔎 Scan</h1>
  {/if}
  </button>  

  <div class="flex items-center w-screen h-full">

    <MyPane class="z-4">
      <div class="container">
        <div class="header">
          {#if isScanning}
          <h1 class="text-3xl font-bold loading">Give us a second</h1>
          {:else}
          <h1 class="text-3xl font-bold">Today's Review</h1>
          {/if}
        </div>
  
        {#if capturedImage}
        <div class="image">
          <img src={capturedImage}
          alt="food"
          class="rounded-lg"/>
        </div>  
        {/if}
  
        <div class="calories">
          <SkeletonText tag="div" effect={effect}>
          <p class="text-4xl font-bold right-0 top-0 p-1">500</p>
          </SkeletonText>
          <p class="font-semibold">Calories</p>
        </div>  
  
        <div class="carbs">
          <p class="text-4xl font-semibold p-1">500</p>
          <p class="font-semibold">Carbs</p>
        </div>
  
        <div class="fats">
          <p class="text-4xl font-semibold p-1">500</p>
          <p class="font-semibold">Fats</p>
        </div>
  
        <div class="protein">
          <p class="text-4xl font-semibold p-1">500</p>
          <p class="font-semibold">Proteins</p>
        </div>
      </div>

      <h2 class="ingredients mt-5 text-2xl font-semibold">Ingredients detected</h2>

      <div class="grid grid-cols-2 gap-4">
        {#each ingredients as ingredient}
          <div class="text-lg border-b border-gray-200 mr-10 ml-10">
            <p>{ingredient}</p>
          </div>
        {/each}
      </div>
      

      <div class="mb-40"></div>

    </MyPane>

    </div>
    
