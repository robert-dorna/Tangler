<script>
  import ItemTree from "./item-tree.svelte";

  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  function triggerRefresh() {
    dispatch("refresh");
  }

  export let items = [];
  export let displayConfig = {};

  let enableOptions = true;
</script>

<div class="container">
  <div class="items">
    {#each items as item, index (item._what + item._id)}
      <ItemTree
        {displayConfig}
        {item}
        bind:enableOptions
        on:refresh={triggerRefresh}
      />
    {/each}
    {#if Array.isArray(items) && items.length === 0}
      <div class="noitems">No items</div>
    {/if}
  </div>
</div>

<style>
  div.container {
    display: flex;
    /* background-color: blueviolet; */
    flex-direction: row;
    min-width: 700px;
    overflow: scroll;
    height: 90vh;
    width: 100%;
    /* width: 80vw; */
    padding-right: 30px;
  }
  div.items {
    display: flex;
    flex: 1;
    flex-direction: column;
    align-items: flex-start;
    /* padding-left: 50px;
    padding-top: 50px; */
    padding-left: 30px;
    padding-top: 30px;
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
