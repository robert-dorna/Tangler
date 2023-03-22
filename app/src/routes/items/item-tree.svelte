<script>
  import Item from "./item.svelte";
  import Prompt from "../prompt.svelte";
  import { LOCATION, newItem } from "../stores";

  export let item;
  export let indent = 0;

  $: anchorId = $newItem.anchorId;
  $: anchorWhat = $newItem.anchorWhat;

  $: newItemLocation =
    anchorId === item._id && anchorWhat === item._what
      ? $newItem.location
      : false;

  $: children = item._children;
  $: len = children.length;
  $: open = len > 0 ? true : undefined;
</script>

{#if newItemLocation === LOCATION.ABOVE}
  <Item {indent} />
{/if}

<Item {item} {indent} bind:open on:refresh />

{#if open}
  {#each item._children as child (child._id)}
    <svelte:self item={child} indent={indent + 32} on:refresh />
  {/each}
{/if}

<!-- {#if newItemLocation === LOCATION.BELOW || newItemLocation === LOCATION.CHILD}
  <Item indent={indent + (newItemLocation === LOCATION.CHILD ? 32 : 0)} />
{/if} -->

<!-- TODO: move prompts to options? -->

{#if newItemLocation}
  <Prompt on:create={() => undefined} on:discard={() => newItem.discard()} />
{/if}

<!-- 
{#if markedForMove}
  <Prompt on:create={create} on:discard={discard} />
{/if}
-->
