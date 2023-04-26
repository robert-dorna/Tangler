<script>
  import Hovering from "../hovering.svelte";

  import Icon from "../icon.svelte";
  import Menu from "../menu/menu.svelte";

  import DetailsToggle from "./buttons/details-toggle.svelte";
  import DetailsButton from "./buttons/details.svelte";
  import ConfirmButton from "./buttons/confirm.svelte";

  import Field from "./item-field.svelte";
  import Options from "./item-options.svelte";

  import {
    displayConfig,
    displayConfigTypes,
    newItem,
    movingItem,
  } from "../../utils";

  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  export let item;
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

  $: creatingNewItem = item._id === "new";

  $: elevated =
    creatingNewItem ||
    ($movingItem !== null &&
      $movingItem.what === item._what &&
      $movingItem._id === item._id);

  $: chevronColor = hover ? "#8A817C" : "#BCB8B1";
  $: if (!hover) editing = false;

  const bodyStyleConst =
    "padding-top: 5px; padding-left: 10px; padding-right: 10px; padding-bottom: 5px; margin-bottom: 10px; color: darkgoldenrod; max-width: 40vw;";

  $: bodyStyle = `margin-left: ${indent + 80}px; ${bodyStyleConst}`;

  const emojiOptions = $displayConfig.order.map((typeName) => ({
    emoji: $displayConfigTypes[typeName].emoji,
    text: typeName,
    action: () => (v = typeName),
  }));
</script>

<Hovering
  cls="g-column g-item-container g-clickable"
  {elevated}
  bind:hover
  on:click={toggleOpen}
>
  <div class="g-row-flex-aligned fields">
    <div class="indent" style="width: {indent}px;" />
    <Icon
      name={open === undefined ? "dot" : open ? "expanded" : "expand"}
      color={chevronColor}
      size={30}
    />

    {#if creatingNewItem}
      <Menu cls="g-item-emoji-menu" options={emojiOptions} bind:focus={editing}>
        <span class="g-row-centered emoji-button"> {layout.emoji} </span>
      </Menu>
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
      <ConfirmButton on:click={() => dispatch("create")} />
    {:else}
      <Menu
        cls="g-row-centered g-item-menu-container"
        hide={!hover || $newItem.anchorId !== null}
        bind:focus={editing}
        {options}
      >
        <Icon name="dots-v" color="grey" size={30} />
      </Menu>
    {/if}
  </div>
  {#if item.body && detailed}
    <Field name="body" {item} bind:editing style={bodyStyle} on:refresh />
  {/if}
</Hovering>

<Options {item} bind:options on:refresh />

<style>
  :global(div.g-item-container) {
    width: 100%;
    max-width: var(--item-width);
    border-radius: var(--radius-small);
    margin: var(--gap-tiny);
    font-size: var(--font-large);
  }
  :global(div.g-item-container:hover) {
    background-color: var(--color-anti-flash-white);
  }

  div.fields {
    flex-wrap: wrap-reverse;
  }
  span.emoji {
    margin-left: var(--gap-small);
    margin-right: var(--gap-medium);
  }
  span.emoji-button {
    margin-right: var(--gap-small);
    padding: var(--gap-small);
    border-radius: var(--radius-small);
  }
  span.emoji-button:hover {
    background-color: var(--color-silver);
  }

  :global(div.g-item-emoji-menu) {
    margin-left: var(--gap-small);
    margin-right: var(--gap-medium);
  }

  /* Menu styles */

  :global(div.g-item-menu-container) {
    padding: var(--gap-small);
    border-radius: var(--radius-small);

    /* prettier-ignore */
    background-color:
      var(--menu-is-visible, var(--color-silver))
      var(--menu-is-not-visible, inherit);
  }
  :global(div.g-item-menu-container:hover) {
    background-color: var(--color-silver);
  }
</style>
