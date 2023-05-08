<script>
  import Icon from "../icon.svelte";

  export let name;
  export let color;
  export let size;
  export let text;
</script>

<div class="g-row-aligned g-clickable button" on:click|preventDefault on:keypress={undefined}>
  <Icon {name} {color} {size} />
  {text}
</div>

<style>
  .button {
    padding: var(--gap-small);
    padding-left: var(--gap-large);
    padding-right: var(--gap-large);
    border-radius: var(--radius-small);
    border: 1px solid silver;
    gap: var(--gap-small);
  }
</style>
