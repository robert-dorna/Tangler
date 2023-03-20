<script>
  import Item from "./panel-item.svelte";
  import Button from "./panel-button.svelte";
  import { displayConfig } from "../stores";

  $: emojis = $displayConfig.emojis || []
  $: types = $displayConfig.order || []

  export let selected;

  let newItem = false;

  function select(itemtype) {
    selected = itemtype;
  }

  function create() {
    newItem = {
      emoji: '🌋',
      name: 'xd'
    };
  }
</script>

<div class="container">
  <Item title name="Items" on:plus={create}>
    <Button name="down" color="black" slim />
  </Item>
  {#each types as itemtype, i (itemtype)}
    <Item
      name={itemtype}
      selected={itemtype === selected}
      on:click={() => select(itemtype)}
    >
      {emojis[i]}
    </Item>
  {/each}
  {#if newItem}
    <Item bind:name={newItem.name} edit>
      {newItem.emoji}
    </Item>
  {/if}
</div>

<style>
  div.container {
    display: flex;
    flex-direction: column;
    background-color: var(--panel-color-bg);
    border-right: 2px solid var(--panel-color-border);
    width: 20vw;
    padding-left: 15px;
    padding-top: 45px;
  }
</style>
