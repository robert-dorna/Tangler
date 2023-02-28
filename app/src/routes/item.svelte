<script>
  import ExpandIconButton from "./item/expand-icon-button.svelte";
  import DetailsIconButton from "./item/details-icon-button.svelte";
  import DetailsAddIconButton from "./item/details-add-icon-button.svelte";
  import OptionsIconButton from "./item/options-icon-button.svelte";
  import NewItemIconsButton from "./item/new-item-icons-button.svelte";
  import Field from "./field.svelte";

  export let item;
  export let displayConfig = {};
  export let indent = 0;

  export let open = undefined;
  export let toggleOpen = undefined;

  export let onConfirm = undefined;

  export let options;

  $: layout = displayConfig[item["_what"]];

  let editing = undefined;

  let hover = false;

  function hoverOn() {
    if (!hover) hover = true;
  }
  function hoverOff() {
    if (hover) hover = false;
  }

  let detailed = false;

  $: chevronColor = hover ? "#8A817C" : "#BCB8B1";
  $: workingItem = { ...item };
  $: hasBody = "body" in workingItem && workingItem.body;

  function createBody() {
    workingItem.body = "enter body text here.";
    detailed = true;
  }

  const bodyStyle =
    "padding-top: 5px; padding-left: 10px; padding-right: 10px; padding-bottom: 5px; margin-bottom: 10px; color: darkgoldenrod; max-width: 40vw;";
</script>

<div
  class="container {onConfirm ? 'elevated' : ''}"
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
    <span class="emoji" on:click={toggleOpen} on:keypress={undefined}>
      {layout.emoji}
    </span>

    {#each layout.fields as field (field)}
      <Field {...field} bind:item={workingItem} {editing} on:click={toggleOpen}>
        {#if field.name === "title"}
          {#if hasBody}
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
    {#if onConfirm}
      <NewItemIconsButton on:click={() => onConfirm(workingItem)} />
    {:else}
      <OptionsIconButton visible={hover} {options} />
    {/if}
  </div>
  {#if hasBody && detailed}
    <Field
      name="body"
      item={workingItem}
      {editing}
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
    opacity: 80%;
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
