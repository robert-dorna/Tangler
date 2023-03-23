<script>
  import ItemTree from "./item-tree.svelte";
  import { displayConfigAvailable } from "../stores";

  export let items = [];
</script>

<div class="container">
  <div class="items">
    {#if $displayConfigAvailable}
      {#each items as item, index (item._what + item._id)}
        <ItemTree {item} on:refresh />
      {/each}
    {/if}
    {#if Array.isArray(items) && items.length === 0}
      <div class="noitems">No items</div>
    {/if}
    <!-- TODO: replace below with some css e.g. in div.items -->
    <div class="space">space</div>
    <div class="space">space</div>
  </div>
</div>

<style>
  div.container {
    display: flex;
    flex-direction: row;
    min-width: 700px;
    overflow: scroll;
    height: 100vh;
    width: 100%;
    padding-right: 30px;
  }
  div.items {
    display: flex;
    flex: 1;
    flex-direction: column;
    align-items: flex-start;
    padding-left: 30px;
    padding-top: 30px;
    margin-bottom: 50px;
  }
  div.space {
    display: flex;
    font-size: 128px;
    visibility: hidden;
  }
  div.noitems {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 15px;
    padding: 10px;
  }
</style>
