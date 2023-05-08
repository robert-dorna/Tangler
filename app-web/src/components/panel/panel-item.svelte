<script>
  export let emoji;
  export let name;
  export let selected = false;
  export let title = false;
</script>

<div class="row align item clickable" class:hover-highlight={!title} class:selected on:click on:keypress={undefined}>
  {emoji}
  <div class="name" class:title>{name}</div>
  <div class="flex" />
  <slot />
</div>

<style>
  :global(:root) {
    --x-buttons-visibility: hidden;
  }
  div.selected {
    background-color: var(--panel-color-hover);
  }
  div.name {
    margin-left: var(--gap-large);
  }
  div.title {
    font-weight: bold;
    margin-left: 0px;
  }
  div.item {
    margin: var(--gap-tiny);
    margin-right: var(--gap-large);
    padding: var(--gap-medium);
    padding-left: var(--gap-large);
    padding-right: var(--gap-large);
    font-size: var(--font-small);
    border-radius: var(--radius-small);
  }
  div.item:hover {
    --x-buttons-visibility: visible;
  }
  div.hover-highlight:hover {
    background-color: var(--panel-color-hover);
    opacity: var(--opacity-hover);
  }
</style>
