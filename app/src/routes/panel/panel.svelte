<script>
  import Item from "./item.svelte";
  import Button from "./button.svelte";
  import { displayConfig } from "../stores";

  export let selected;

  let newItem = false;

  function create() {
    newItem = { emoji: "🌋", name: "xd" };
  }

  $: emojis = $displayConfig.emojis || [];
  $: types = $displayConfig.order || [];
</script>

<div class="container">
  <Item title name="Items" on:plus={create}>
    <Button name="expanded" color="black" slim />
  </Item>
  {#each types as typeName, i (typeName)}
    <Item
      name={typeName}
      selected={typeName === selected}
      on:click={() => (selected = typeName)}
      on:settings={() => alert("settings")}
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
