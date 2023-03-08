<script>
  import Item from "./item.svelte";

  import Prompt from "./prompt.svelte";

  // options
  import HandIcon from "svelte-material-icons/HandFrontLeftOutline.svelte";
  import UpIcon from "svelte-material-icons/MenuUpOutline.svelte";
  import DownIcon from "svelte-material-icons/MenuDownOutline.svelte";
  import TreeIcon from "svelte-material-icons/FileTree.svelte";
  import TopIcon from "svelte-material-icons/FormatVerticalAlignTop.svelte";
  import TrashIcon from "svelte-material-icons/DeleteForeverOutline.svelte";

  // marked for move options
  import Cancel from "svelte-material-icons/Cancel.svelte";

  // move target options

  import { createEventDispatcher } from "svelte";

  import client from "./client";

  const dispatch = createEventDispatcher();

  export let item;
  export let displayConfig = {};
  export let indent = 0;
  export let enableOptions = true;

  export let moving = null;

  const LOCATION = Object.freeze({
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

  function handleDetach() {
    client
      .unlink({ what: item["_what"], _id: item["_id"] })
      .then(() => dispatch("refresh"))
      .catch(() => alert("error on detach"));
  }

  function moveItem(location) {
    client
      .move({
        location:
          location === LOCATION.ABOVE
            ? "above"
            : location === LOCATION.BELOW
            ? "below"
            : "child",
        what: moving.what,
        id: moving._id,
        to_what: item._what,
        to_id: item._id,
      })
      .then(() => {
        dispatch("refresh");
        moving = null;
      })
      .catch(() => alert("error on move"));
  }

  // prettier-ignore
  const options = [
    { Icon: HandIcon,   text: "move",          action: () => { moving = { what: item._what, _id: item._id }; } },
    { Icon: UpIcon,     text: "create above",  action: () => { createMode = LOCATION.ABOVE; } },
    { Icon: DownIcon,   text: "create below",  action: () => { createMode = LOCATION.BELOW; } },
    { Icon: TreeIcon,   text: "create child",  action: () => { createMode = LOCATION.CHILD; } },
    { Icon: TopIcon,    text: "detach top",    action: handleDetach },
    { Icon: TrashIcon,  text: "delete",        action: handleDelete },
  ];

  // prettier-ignore
  const moveTargetOptions = [
    { Icon: Cancel,     text: "cancel move",      action: () => { moving = null; } },
    { Icon: UpIcon,     text: "place above",      action: () => { moveItem(LOCATION.ABOVE); } },
    { Icon: DownIcon,   text: "place below",      action: () => { moveItem(LOCATION.BELOW); } },
    { Icon: TreeIcon,   text: "place as child ",  action: () => { moveItem(LOCATION.CHILD); } },
  ]

  // prettier-ignore
  const markedForMoveOptions = [
    { Icon: Cancel,   text: "cancel move",   action: () => { moving = null; } },
  ]

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

  $: markedForMove =
    moving !== null && moving.what === item._what && moving._id === item._id;
  $: moveTarget = moving !== null && !markedForMove;

  const newItem = { _children: [], _what: item["_what"], title: "new item" };
</script>

{#if createMode === LOCATION.ABOVE}
  <Item item={newItem} {displayConfig} {indent} options={create} />
{/if}

<Item
  {item}
  {displayConfig}
  {indent}
  options={moveTarget
    ? moveTargetOptions
    : markedForMove
    ? markedForMoveOptions
    : options}
  bind:open
  {enableOptions}
  on:refresh
  elevate={markedForMove}
/>

{#if open}
  {#each item._children as child (child._id)}
    <svelte:self
      item={child}
      {displayConfig}
      indent={indent + 32}
      bind:enableOptions
      on:refresh
      bind:moving
    />
  {/each}
{/if}

{#if createMode === LOCATION.BELOW || createMode === LOCATION.CHILD}
  <Item
    item={newItem}
    {displayConfig}
    indent={indent + (createMode === LOCATION.CHILD ? 32 : 0)}
    options={create}
  />
{/if}

{#if createMode}
  <Prompt on:create={create} on:discard={discard} />
{/if}
<!-- 
{#if markedForMove}
  <Prompt on:create={create} on:discard={discard} />
{/if} -->
