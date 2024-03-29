<script>
  import Hovering from "../hovering.svelte";

  import Icon from "../icon.svelte";
  import Menu from "../menu/menu.svelte";

  import IconButton from "../icon-button.svelte";
  import IconSwitch from "../icon-switch.svelte";

  import Field from "./item-field.svelte";
  import Options from "./item-options.svelte";

  import {
    config as latestConfig,
    itemsLoaded,
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

  function toggleOpen() {
    dispatch("toggleOpen");
  }

  function createBody() {
    item.body = "enter body text here.";
    detailed = true;
  }

  $: if (item.body === undefined || item.body === null) {
    item.body = "";
  }

  let config = $latestConfig;
  $: if ($itemsLoaded) config = $latestConfig;

  // $: typeConfig = console.log("updating typeConfig!") || $config.types[item._what];
  $: typeConfig = config.types[item._what];

  // console.log("rendering item ", item._what);
  // console.log({ item, typeConfig, what: item._what, config: $config, space: $space });

  $: isMoving =
    $movingItem !== null &&
    $movingItem.what === item._what &&
    $movingItem._id === item._id;
  $: isNewItem = item._id === "new";
  $: isElevated = isNewItem || isMoving;

  $: chevronColor = hover ? "#8A817C" : "#BCB8B1";
  $: if (!hover) editing = false;

  $: emojiOptions = config.order.map((typeName) => ({
    emoji: config.types[typeName].emoji,
    text: typeName,
    action: () => {
      item._what = typeName;
    },
  }));
</script>

<Hovering
  cls="column clickable item"
  elevated={isElevated}
  bind:hover
  on:click={toggleOpen}
>
  <div class="row flex align wrap-reverse item-fields">
    <div style="width: {indent}px;" />
    <Icon
      name={open === undefined ? "dot" : open ? "expanded" : "expand"}
      color={chevronColor}
      size="large"
    />

    {#if isNewItem}
      <Menu cls="emoji" options={emojiOptions} bind:focus={editing}>
        <span class="row center emoji-button"> {typeConfig.emoji} </span>
      </Menu>
    {:else}
      <span class="emoji"> {typeConfig.emoji} </span>
    {/if}

    {#each typeConfig.fields as field (field.name)}
      {#if field.width !== false}
        <Field {...field} {item} bind:editing on:refresh>
          {#if field.name === "title"}
            {#if item.body}
              <IconSwitch
                nameOn="dots"
                nameOff="dots-h"
                color="darkgoldenrod"
                size="medium"
                bind:toggled={detailed}
              />
            {:else}
              <IconButton
                name="pencil-plus"
                color="darkgoldenrod"
                size="medium"
                hidden={!hover}
                on:click={createBody}
              />
            {/if}
          {/if}
        </Field>
      {/if}
    {/each}

    {#if isNewItem}
      <IconButton
        name="check"
        color="grey"
        size="large"
        on:click={() => dispatch("create")}
      />
    {:else}
      <Menu
        cls="row center"
        hide={!hover || $newItem.anchor.id !== null}
        bind:focus={editing}
        {options}
      >
        <Icon name="dots-v" color="grey" size="large" />
      </Menu>
    {/if}
  </div>
  {#if item.body && detailed}
    <Field
      style="margin-left: {indent + 80}px;"
      name="body"
      {item}
      bind:editing
      on:refresh
    />
  {/if}
</Hovering>

<Options {item} bind:options on:refresh />

<style>
  :global(.item) {
    width: 100%;
    max-width: var(--item-width);
    border-radius: var(--radius-small);
    margin: var(--gap-tiny);
    font-size: var(--font-large);
  }
  :global(.item:hover) {
    background-color: var(--color-anti-flash-white);
  }

  :global(.item-fields > .emoji) {
    margin-left: var(--gap-small);
    margin-right: var(--gap-medium);
  }

  .emoji-button {
    margin-right: var(--gap-small);
    padding: var(--gap-small);
    border-radius: var(--radius-small);
  }
  .emoji-button:hover {
    background-color: var(--color-silver);
  }

  :global(.field > .icon-button) {
    padding: var(--gap-small);
  }

  :global(.field > .icon-button:hover) {
    border-radius: var(--radius-small);
    background-color: var(--color-silver);
  }

  :global(.field > .icon-switch) {
    /* prettier-ignore */
    padding-left: 
      var(--icon-switch-is-on, inherit)
      var(--icon-switch-is-off, var(--gap-small));

    /* prettier-ignore */
    padding-right:
      var(--icon-switch-is-on, inherit)
      var(--icon-switch-is-off, var(--gap-small));
  }

  :global(.item-fields > .icon-button) {
    padding: var(--gap-small);
    margin-left: var(--gap-large);
  }
  :global(.item-fields > .icon-button:hover) {
    border-radius: var(--radius-small);
    background-color: var(--color-silver);
  }

  :global(.item-fields > .menu:last-child) {
    padding: var(--gap-small);
    border-radius: var(--radius-small);

    /* prettier-ignore */
    background-color:
      var(--menu-is-visible, var(--color-silver))
      var(--menu-is-not-visible, inherit);
  }
  :global(.item-fields > .menu:last-child:hover) {
    background-color: var(--color-silver);
  }

  :global(.item > .field) {
    padding-top: var(--gap-small);
    padding-left: var(--gap-medium);
    padding-right: var(--gap-medium);
    padding-bottom: var(--gap-small);
    margin-bottom: var(--gap-medium);
    color: darkgoldenrod;
    max-width: 40vw;
  }
</style>
