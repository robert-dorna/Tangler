<script>
  import ExpandIconButton from "./buttons/expand-icon-button.svelte";
  import DetailsIconButton from "./buttons/details-icon-button.svelte";
  import DetailsAddIconButton from "./buttons/details-add-icon-button.svelte";
  import OptionsIconButton from "./buttons/options-icon-button.svelte";
  import NewItemIconsButton from "./buttons/new-item-icons-button.svelte";
  import EmojiIconButton from "./buttons/emoji-icon-button.svelte";
  import Field from "./field.svelte";

  export let item;
  export let displayConfig = {};
  export let indent = 0;
  export let options;
  export let open = undefined;

  function toggleOpen() {
    if (open !== undefined) open = !open;
  }

  let hover = false;
  let editing = false;
  let detailed = false;

  function hoverOn() {
    if (!hover) hover = true;
  }

  function hoverOff() {
    if (hover) hover = false;
  }

  $: gotConfirmOption = typeof options === "function";
  $: layout = displayConfig.types[item["_what"]];
  $: workingItem = { body: "", ...item };
  $: chevronColor = hover ? "#8A817C" : "#BCB8B1";
  $: if (!hover) editing = false;

  function createBody() {
    workingItem.body = "enter body text here.";
    detailed = true;
  }

  const bodyStyle =
    "padding-top: 5px; padding-left: 10px; padding-right: 10px; padding-bottom: 5px; margin-bottom: 10px; color: darkgoldenrod; max-width: 40vw;";
</script>

<div
  class="container {gotConfirmOption ? 'elevated' : ''}"
  on:click|self={toggleOpen}
  on:keypress={undefined}
  on:mouseenter={hoverOn}
  on:mouseleave={hoverOff}
>
  <div class="fields" on:click|self={toggleOpen} on:keypress={undefined}>
    <div class="indent" style="width: {indent}px;" />
    <ExpandIconButton
      expanded={open}
      color={chevronColor}
      size={30}
      on:click={toggleOpen}
    />
    {#if gotConfirmOption}
      <EmojiIconButton bind:item={workingItem} {displayConfig} />
    {:else}
      <span class="emoji" on:click={toggleOpen} on:keypress={undefined}>
        {layout.emoji}
      </span>
    {/if}

    {#each layout.fields as field (field)}
      <Field {...field} item={workingItem} bind:editing on:click={toggleOpen}>
        {#if field.name === "title"}
          {#if workingItem.body}
            <DetailsIconButton
              bind:detailed
              color="darkgoldenrod"
              hoverColor="brown"
              size={24}
            />
          {:else}
            <DetailsAddIconButton
              visible={hover}
              color="darkgoldenrod"
              hoverColor="brown"
              size={24}
              on:click={createBody}
            />
          {/if}
        {/if}
      </Field>
    {/each}
    {#if gotConfirmOption}
      <NewItemIconsButton on:click={() => options(workingItem)} />
    {:else}
      <OptionsIconButton visible={hover} bind:editing {options} />
    {/if}
  </div>
  {#if workingItem.body && detailed}
    <Field
      name="body"
      item={workingItem}
      bind:editing
      style="margin-left: {indent + 80}px; {bodyStyle}"
    />
  {/if}
</div>

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
    padding: 15px;
  }
  span.emoji {
    margin-right: 10px;
  }
</style>
