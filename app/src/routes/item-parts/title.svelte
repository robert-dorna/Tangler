<script>
  export let value;
  export let editable = false;
  export let style;
</script>

{#if editable}
  <input type="text" class="title" {style} bind:value />
{:else}
  <div class="title">
    {value}
  </div>
{/if}

<style>
  div.title {
    display: flex;
    flex-direction: column;
    margin: 5px;
    font-size: 32px;
    user-select: none;
  }
  input.title {
    all: unset;
    margin: 5px;
    font-size: 32px;
    border: none;
  }
</style>
