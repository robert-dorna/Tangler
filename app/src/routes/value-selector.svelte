<script>
  import { createEventDispatcher } from "svelte";

  export let colors;
  export let style = undefined;

  const dispatch = createEventDispatcher()

  $: values = Object.keys(colors);
</script>

<div class="container" {style}>
  <div class="wrap">
    {#each values as value (value)}
      <div
        class="value"
        style="color: {colors[value]};"
        on:click={() => dispatch('select', { value })}
        on:keypress={undefined}
      >
        {value}
      </div>
    {/each}
  </div>
</div>

<style>
  div.container {
    display: flex;
    flex-direction: column;
    background-color: white;
    border-radius: 8px;
    padding: 2px;
    position: absolute;
    z-index: 1;
    box-shadow: 8px 8px 24px 0px rgba(66, 68, 90, 1);
  }
  div.wrap {
    display: flex;
    flex-direction: column;
    max-height: 20vw;
    /*
      Cannot use wrap because of a bug
      https://stackoverflow.com/questions/33891709/when-flexbox-items-wrap-in-column-mode-container-does-not-grow-its-width
    */
    /* flex-wrap: wrap; */
    overflow: scroll;
  }
  div.value {
    display: flex;
    background-color: white;
    padding: 20px;
  }
  div.value:hover {
    background-color: #f4f3ee;
  }
</style>
