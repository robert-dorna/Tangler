<script>
  import Icon from "../../components/icon.svelte";

  export let name;
  export let color;
</script>

<div
  class="g-row-centered button"
  on:click|stopPropagation
  on:keypress={undefined}
>
  <Icon {name} {color} size={20} />
</div>

<style>
  div.button {
    border-radius: var(--radius-small);
    padding: var(--gap-small);
  }
  div.button:hover {
    background-color: var(--panel-color-button-hover);
  }
</style>
