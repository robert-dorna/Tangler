<script>
  import HoverPad from "../utils/hoverpad.svelte";

  import ExpandButton from "./buttons/expand-button.svelte";
  import EmojiButton from "./buttons/emoji-button.svelte";
  import DetailsToggle from "./buttons/details-toggle.svelte";
  import DetailsButton from "./buttons/details-button.svelte";
  import ConfirmButton from "./buttons/confirm-button.svelte";
  import OptionsButton from "./buttons/options-button.svelte";

  import Field from "./field.svelte";
  import Options from "./options.svelte";

  import { displayConfigTypes, newItem, movingItem } from "../stores";

  export let item = newItem.plain;
  export let indent = 0;
  export let open = undefined;

  let hover = false;
  let editing = false;
  let detailed = false;

  let options;

  let v = item._what;

  function toggleOpen() {
    if (open !== undefined) open = !open;
  }

  function createBody() {
    item.body = "enter body text here.";
    detailed = true;
  }

  $: if (item.body === undefined || item.body === null) {
    item.body = "";
  }

  $: item._what = v;

  $: what = item._what;
  $: layout = $displayConfigTypes[what];
  $: fields = layout.fields;

  $: creatingNewItem = item === newItem.plain;

  $: elevated =
    creatingNewItem ||
    ($movingItem !== null &&
      $movingItem.what === item._what &&
      $movingItem._id === item._id);

  $: chevronColor = hover ? "#8A817C" : "#BCB8B1";
  $: if (!hover) editing = false;

  $: showOptions = Boolean($newItem.anchorId === null) && hover;

  const bodyStyleConst =
    "padding-top: 5px; padding-left: 10px; padding-right: 10px; padding-bottom: 5px; margin-bottom: 10px; color: darkgoldenrod; max-width: 40vw;";

  $: bodyStyle = `margin-left: ${indent + 80}px; ${bodyStyleConst}`;
</script>

<div class="container" class:elevated>
  <HoverPad bind:hover on:click={toggleOpen}>
    <div class="fields">
      <div class="indent" style="width: {indent}px;" />
      <ExpandButton expanded={open} color={chevronColor} />

      {#if creatingNewItem}
        <EmojiButton bind:value={v} {item} bind:editing />
      {:else}
        <span class="emoji"> {layout.emoji} </span>
      {/if}

      {#each fields as field (field.name)}
        <Field {...field} {item} bind:editing on:refresh>
          {#if field.name === "title"}
            {#if item.body}
              <DetailsToggle bind:detailed />
            {:else}
              <DetailsButton visible={hover} on:click={createBody} />
            {/if}
          {/if}
        </Field>
      {/each}

      {#if creatingNewItem}
        <ConfirmButton on:click={() => options(item)} />
      {:else}
        <OptionsButton visible={showOptions} bind:editing {options} />
      {/if}
    </div>
    {#if item.body && detailed}
      <Field name="body" {item} bind:editing style={bodyStyle} on:refresh />
    {/if}
  </HoverPad>
</div>

<Options {item} bind:options />

<!-- removing padding gives nice compact view -->
<style>
  div.container {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 65vw;
    border-radius: 8px;
    margin: 3px;
    user-select: none;
    cursor: pointer;
    font-size: 22px;
  }
  div.container:hover {
    background-color: #eef0f2;
  }
  div.elevated {
    box-shadow: 8px 8px 24px 0px rgba(66, 68, 90, 1);
  }
  div.fields {
    display: flex;
    flex: 1;
    flex-wrap: wrap-reverse;
    flex-direction: row;
    align-items: center;
    /* padding: 15px; */
  }
  span.emoji {
    margin-left: 5px;
    margin-right: 10px;
  }
</style>
