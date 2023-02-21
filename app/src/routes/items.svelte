<script>
  import Item from "./item.svelte";

  export let itemtype;
  export let items = [];
  export let displayConfig = {}
</script>

<div class="container">
  <div class="items">
    {#each items as item, index (item._what + item._id)}
      <Item {displayConfig} {itemtype} {item} />
    {/each}
    {#if Array.isArray(items) && items.length === 0}
      <div class="noitems">No items</div>
    {/if}
  </div>
</div>

<style>
  div.container {
    display: flex;
    flex-direction: row;
    min-width: 700px;
  }
  div.items {
    display: flex;
    flex: 1;
    flex-direction: column;
    align-items: flex-start;
    padding-left: 50px;
    padding-top: 50px;
    /* flex-wrap: wrap; */
  }
  div.noitems {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 15px;
    padding: 10px;
  }
</style>
