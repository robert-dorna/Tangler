<script>
  import PanelButton from "./panel-button.svelte";

  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  export let name;
  export let selected = false;
  export let title = false;
  export let edit = false;

  let editing = false;
  let input = null;
  $: if (input) input.focus();
</script>

<div
  class="item"
  class:hover-highlight={!title}
  class:selected
  on:click
  on:keypress={undefined}
>
  <slot />
  {#if !editing}
    <div class="name" class:title>{name}</div>
  {:else}
    <input
      bind:this={input}
      type="text"
      bind:value={name}
    />
  {/if}
  <div class="spacer" />
  <div class="buttons">
    {#if title}
      <PanelButton name="plus" color="grey" on:click={() => dispatch("plus")} />
    {:else if edit}
      <PanelButton name="plus" color="grey" on:click={() => dispatch("plus")} />
    {:else}
      <PanelButton name="cog" color="black" on:click={undefined} />
      <PanelButton name="hand" color="black" on:click={undefined} />
    {/if}
  </div>
</div>

<style>
  :root {
    --buttons-visibility: hidden;
  }
  div.selected {
    background-color: var(--panel-color-hover);
  }
  input {
    all: unset;
    border: 1px solid grey;
    border-radius: 8px;
    padding: 5px;
    margin-left: 15px;
  }
  div.name {
    margin-left: 15px;
  }
  div.title {
    font-weight: bold;
  }
  div.item {
    display: flex;
    align-items: center;
    margin: 2px;
    margin-right: 20px;
    padding: 10px;
    padding-left: 15px;
    padding-right: 15px;
    font-size: 18px;
    border-radius: 8px;
    user-select: none;
    cursor: pointer;
  }
  div.item:hover {
    --buttons-visibility: visible;
  }
  div.hover-highlight:hover {
    background-color: var(--panel-color-hover);
    opacity: 80%;
  }
  div.spacer {
    display: flex;
    flex: 1;
  }
  div.buttons {
    display: flex;
    align-items: center;
    gap: 10px;
    visibility: var(--buttons-visibility);
  }
</style>
