<script>
  import Icon from "../icon.svelte";
  import EditorItemField from "./editor-item-field.svelte";
  import EditorItemValues from "./editor-item-values.svelte";

  export let field;
  export let legend = false;

  $: isEnum = field !== undefined && typeof field.values === "object";
</script>

<div class="column flex clickable editor-item">
  <div class="row center flex">
    <div class="row center icon" class:hidden={legend}>
      <Icon name="dot" color="black" size="small" />
    </div>
    <EditorItemField>{legend ? "name" : field.name}</EditorItemField>
    <EditorItemField>{legend ? "width" : field.width} {!legend && field.width === 0 ? "(expanded)" : ""}</EditorItemField>
    <EditorItemField>{legend ? "values" : isEnum ? "one of given values" : field.values}</EditorItemField>
    <div class="icon" />
  </div>
  {#if isEnum}
    <EditorItemValues values={field.values} />
  {/if}
</div>

<style>
  .editor-item {
    padding-top: var(--gap-small);
    padding-bottom: var(--gap-small);
    border-radius: var(--radius-small);
  }
  .icon {
    margin-left: var(--gap-medium);
    margin-right: var(--gap-medium);
  }
</style>
