<script>
  import { createEventDispatcher } from "svelte";
  import { client, displayConfig, displayConfigAvailable, displayConfigTypes } from "../../utils";
  import DragDropList from "../drag-drop-list.svelte";
  import IconButton from "../icon-button.svelte";
  import Icon from "../icon.svelte";
  import Menu from "../menu/menu.svelte";
  import EditorButton from "./editor-button.svelte";
  import EditorItem from "./editor-item.svelte";
  import EditorTypeEditor from "./editor-type-editor.svelte";

  const dispatch = createEventDispatcher();

  export let what;

  let editingTypeName = false;

  function switchTypeNameEditing() {
    editingTypeName = !editingTypeName;
  }

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

  $: emoji = config.emoji;
  $: name = what;

  function onRename(event) {
    console.log("saving config: ", event.detail);
    emoji = event.detail.emoji;
    name = event.detail.what;
    editingTypeName = false;
  }

  function onSave() {
    if (emoji !== config.emoji && name === what) {
      client.oldapi.patchConfig({
        target: "emoji",
        type_name: what,
        new_value: emoji,
      });
    } else if (name !== what) {
      let new_value = { name };
      if (emoji !== config.emoji) {
        new_value.emoji = emoji;
      }
      client.oldapi.patchConfig({
        target: "name",
        type_name: what,
        new_value,
      });
    }
    dispatch('refresh')
  }
</script>

<div class="column elevated editor">
  <div class="row align flex">
    <div class="title">Fields editor</div>
    {#if editingTypeName}
      <EditorTypeEditor cls="row align type-picker" {emoji} what={name} on:save={onRename} on:close={switchTypeNameEditing} />
    {:else}
      <Menu cls="row align clickable type-picker" options={emojiOptions} loseFocus>
        <Icon name="expanded" color="silver" size="medium" />
        {emoji}
        {name}
      </Menu>
      <IconButton name="pencil-outline" color="silver" size="medium" on:click={switchTypeNameEditing} />
    {/if}
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
    <EditorButton name="check" color="black" size="medium" text="Save" on:click={onSave} />
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
