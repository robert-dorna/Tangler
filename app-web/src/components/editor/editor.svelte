<script>
  import { createEventDispatcher } from "svelte";
  import { displayConfig, displayConfigTypes, displayConfigAvailable } from "../../utils";
  import DragDropList from "../drag-drop-list.svelte";
  import IconButton from "../icon-button.svelte";
  import Icon from "../icon.svelte";
  import EditorButton from "./editor-button.svelte";
  import EditorItem from "./editor-item.svelte";
  import Menu from "../menu/menu.svelte";

  const dispatch = createEventDispatcher();

  export let what = "task";

  $: configs = $displayConfig.types;
  $: config = configs !== undefined && configs[what];
  $: fields = config !== undefined && config.fields;

  $: emojiOptions =
    $displayConfigAvailable &&
    $displayConfig.order.map((typeName) => ({
      emoji: $displayConfigTypes[typeName].emoji,
      text: typeName,
      action: () => dispatch("edit", { what: typeName }),
    }));
</script>

<div class="column elevated editor">
  <div class="row align flex">
    <div class="title">Fields editor</div>
    <Menu cls="row align clickable type-picker" options={emojiOptions} loseFocus>
      <Icon name="expanded" color="silver" size="medium" />
      {config.emoji}
      {what}
    </Menu>
    <IconButton name="pencil-outline" color="silver" size="medium" />
    <div class="row-reverse align flex">
      <EditorButton name="trash" color="silver" size="medium" text="Delete" on:click={() => alert("delete operation is not supported yet")} />
    </div>
  </div>
  {#if fields}
    <div class="column fields">
      <EditorItem legend />
      <DragDropList data={fields} let:item>
        <EditorItem field={item} />
      </DragDropList>
    </div>
  {/if}
  <div class="row align flex buttons">
    <EditorButton name="close" color="black" size="medium" text="Close" on:click={() => dispatch("discard")} />
    <EditorButton name="check" color="black" size="medium" text="Save" on:click={() => undefined} />
    <EditorButton name="eraser" color="black" size="medium" text="Clear changes" on:click={() => undefined} />
    <div class="flex" />
    <EditorButton name="eye-outline" color="black" size="medium" text="Preview (on)" on:click={() => undefined} />
  </div>
</div>

<style>
  .editor {
    background-color: var(--color-white);
    border-radius: var(--radius-large);
    padding: var(--gap-max);
    min-width: 40vw;
  }
  .title {
    font-size: var(--font-header);
    font-weight: bold;
    margin: var(--gap-medium);
  }
  :global(.type-picker) {
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
  .fields {
    margin-top: var(--gap-large);
    margin-bottom: var(--gap-large);
    gap: var(--gap-medium);
  }
  :global(.fields > .editor-item) {
    color: grey;
  }
  .buttons {
    flex-direction: row-reverse;
    padding-top: var(--gap-large);
    gap: var(--gap-large);
  }
</style>
