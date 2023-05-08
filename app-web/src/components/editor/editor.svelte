<script>
  import DragDropList from "../drag-drop-list.svelte";

  import Icon from "../icon.svelte";
  import Item from "./editor-item.svelte";
  import { displayConfig, displayConfigTypes } from "../../utils";

  import { createEventDispatcher } from "svelte";
  import IconButton from "../icon-button.svelte";

  const dispatch = createEventDispatcher();

  export let what = "task";

  $: configs = $displayConfig.types;
  $: config = configs !== undefined && configs[what];
  $: fields = config !== undefined && config.fields;
</script>

<div class="editor g-elevated">
  <div class="g-row-aligned g-flex">
    <div class="title">Fields editor</div>
    <div class="g-row-aligned header g-clickable">
      <Icon name="expanded" color="silver" size="medium" />
      {config.emoji}
      {what}
    </div>
    <IconButton cls="g-row-centered" name="pencil-outline" color="silver" size="medium" />
    <div class="g-row-aligned g-flex title-buttons">
      <div class="g-row-aligned button">
        <IconButton cls="g-row-centered" name="trash" color="silver" size="medium" />
        Delete
      </div>
    </div>
  </div>
  {#if fields}
    <div class="g-column fields">
      <Item legend />
      <DragDropList data={fields} let:item>
        <Item field={item} />
      </DragDropList>
    </div>
  {/if}
  <div class="g-row-flex-aligned buttons">
    <div class="g-row-aligned g-clickable button" on:click={() => dispatch("discard")} on:keypress={undefined}>
      <Icon name="close" color="black" size="medium" />
      Close
    </div>
    <div class="g-row-aligned g-clickable button">
      <Icon name="check" color="black" size="medium" />
      Save
    </div>
    <div class="g-row-aligned g-clickable button">
      <Icon name="eraser" color="black" size="medium" />
      Clear changes
    </div>
    <div class="g-flex" />
    <div class="g-row-aligned g-clickable button">
      <Icon name="eye-outline" color="black" size="medium" />
      Preview (on)
    </div>
  </div>
</div>

<style>
  div.editor {
    display: flex;
    flex-direction: column;
    background-color: var(--color-white);
    border-radius: var(--radius-large);
    padding: var(--gap-max);
    min-width: 40vw;
  }
  div.title {
    font-size: var(--font-header);
    font-weight: bold;
    margin: var(--gap-medium);
  }
  div.header {
    margin-left: var(--gap-max);
    margin-right: var(--gap-medium);
    padding: var(--gap-small);
    padding-left: var(--gap-small);
    padding-right: var(--gap-large);
    border-radius: var(--radius-large);
    border: 1px solid silver;
    font-size: var(--font-large);
    gap: var(--gap-tiny);
  }
  div.title-buttons {
    flex-direction: row-reverse;
  }
  div.fields {
    margin-top: var(--gap-large);
    margin-bottom: var(--gap-large);
    gap: var(--gap-medium);
  }
  div.buttons {
    flex-direction: row-reverse;
    padding-top: var(--gap-large);
    gap: var(--gap-large);
  }
  div.button {
    padding: var(--gap-small);
    padding-left: var(--gap-large);
    padding-right: var(--gap-large);
    border-radius: var(--radius-small);
    border: 1px solid silver;
    gap: var(--gap-small);
  }
</style>
