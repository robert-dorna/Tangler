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

  $: open = item._children.length ? true : undefined;

  function toggleOpen() {
    if (item._children.length) open = !open;
  }

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
  <Item item={newItem} {displayConfig} {indent} onConfirm={create} {options} />
{/if}

<Item {item} {displayConfig} {indent} {open} {toggleOpen} {options} />

{#if open}
  {#each item._children as child}
    <svelte:self item={child} {displayConfig} indent={indent + 32} />
  {/each}
{/if}

{#if createMode === CREATE_MODE.BELOW || createMode === CREATE_MODE.CHILD}
  <Item
    item={newItem}
    {displayConfig}
    indent={indent + (createMode === CREATE_MODE.CHILD ? 32 : 0)}
    onConfirm={create}
    {options}
  />
{/if}

{#if createMode}
  <Prompt onCreate={create} onDiscard={discard} />
{/if}
