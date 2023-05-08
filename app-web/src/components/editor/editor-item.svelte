<script>
  import Hovering from "../hovering.svelte";
  import Icon from "../icon.svelte";
  import Values from "./editor-item-values.svelte";

  import Field from "./editor-item-field.svelte";

  export let field;
  export let legend = false;

  let hover;

  $: hoverClass = legend || !hover ? "" : "l-hover";
  $: isEnum = field !== undefined && typeof field.values === "object";
</script>

<!-- <Hovering cls="g-column g-flex l-field {legend ? 'l-legend' : ''} g-clickable {hoverClass}" bind:hover> -->
<div class="qq-column qq-flex l-field {legend ? 'l-legend' : ''} g-clickable {hoverClass}">
  <div class="qq-row qq-center qq-flex">
    <div class="qq-row qq-center icon" class:g-hidden={legend}>
      <Icon name="dot" color="black" size="small" />
    </div>
    <Field>{legend ? "name" : field.name}</Field>
    <Field>{legend ? "width" : field.width} {!legend && field.width === 0 ? "(expanded)" : ""}</Field>
    <Field>{legend ? "values" : isEnum ? "one of given values" : field.values}</Field>
    <div class="qq-row qq-center icon" class:g-hidden={legend || !hover}>
      <Icon name="hand-outline" color="black" size="small" />
    </div>
  </div>
  {#if isEnum}
    <Values values={field.values} />
  {/if}
</div>
<!-- </Hovering> -->

<style>
  :global(div.l-field) {
    padding-top: var(--gap-small);
    padding-bottom: var(--gap-small);
    border-radius: var(--radius-small);
  }
  :global(div.l-legend) {
    color: grey;
  }
  :global(div.l-hover) {
    background-color: var(--color-tea-green);
  }
  div.icon {
    margin-left: var(--gap-medium);
    margin-right: var(--gap-medium);
  }
</style>
