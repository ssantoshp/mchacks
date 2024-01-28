<script>
  import { onMount } from 'svelte';
  import Webcam from "../Webcam.svelte";
  import TailwindCss from '../lib/TailwindCSS.svelte';
  import { SyncLoader } from 'svelte-loading-spinners';
  import '../app.css';
  import MyPane from '../MyPane.svelte';
  import { resultReleased, isScanning } from '../store.js';

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
  
  let cameraSound = new Audio('../src/assets/camera_sound.mp3');
  let capturedImage = null;
  let webcamComponent;

  let goalCalories = localStorage.getItem('goalCalories');
  let goalCarbs = localStorage.getItem('goalCarbs');
  let goalProteins = localStorage.getItem('goalProteins');
  let goalFats = localStorage.getItem('goalFats');

  let dailyTotalCalories = localStorage.getItem('dailyTotalCalories');
  let dailyTotalCarbs = localStorage.getItem('dailyTotalCarbs');
  let dailyTotalProteins = localStorage.getItem('dailyTotalProteins');
  let dailyTotalFats = localStorage.getItem('dailyTotalFats');

  let colorStopCalories = "0%";
  let colorStopAfterCalories = "100%";

  let colorStopCarbs = "0%";
  let colorStopAfterCarbs = "100%";

  let colorStopProteins = "0%";
  let colorStopAfterProteins = "100%";

  let colorStopFats = "0%";
  let colorStopAfterFats = "100%";


  function sendTweet(){
    return
      }

  async function scan() {
    resultReleased.set(false);
    if ($isScanning) {
      isScanning.set(false);
      capturedImage = null;
      return;
    }
    dailyTotalCalories = (parseFloat(localStorage.getItem('dailyTotalCalories')) + 800).toString();
    dailyTotalCarbs = (parseFloat(localStorage.getItem('dailyTotalCarbs')) + 1100).toString();
    dailyTotalFats = (parseFloat(localStorage.getItem('dailyTotalFats')) + 400).toString();
    dailyTotalProteins = (parseFloat(localStorage.getItem('dailyTotalProteins')) + 1500).toString();

    cameraSound.play();
    isScanning.set(true);
    capturedImage = await webcamComponent.captureImage();
    setTimeout(() => {
       isScanning.set(false);
    }, 5000);

    console.log("Scanning...");

    // Convert the base64-encoded image data to a Blob
    const base64Data = capturedImage.split(',')[1];
    const contentType = capturedImage.split(',')[0].split(';')[0].split(':')[1];
    const blob = new Blob([Uint8Array.from(atob(base64Data), c => c.charCodeAt(0))], { type: contentType });

    // Create a FormData object and append the Blob
    const formData = new FormData();
    formData.append('food_pic', blob, 'image.jpg');

    resultReleased.set(true);

    let fillRatioCalories = (dailyTotalCalories / goalCalories) * 100;
    fillRatioCalories = Math.min(Math.max(fillRatioCalories, 0), 100); 
    colorStopCalories = `${fillRatioCalories}%`;
    colorStopAfterCalories = `${Math.min(fillRatioCalories + 0.1, 100)}%`;

    let fillRatioCarbs = (dailyTotalCarbs / goalCarbs) * 100;
    fillRatioCarbs = Math.min(Math.max(fillRatioCarbs, 0), 100); 
    colorStopCarbs = `${fillRatioCarbs}%`;
    colorStopAfterCarbs = `${Math.min(fillRatioCarbs + 0.1, 100)}%`;

    let fillRatioFats = (dailyTotalFats / goalFats) * 100;
    fillRatioFats = Math.min(Math.max(fillRatioFats, 0), 100); 
    colorStopFats = `${fillRatioFats}%`;
    colorStopAfterFats = `${Math.min(fillRatioFats + 0.1, 100)}%`;

    let fillRatioProteins = (dailyTotalProteins / goalProteins) * 100;
    fillRatioProteins = Math.min(Math.max(fillRatioProteins, 0), 100); 
    colorStopProteins = `${fillRatioProteins}%`;
    colorStopAfterProteins = `${Math.min(fillRatioProteins + 0.1, 100)}%`;

  console.log(colorStopCalories);

    const response = await fetch('http://localhost:80/foodsnaps/', {
      method: 'POST',
      mode: 'no-cors',
      body: formData, 
    });
    
    const data = await response.json();
    console.log(data);
    //resultReleased.set(true);
    }

    onMount(() => {
      if (!localStorage.getItem('goalCalories') || !localStorage.getItem('goalCarbs') || !localStorage.getItem('goalProteins') || !localStorage.getItem('goalFats') || !localStorage.getItem('userName')){
        window.location.href = '/onboarding';
      }
    });

</script>

<TailwindCss/>

  <Webcam bind:this={webcamComponent} />

  <button on:click={scan} class="scan-button absolute flex items-center justify-center z-20 w-3/4 h-16 max-w-lg -translate-x-1/2 bg-purple-600 rounded-full left-1/2 bottom-4 mb-16 focus:outline-none">
    {#if $isScanning}
    <SyncLoader size="55" color="#FFFFFF" unit="px" duration="1s" />
  {:else}
    <h1 class="text-2xl font-bold dark:text-white">🔎 Scan</h1>
  {/if}
  </button>  

  <div class="flex items-center w-screen h-full">
    {#if $isScanning || $resultReleased}
    <MyPane class="z-4">
      <div class="container">
        <div class="header">
          {#if $isScanning}
          <h1 class="text-3xl font-bold loading">Give us a second</h1>
          {:else}
          <h1 class="text-3xl font-bold">Report</h1>
          {/if}
        </div>
  
        {#if capturedImage}
        <div class="image">
          <img src={capturedImage}
          alt="food"
          class="rounded-lg"/>
        </div>  
        {/if}
  
        <div class="calories" style="background-image: linear-gradient(0deg, #ff418a 0%, #ff418a {colorStopCalories}, #e10056 {colorStopCalories}, #e10056 {colorStopAfterCalories}, #8b0018 {colorStopAfterCalories});">
          {#if $isScanning}
          <p class="loading text-4xl font-bold right-0 top-0 p-1"></p>
          {:else}
          <p class="text-4xl font-bold right-0 top-0 p-1">{dailyTotalCalories}</p>
          {/if}
          <p class="font-semibold">Calories</p>
        </div>
  
        <div class="carbs" style="background-image: linear-gradient(0deg, #ffdc50 0%, #ffdc50 {colorStopCarbs}, #ffcd04 {colorStopCarbs}, #ffcd04 {colorStopAfterCarbs}, #ffcd04  {colorStopAfterCarbs});">
          {#if $isScanning}
          <p class="loading text-4xl font-bold right-0 top-0 p-1"></p>
          {:else}
          <p class="text-4xl font-bold right-0 top-0 p-1">{dailyTotalCarbs}</p>
          {/if}
          <p class="font-semibold">Carbs</p>
        </div>
  
  
        <div class="fats" style="background-image: linear-gradient(0deg, #20ffc3 0%, #20ffc3 {colorStopFats}, #00DFA2 {colorStopFats}, #00DFA2 {colorStopAfterFats});">
          {#if $isScanning}
          <p class="loading text-4xl font-bold right-0 top-0 p-1"></p>
          {:else}
          <p class="text-4xl font-bold right-0 top-0 p-1">{dailyTotalFats}</p>
          {/if}
          <p class="font-semibold">Fats</p>
        </div>
  
        <div class="protein" style="background-image: linear-gradient(0deg, #3191ff 0%, #3191ff {colorStopProteins}, #0079FF {colorStopProteins}, #0079FF {colorStopAfterProteins});">
          {#if $isScanning}
          <p class="loading text-4xl font-bold right-0 top-0 p-1"></p>
          {:else}
          <p class="text-4xl font-bold right-0 top-0 p-1">{dailyTotalProteins}</p>
          {/if}
          <p class="font-semibold">Proteins</p>
        </div>
      </div>
      
      {#if $isScanning}
      <div class="mb-40"></div>
      {:else}
      <h2 class="ingredients mt-5 text-2xl font-semibold">Ingredients detected</h2>

      <div class="grid grid-cols-2 gap-4">
        {#each ingredients as ingredient}
          <div class="text-lg border-b border-gray-200 mr-10 ml-10">
            <p>{ingredient}</p>
          </div>
        {/each}
      </div>

      {/if}

      <div class="mb-40"></div>

    </MyPane>
    {/if}

    </div>
    
