<script>
  import Item from "./item.svelte";
  import NewItem from "./new-item.svelte";
  import client from "./client.js";

  export let itemtype;

  export let controlMode = false;

  export let items = [];

  export let onSelect;
  export let onCreate;
  export let onDelete;

  $: itemsSlice = itemtype === "transaction" ? items.slice(0, 30) : items;
</script>

<div class="container">
  <h2>{itemtype}</h2>
  {#each itemsSlice as item, index (item._id)}
    {#if controlMode}
      <NewItem on:click={() => onCreate(index)}/>
    {/if}
    <Item
      {itemtype}
      {controlMode}
      {item}
      onClick={() => onSelect(item, index)}
      onDelete={() => onDelete(index)}
    />
  {/each}
  {#if controlMode}
    <NewItem on:click={() => onCreate()}/>
  {/if}
  {#if Array.isArray(itemsSlice) && itemsSlice.length === 0}
    <div class="noitems">No items</div>
  {/if}
</div>

<style>
  div.container {
    display: flex;
    flex: 1;
    flex-direction: column;
  }
  h2 {
    align-self: center;
  }
  div.noitems {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 15px;
    padding: 10px;
  }
</style>
