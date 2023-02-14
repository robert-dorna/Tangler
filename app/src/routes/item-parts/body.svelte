<script>
  export let value;
  export let editable = false;
  export let style;
</script>

{#if editable}
  <textarea type="text" class="body" {style} bind:value placeholder="add body message..."/>
{:else if value}
  <div class="body">
    {value}
  </div>
{/if}

<style>
  div.body {
    display: flex;
    flex-direction: column;
    padding: 10px;
    color: grey;
    font-size: 24px;
  }
  textarea.body {
    all: unset;
    white-space: pre-wrap;
    display: flex;
    flex-direction: column;
    padding: 10px;
    color: grey;
    font-size: 24px;
  }
</style>
