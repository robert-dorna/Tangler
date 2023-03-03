<script>
  import Item from "./item.svelte";

  import Prompt from "./prompt.svelte";

  import HandIcon from "svelte-material-icons/HandFrontLeftOutline.svelte";
  import UpIcon from "svelte-material-icons/MenuUpOutline.svelte";
  import DownIcon from "svelte-material-icons/MenuDownOutline.svelte";
  import TreeIcon from "svelte-material-icons/FileTree.svelte";
  import TopIcon from "svelte-material-icons/FormatVerticalAlignTop.svelte";
  import TrashIcon from "svelte-material-icons/DeleteForeverOutline.svelte";

  export let item;
  export let displayConfig = {};
  export let indent = 0;

  $: children = item._children;
  $: len = children.length;
  $: open = len > 0 ? true : undefined;

  // NOTE
  // with such definition of open
  //
  //   let open = undefined;
  //
  // this will work
  //
  //   $: if (len > 0) { open = true; }
  //
  // but this not, correctly evaluating open at init but then value is blocked
  //
  //   $: if (item._children.length > 0) {
  //     open = true;
  //   }

  const CREATE_MODE = Object.freeze({
    ABOVE: 1,
    BELOW: 2,
    CHILD: 3,
  });

  let createMode = false;

  // prettier-ignore
  const options = [
    { Icon: HandIcon,   text: "move",          action: () => { alert("TODO: move"); } },
    { Icon: UpIcon,     text: "create above",  action: () => { createMode = CREATE_MODE.ABOVE; } },
    { Icon: DownIcon,   text: "create below",  action: () => { createMode = CREATE_MODE.BELOW; } },
    { Icon: TreeIcon,   text: "create child",  action: () => { createMode = CREATE_MODE.CHILD; } },
    { Icon: TopIcon,    text: "detach top",    action: () => { alert("TODO: detach"); } },
    { Icon: TrashIcon,  text: "delete",        action: () => { alert("TODO: delete"); } },
  ];

  function create(item) {
    alert("create: " + JSON.stringify(item));
    discard();
  }

  function discard() {
    createMode = false;
  }

  const newItem = { _children: [], _what: "account", title: "new item" };
</script>

{#if createMode === CREATE_MODE.ABOVE}
  <Item item={newItem} {displayConfig} {indent} options={create} />
{/if}

<Item {item} {displayConfig} {indent} {options} bind:open />

{#if open}
  {#each item._children as child (child._id)}
    <svelte:self item={child} {displayConfig} indent={indent + 32} />
  {/each}
{/if}

{#if createMode === CREATE_MODE.BELOW || createMode === CREATE_MODE.CHILD}
  <Item
    item={newItem}
    {displayConfig}
    indent={indent + (createMode === CREATE_MODE.CHILD ? 32 : 0)}
    options={create}
  />
{/if}

{#if createMode}
  <Prompt on:create={create} on:discard={discard} />
{/if}
