<script>
  import Icon from "../icon.svelte";
  import Item from "./editor-item.svelte";
  import { displayConfig, displayConfigTypes } from "../../utils";

  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  export let what = "task";

  $: configs = $displayConfig.types;
  $: config = configs !== undefined && configs[what];
  $: fields = config !== undefined && config.fields;
</script>

<div class="editor g-elevated">
  <div class="header">{config.emoji} {what}</div>
  {#if fields}
    <div class="g-column fields">
      <Item legend />
      {#each fields as field (field)}
        <Item {field} />
      {/each}
    </div>
  {/if}
  <div class="g-row-aligned g-clickable buttons" on:click={() => dispatch("discard")} on:keypress={undefined}>
    <Icon name="close" color="black" size="medium" />
    Discard
  </div>
</div>

<style>
  div.editor {
    display: flex;
    flex-direction: column;
    background-color: var(--color-mint-cream);
    border-radius: var(--radius-large);
    padding: var(--gap-max);
    min-width: 40vw;
  }
  div.header {
    font-size: var(--font-large);
    padding-bottom: var(--gap-large);
  }
  div.fields {
    margin-top: var(--gap-large);
    margin-bottom: var(--gap-large);
    gap: var(--gap-medium);
  }
  div.buttons {
    flex-direction: row-reverse;
    padding-top: var(--gap-large);
  }
</style>
