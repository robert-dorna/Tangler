<script>
  import ItemTree from "./item-tree.svelte";
  import { lang, displayConfigAvailable } from "../../utils";

  const texts = lang.components.items;

  export let items = [];
</script>

<div class="row items-container">
  <div class="column flex items">
    {#if $displayConfigAvailable}
      {#each items as item, index (item._what + item._id)}
        <ItemTree {item} on:refresh />
      {/each}
    {/if}
    {#if Array.isArray(items) && items.length === 0}
      <div class="row center noitems">{texts.no_items}</div>
    {/if}
    <!-- TODO: replace below with some css e.g. in div.items -->
    <div class="space">space</div>
    <div class="space">space</div>
  </div>
</div>

<style>
  .items-container {
    min-width: var(--items-width);
    height: 100vh;
    width: 100%;
    overflow: scroll;
  }
  .items {
    align-items: flex-start;
    padding-left: var(--gap-max);
    padding-top: var(--gap-max);
  }
  .noitems {
    margin: var(--gap-large);
    padding: var(--gap-medium);
  }
  .space {
    display: flex;
    font-size: 128px;
    visibility: hidden;
  }
</style>
