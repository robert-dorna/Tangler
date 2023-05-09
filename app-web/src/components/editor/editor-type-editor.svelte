<script>
  import { createEventDispatcher } from "svelte";
  import IconButton from "../icon-button.svelte";
  import EmojiSelector from "../emoji-selector.svelte";
  import Tooltip from "../tooltip.svelte";

  const dispatch = createEventDispatcher();

  export let cls = "";
  export let emoji;
  export let what;

  let whatInput = null;

  let emojiSelectorFocus = null;
  function onEmoji(event) {
    emoji = event.detail;
    emojiSelectorFocus = null;
  }
</script>

<div class="editor-type-editor {cls}">
  <Tooltip bind:focus={emojiSelectorFocus} loseFocus>
    {emoji}
    <div slot="tooltip" class="column floating-menu elevated emoji-picker" let:menuPosition style={menuPosition}>
      <EmojiSelector on:emoji={onEmoji} />
    </div>
  </Tooltip>
  <div class="spacer" />
  <input
    bind:this={whatInput}
    style="width: {what.length / 2 + 1}em;"
    maxlength="16"
    type="text"
    bind:value={what}
    on:click|stopPropagation={() => undefined}
  />
</div>
<IconButton name="check" color="silver" size="medium" on:click={() => dispatch("save", { emoji, what })} />
<IconButton name="close" color="silver" size="medium" on:click={() => dispatch("close")} />

<style>
  .editor-type-editor {
    padding-left: var(--gap-large);
  }
  input {
    all: unset;
    /* background-color: brown; */
  }
  .spacer {
    width: var(--gap-line);
    height: 30px;
    margin-left: var(--gap-medium);
    margin-right: var(--gap-medium);
    background-color: var(--color-silver);
  }
</style>
