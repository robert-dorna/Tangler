<script>
  import ChevronDown from "svelte-material-icons/ChevronDown.svelte";
  import ChevronUp from "svelte-material-icons/ChevronUp.svelte";
  import Dot from "svelte-material-icons/CircleSmall.svelte";

  export let expanded;
  export let color;
  export let size;
</script>

<div class="container" on:click on:keypress={undefined}>
  {#if expanded !== undefined}
    {#if expanded}
      <ChevronDown {color} {size} />
    {:else}
      <ChevronUp {color} {size} />
    {/if}
  {:else}
    <Dot {color} {size} />
  {/if}
</div>

<style>
  div.container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-right: 10px;
  }
</style>
