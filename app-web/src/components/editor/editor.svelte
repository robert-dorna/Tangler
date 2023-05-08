<script>
  import DragDropList from "../drag-drop-list.svelte";
  import Button from "./editor-button.svelte";

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

<div class="column editor elevated">
  <div class="row align flex">
    <div class="title">Fields editor</div>
    <div class="row align header clickable">
      <Icon name="expanded" color="silver" size="medium" />
      {config.emoji}
      {what}
    </div>
    <IconButton cls="row center" name="pencil-outline" color="silver" size="medium" />
    <div class="row-reverse align flex">
      <Button name="trash" color="silver" size="medium" text="Delete" on:click={() => alert('delete operation is not supported yet')}/>
    </div>
  </div>
  {#if fields}
    <div class="column fields">
      <Item legend />
      <DragDropList data={fields} let:item>
        <Item field={item} />
      </DragDropList>
    </div>
  {/if}
  <div class="row align flex buttons">
    <Button name="close" color="black" size="medium" text="Close" on:click={() => dispatch("discard")}/>
    <Button name="check" color="black" size="medium" text="Save" on:click={() => undefined}/>
    <Button name="eraser" color="black" size="medium" text="Clear changes" on:click={() => undefined}/>
    <div class="flex" />
    <Button name="eye-outline" color="black" size="medium" text="Preview (on)" on:click={() => undefined}/>
  </div>
</div>

<style>
  div.editor {
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
</style>
