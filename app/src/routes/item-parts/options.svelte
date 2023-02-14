<script>
  export let options;
  export let value;
  export let editable = false;
  export let style;
</script>

{#if editable}
  <select bind:value {style}>
    {#each options as option}
      <option value={option}>{option}</option>
    {/each}
  </select>
{:else}
  {value}
{/if}

<style>
  select {
    all: unset;
    text-align-last: center;
  }
</style>
