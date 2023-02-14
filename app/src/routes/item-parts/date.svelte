<script>
  export let value;
  export let editable = false;
  export let style;
</script>

{#if editable}
  <input type="date" bind:value {style}/>
{:else if value}
  <div>
    {value}
  </div>
{/if}

<style>
  input {
    all: unset;
  }
</style>
