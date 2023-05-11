<script>
  import { createEventDispatcher } from "svelte";
  import Item from "./item.svelte";
  import Prompt from "../prompt.svelte";
  import { client, LOCATION, newItem } from "../../utils";

  const dispatch = createEventDispatcher();

  export let item;
  export let indent = 0;

  $: anchorId = $newItem.anchorId;
  $: anchorWhat = $newItem.anchorWhat;

  $: newItemLocation = anchorId === item._id && anchorWhat === item._what ? $newItem.location : false;

  $: children = item._children;
  $: len = children.length;
  $: open = len > 0 ? true : undefined;

  $: newItemFields = { _id: "new", _what: $newItem.anchorWhat };

  function create() {
    client.oldapi
      .create({
        ...newItemFields,
        _location: newItemLocation,
        _anchorId: item["_id"],
        _anchorWhat: item["_what"],
      })
      .then(() => {
        dispatch("refresh");
        newItem.discard();
      });
  }
</script>

{#if newItemLocation === LOCATION.ABOVE}
  <Item item={newItemFields} {indent} on:create={create} />
{/if}

<Item {item} {indent} bind:open on:refresh />

{#if open}
  {#each item._children as child (child._id)}
    <svelte:self item={child} indent={indent + 32} on:refresh />
  {/each}
{/if}

{#if newItemLocation === LOCATION.BELOW || newItemLocation === LOCATION.CHILD}
  <Item item={newItemFields} indent={indent + (newItemLocation === LOCATION.CHILD ? 32 : 0)} on:create={create} />
{/if}

{#if newItemLocation}
  <Prompt on:create={create} on:discard={() => newItem.discard()} />
{/if}

<!-- 
{#if markedForMove}
  <Prompt on:create={create} on:discard={discard} />
{/if}
-->
