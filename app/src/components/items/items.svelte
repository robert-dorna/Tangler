<script>
  import ItemTree from "./item-tree.svelte";
  import { lang, displayConfigAvailable } from "../../utils";

  const texts = lang.components.items;

  export let items = [];
</script>

<div class="g-row container">
  <div class="g-column-flex items">
    {#if $displayConfigAvailable}
      {#each items as item, index (item._what + item._id)}
        <ItemTree {item} on:refresh />
      {/each}
    {/if}
    {#if Array.isArray(items) && items.length === 0}
      <div class="g-row-centered noitems">{texts.no_items}</div>
    {/if}
    <!-- TODO: replace below with some css e.g. in div.items -->
    <div class="space">space</div>
    <div class="space">space</div>
  </div>
</div>

<style>
  div.container {
    min-width: var(--items-width);
    height: 100vh;
    width: 100%;
    overflow: scroll;
  }
  div.items {
    align-items: flex-start;
    padding-left: var(--gap-max);
    padding-top: var(--gap-max);
  }
  div.noitems {
    margin: var(--gap-large);
    padding: var(--gap-medium);
  }
  div.space {
    display: flex;
    font-size: 128px;
    visibility: hidden;
  }
</style>
