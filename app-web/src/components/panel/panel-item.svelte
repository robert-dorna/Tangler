<script>
  export let id;

  export let emoji;
  export let name;
  export let selected = false;
</script>

<div {id} class="row align clickable panel-item" class:selected on:click|stopPropagation on:keypress={undefined}>
  {#if id === undefined}
    <div class="dot">•</div>
  {/if}
  {emoji}
  <div class="name">{name}</div>
  <div class="flex" />
  <slot />
</div>

<style>
  .panel-item {
    --panel-item-hover-true: ;
    --panel-item-hover-flase: inherit;

    margin: var(--gap-tiny);
    margin-right: var(--gap-large);
    padding: var(--gap-medium);
    padding-left: var(--gap-large);
    padding-right: var(--gap-large);
    font-size: var(--font-small);
    border-radius: var(--radius-small);
  }
  .panel-item:hover {
    --panel-item-hover-true: inherit;
    --panel-item-hover-flase: ;
  }
  .dot {
    color: var(--color-silver);
    margin-right: var(--gap-medium);
  }
  .selected {
    background-color: var(--panel-color-hover);
  }
  .name {
    margin-left: var(--gap-large);
  }
</style>
