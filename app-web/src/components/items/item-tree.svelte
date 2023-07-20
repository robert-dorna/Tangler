<script>
  import { createEventDispatcher } from "svelte";
  import Item from "./item.svelte";
  import Prompt from "../prompt.svelte";
  import { client, space, LOCATION, newItem } from "../../utils";

  const dispatch = createEventDispatcher();

  export let item;
  export let indent = 0;

  $: open = item._children.length > 0 ? true : undefined;
  $: anchored = newItem.isAnchoredTo($newItem.anchor, item);

  function toggleOpen() {
    if (open !== undefined) open = !open;
  }

  function translateObsoleteLocation(location) {
    if (location === LOCATION.ABOVE) return "above";
    if (location === LOCATION.BELOW) return "below";
    return "child";
  }

  function create() {
    // const { _id, _what: newFieldType, ...fields } = $newItem.item

    const fields = { ...$newItem.item };
    delete fields._id;
    const newFieldType = fields._what;
    delete fields._what;
    client.data
      .create(newFieldType, {
        ...fields,
        _place: {
          relationship: translateObsoleteLocation($newItem.location),
          reference: {
            what: item["_what"],
            _id: item["_id"],
          },
        },
      })
      .then(() => {
        dispatch("refresh");
        newItem.discard();
      });
  }
</script>

{#if anchored && $newItem.location === LOCATION.ABOVE}
  <Item item={$newItem.item} {indent} on:create={create} />
{/if}

<!-- anchored: {anchored} newItemLocation: {$newItem.location} -->
<Item {item} {indent} {open} on:toggleOpen={toggleOpen} on:refresh />

{#if open}
  {#each item._children as child ($space + child._what + child._id)}
    <svelte:self item={child} indent={indent + 32} on:refresh />
  {/each}
{/if}

{#if anchored && ($newItem.location === LOCATION.BELOW || $newItem.location === LOCATION.CHILD)}
  <Item
    item={$newItem.item}
    indent={indent + ($newItem.location === LOCATION.CHILD ? 32 : 0)}
    on:create={create}
  />
{/if}

{#if anchored}
  <Prompt on:create={create} on:discard={() => newItem.discard()} />
{/if}

<!-- 
{#if markedForMove}
  <Prompt on:create={create} on:discard={discard} />
{/if}
-->
