<script>
  import Item from "./item.svelte";

  import Prompt from "./prompt.svelte";

  import HandIcon from "svelte-material-icons/HandFrontLeftOutline.svelte";
  import UpIcon from "svelte-material-icons/MenuUpOutline.svelte";
  import DownIcon from "svelte-material-icons/MenuDownOutline.svelte";
  import TreeIcon from "svelte-material-icons/FileTree.svelte";
  import TopIcon from "svelte-material-icons/FormatVerticalAlignTop.svelte";
  import TrashIcon from "svelte-material-icons/DeleteForeverOutline.svelte";

  import { createEventDispatcher } from "svelte";

  import client from "./client";

  const dispatch = createEventDispatcher();

  export let item;
  export let displayConfig = {};
  export let indent = 0;
  export let enableOptions = true;

  const CREATE_MODE = Object.freeze({
    ABOVE: 1,
    BELOW: 2,
    CHILD: 3,
  });

  let createMode = false;

  function handleDelete() {
    client
      .get({ method: "delete", what: item["_what"], _id: item["_id"] })
      .then(() => dispatch("refresh"))
      .catch(() => alert("error on delete"));
  }

  // prettier-ignore
  const options = [
    { Icon: HandIcon,   text: "move",          action: () => { alert("TODO: move"); } },
    { Icon: UpIcon,     text: "create above",  action: () => { createMode = CREATE_MODE.ABOVE; } },
    { Icon: DownIcon,   text: "create below",  action: () => { createMode = CREATE_MODE.BELOW; } },
    { Icon: TreeIcon,   text: "create child",  action: () => { createMode = CREATE_MODE.CHILD; } },
    { Icon: TopIcon,    text: "detach top",    action: () => { alert("TODO: detach"); } },
    { Icon: TrashIcon,  text: "delete",        action: handleDelete },
  ];

  function create(fields) {
    // alert("create: " + JSON.stringify(fields));
    client
      .create({ ...fields, _aboveId: item["_id"], _aboveWhat: item["_what"] })
      .then(() => {
        dispatch("refresh");
        discard();
      });
  }

  function discard() {
    createMode = false;
  }

  $: enableOptions = Boolean(createMode == false);

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

  $: children = item._children;
  $: len = children.length;
  $: open = len > 0 ? true : undefined;

  const newItem = { _children: [], _what: item["_what"], title: "new item" };
</script>

{#if createMode === CREATE_MODE.ABOVE}
  <Item item={newItem} {displayConfig} {indent} options={create} />
{/if}

<Item
  {item}
  {displayConfig}
  {indent}
  {options}
  bind:open
  {enableOptions}
  on:refresh
/>

{#if open}
  {#each item._children as child (child._id)}
    <svelte:self
      item={child}
      {displayConfig}
      indent={indent + 32}
      bind:enableOptions
      on:refresh
    />
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
