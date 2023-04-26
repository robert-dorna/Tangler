<script>
  import Icon from "../../../components/icon.svelte";
</script>

<div
  class="g-row-centered confirm-button"
  on:click|stopPropagation
  on:keypress={undefined}
>
  <Icon name="check" color="grey" size={30} />
</div>

<style>
  div.confirm-button {
    padding: var(--gap-small);
    margin-left: var(--gap-large);
  }
  div.confirm-button:hover {
    border-radius: var(--radius-small);
    background-color: var(--color-silver);
  }
</style>
