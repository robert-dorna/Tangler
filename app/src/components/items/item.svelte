<script>
  import Hovering from "../../components/hovering.svelte";


  import Icon from "../../components/icon.svelte";
  import Menu from "../menu/menu.svelte";

  import DetailsToggle from "./buttons/details-toggle.svelte";
  import DetailsButton from "./buttons/details.svelte";
  import ConfirmButton from "./buttons/confirm.svelte";

  import Field from "./field.svelte";
  import Options from "./options.svelte";

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

<Hovering cls="g-item-container" {elevated} bind:hover on:click={toggleOpen}>
  <div class="fields">
    <div class="indent" style="width: {indent}px;" />
    <Icon
      name={open === undefined ? "dot" : open ? "expanded" : "expand"}
      color={chevronColor}
      size={30}
    />

    {#if creatingNewItem}
      <Menu cls="g-item-emoji-menu" options={emojiOptions} bind:focus={editing}>
        <span class="emoji-button"> {layout.emoji} </span>
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
      <ConfirmButton on:click={() => dispatch('create')} />
    {:else}
      <Menu
        cls="g-item-menu-container"
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

<!-- removing padding gives nice compact view -->
<style>
  :global(div.g-item-container) {
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
  :global(div.g-item-container:hover) {
    background-color: #eef0f2;
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
  span.emoji-button {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-right: 5px;
    padding: 5px;
    border-radius: 8px;
  }
  span.emoji-button:hover {
    background-color: #bcb8b1;
  }
  /* to bylo w emoji menu container */
  /* :global(div.g-emoji-container) {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-right: 5px;
    padding: 5px;
  }
  :global(div.g-emoji-container:hover) {
    border-radius: 8px;
    background-color: #bcb8b1;
  } */

  :global(div.g-item-emoji-menu) {
    margin-left: 5px;
    margin-right: 10px;
  }

  /* Menu styles */

  :global(div.g-item-menu-container) {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 5px;
    border-radius: 8px;

    /* TODO: this is global and will fuck up other menus? */
    background-color: var(--menu-is-visible, var(--color-silver))
      var(--menu-is-not-visible, inherit);
  }
  :global(div.g-item-menu-container:hover) {
    background-color: var(--color-silver);
  }
</style>
