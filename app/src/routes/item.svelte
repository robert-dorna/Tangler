<script>
  import ExpandIconButton from "./item/expand-icon-button.svelte";
  import DetailsIconButton from "./item/details-icon-button.svelte";
  import DetailsAddIconButton from "./item/details-add-icon-button.svelte";
  import OptionsIconButton from "./item/options-icon-button.svelte";
  import NewItemIconsButton from "./item/new-item-icons-button.svelte";
  import Prompt from "./prompt.svelte";
  import Field from "./field.svelte";

  import Detach from "svelte-material-icons/FormatVerticalAlignTop.svelte";
  import Move from "svelte-material-icons/HandFrontLeftOutline.svelte";
  import CreateAbove from "svelte-material-icons/MenuUpOutline.svelte";
  import CreateBelow from "svelte-material-icons/MenuDownOutline.svelte";
  import CreateChild from "svelte-material-icons/FileTree.svelte";
  import Delete from "svelte-material-icons/DeleteForeverOutline.svelte";

  export let item;
  export let displayConfig = {};
  export let indent = 0;

  export let marked = false;
  export let onConfirm;

  $: layout = displayConfig[item["_what"]];
  $: children = item["_children"];
  $: hasChildren = children.length;
  $: open = hasChildren ? true : undefined;

  function toggleOpen() {
    if (hasChildren) open = !open;
  }

  let hover = false;

  function hoverOn() {
    if (!hover) hover = true;
  }
  function hoverOff() {
    if (hover) hover = false;
  }

  $: chevronColor = hover ? "#8A817C" : "#BCB8B1";

  let detailed = false;
  let editing = undefined;

  const CREATE_MODE = Object.freeze({
    ABOVE: 1,
    BELOW: 2,
    CHILD: 3,
  });

  let createMode = false;

  $: workingItem = { ...item };

  const options = [
    {
      Icon: Move,
      text: "move",
      action: () => {
        alert("move");
      },
    },
    {
      Icon: CreateAbove,
      text: "create above",
      action: () => {
        createMode = CREATE_MODE.ABOVE;
      },
    },
    {
      Icon: CreateBelow,
      text: "create below",
      action: () => {
        alert("below");
      },
    },
    {
      Icon: CreateChild,
      text: "create child",
      action: () => {
        alert("child");
      },
    },
    {
      Icon: Detach,
      text: "detach top",
      action: () => {
        alert("detach");
      },
    },
    {
      Icon: Delete,
      text: "delete",
      action: () => {
        alert("delete");
      },
    },
  ];

  function create(item) {
    alert("create: " + JSON.stringify(item));
    discard();
  }

  function discard() {
    createMode = false;
  }

  function createBody() {
    workingItem.body = "enter body text here.";
    detailed = true;
  }

  $: hasBody = "body" in workingItem && workingItem.body;

  const bodyStyle = "padding-top: 5px; padding-left: 10px; padding-right: 10px; padding-bottom: 5px; margin-bottom: 10px; color: darkgoldenrod; max-width: 40vw;"
</script>

{#if createMode === CREATE_MODE.ABOVE}
  <svelte:self
    item={{ _children: [], _what: "account", title: "new item" }}
    {displayConfig}
    {indent}
    marked
    onConfirm={create}
  />
{/if}
<div
  class="container {marked ? 'mark' : ''}"
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
    {#if marked}
      <NewItemIconsButton on:click={() => onConfirm(workingItem)} />
    {:else}
      <OptionsIconButton visible={hover} {options} />
    {/if}
  </div>
  {#if hasBody && detailed}
    <Field name="body" item={workingItem} {editing} style="margin-left: {indent + 80}px; {bodyStyle}"/>
  {/if}
</div>

{#if open}
  {#each children as child}
    <svelte:self item={child} {displayConfig} indent={indent + 32} />
  {/each}
{/if}

{#if createMode}
  <Prompt onCreate={create} onDiscard={discard} />
{/if}

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
  div.mark {
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
