<script lang="ts">
  import { Router, Route } from 'svelte-routing';
  import Home from './routes/Home.svelte'; 
  import Onboarding from './routes/Onboarding.svelte';
</script>


<main>

  <Router>
    <Route path="/" component={Home} />
    <Route path="/onboarding" component={Onboarding} />
  </Router>

</main>