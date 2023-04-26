<script>
  import Item from "./panel-item.svelte";
  import Button from "./panel-button.svelte";
  import { displayConfig } from "../../utils";

  export let selected;

  let newItem = false;

  function onCreate() {
    alert("create")
    return;
    newItem = { emoji: "🌋", name: "xd" };
  }

  function onEdit(typeName, i) {
    alert("edit")
  }

  function onMove(typeName, i) {
    alert("move")
  }

  $: emojis = $displayConfig.emojis || [];
  $: types = $displayConfig.order || [];
</script>

<div class="g-column panel">
  <Item emoji="" name="Items" title>
    <Button name="plus" color="grey" on:click={onCreate} />
  </Item>
  {#each types as typeName, i (typeName)}
    <Item
      emoji={emojis[i]}
      name={typeName}
      selected={typeName === selected}
      on:click={() => (selected = typeName)}
    >
      <div class="g-row-aligned buttons">
        <Button
          name="cog-outline"
          color="black"
          on:click={() => onEdit(typeName, i)}
        />
        <Button
          name="hand-outline"
          color="black"
          on:click={() => onMove(typeName, i)}
        />
      </div>
    </Item>
  {/each}
  <!-- {#if newItem}
    <Item emoji={newItem.emoji} bind:name={newItem.name} edit>
      <Button name="plus" color="grey" on:click={() => dispatch("plus")} />
    </Item>
  {/if} -->
</div>

<style>
  div.panel {
    background-color: var(--panel-color-bg);
    border-right: var(--gap-tiny) solid var(--panel-color-border);
    padding-left: var(--gap-large);
    padding-top: var(--gap-large);
    width: var(--panel-width);
  }
  div.buttons {
    gap: var(--gap-medium);
    visibility: var(--x-buttons-visibility);
  }
</style>
