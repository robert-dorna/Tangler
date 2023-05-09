<script>
  import Icon from "../icon.svelte";

  export let name;
  export let color;
  export let size;
  export let text;
</script>

<div class="row align clickable editor-button" on:click|preventDefault on:keypress={undefined}>
  <Icon {name} {color} {size} />
  {text}
</div>

<style>
  .editor-button {
    padding: var(--gap-small);
    padding-left: var(--gap-large);
    padding-right: var(--gap-large);
    border-radius: var(--radius-small);
    border: var(--gap-line) solid var(--color-silver);
    gap: var(--gap-small);
  }
</style>
