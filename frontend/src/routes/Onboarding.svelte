<script>
    import { onMount } from 'svelte';
    import TailwindCss from '../lib/TailwindCSS.svelte';
    import '../app.css';
    import { Input } from '@svelteuidev/core';
    import { Target, Person } from 'radix-icons-svelte';

    let goalCalories = '';
    let goalCarbs = '';
    let goalProteins = '';
    let goalFats = '';
    let userName = '';
    let errorMessage = '';

    function redirectTo(newRoute) {
    window.location.href = newRoute;
}

    function validateInputs() {
        // Reset previous error message
        errorMessage = '';

        if (!isFloatOrInteger(goalCalories) && parseFloat(goalCalories) > 0) {
            errorMessage = 'Inputs invalid.';
            return;
        }

        if (!isFloatOrInteger(goalCarbs) && parseFloat(goalCarbs) > 0) {
            errorMessage = 'Inputs invalid.';
            return;
        }

        if (!isFloatOrInteger(goalProteins) && parseFloat(goalProteins) > 0) {
            errorMessage = 'Inputs invalid.';
            return;
        }

        if (!isFloatOrInteger(goalFats) && parseFloat(goalFats) > 0) {
            errorMessage = 'Inputs invalid.';
            return;
        }

        localStorage.setItem('goalCalories', goalCalories);
        localStorage.setItem('goalCarbs', goalCarbs);
        localStorage.setItem('goalProteins', goalProteins);
        localStorage.setItem('goalFats', goalFats);
        localStorage.setItem('dailyTotalCalories', '0');
        localStorage.setItem('dailyTotalCarbs', '0');
        localStorage.setItem('dailyTotalFats', '0');
        localStorage.setItem('dailyTotalProteins', '0');
        localStorage.setItem('userName', userName);
        redirectTo('/');

        console.log('Validation passed');
    }

    function isFloatOrInteger(value) {
        return !isNaN(value) && (Number(value) == value);
    }



</script>

<TailwindCss/>

<div class="text-left -mt-10">
    <h2 class="text-3xl font-bold">
        Onboarding
    </h2>

    <Input icon={Person} 
        bind:value={userName}
        variant="filled"
        placeholder="Full name"
        radius="md"
        size="md"
        class="mt-5"
    />

    <Input icon={Target} 
        bind:value={goalCalories}
        variant="filled"
        placeholder="Daily Calorie Goal (cal)"
        radius="md"
        size="md"
        class="mt-3"
    />

    <Input icon={Target} 
        bind:value={goalCarbs}
        variant="filled"
        placeholder="Daily Carb Goal (cal)"
        radius="md"
        size="md"
        class="mt-3"
    />


        <Input icon={Target} 
        bind:value={goalFats}
        variant="filled"
        placeholder="Daily Fat Goal (cal)"
        radius="md"
        size="md"
        class="mt-3"
    />

        <Input icon={Target} 
        bind:value={goalProteins}
        variant="filled"
        placeholder="Daily Protein Goal (gram)"
        radius="md"
        size="md"
        class="mt-3"
        />
    {#if errorMessage}
        <p class="text-red-500 mt-3">{errorMessage}</p>
    {/if}

    <button on:click={validateInputs} class="scan-button flex items-center justify-center rounded-full p-3 mt-5">
        <h1 class="text-md font-semibold dark:text-white">Get Started</h1>
    </button>
</div>
