<script>
  import { onMount } from 'svelte';
  let videoElement;
  let stream;
  let canvas;

  async function startWebcam() {
    try {
      stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment" }
    });
      videoElement.srcObject = stream;
    } catch (err) {
      console.error('Error accessing the webcam', err);
    }
  }

  onMount(() => {
    startWebcam();

    return () => {
      if (stream) {
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
      }
    };
  });

  export function captureImage() {
    const context = canvas.getContext('2d');
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    
    return canvas.toDataURL('image/png');
  }
</script>

<video bind:this={videoElement} autoplay playsinline class="w-screen h-screen object-cover"></video>
<canvas bind:this={canvas} class="hidden"></canvas> 

