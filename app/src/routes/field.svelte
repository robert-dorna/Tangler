<script>
  import Trackpad from "./buttons/trackpad.svelte";
  import ValueSelector from "./value-selector.svelte";
  // import client from "./client";

  export let name;
  export let style = undefined;
  export let colors = undefined;

  export let item;
  export let editing;

  let input = null;
  let position = { x: 0, y: 0 };
  let menuPosition = "";

  function submitChange() {
    editing = false;
    // if (valueChanged && "_id" in item) {
    //   client.update({
    //     what: item["_what"],
    //     _id: item["_id"],
    //     [name]: item[name],
    //   });
    // }
  }

  function handleKeyPress(event) {
    if (input) {
      if (event.key === "Escape" || event.key === "Enter") {
        submitChange();
      }
    }
  }

  function onSelect(v) {
    item[name] = v;
    submitChange();
  }

  function onClick() {
    editing = name;
    menuPosition = `left: ${position.x}px; top: ${position.y}px;`;
  }

  $: value = item[name] || "?";
  $: if (input) input.focus();
</script>

<svelte:window on:keyup={handleKeyPress} />
<div
  class="container"
  style="{style} {colors && value in colors ? `color: ${colors[value]};` : ''}"
  on:click|self
  on:keypress={undefined}
>
  {#if name === editing}
    {#if colors !== undefined}
      <ValueSelector {colors} style={menuPosition} {onSelect} />
    {:else}
      <input
        bind:this={input}
        style="width: {value.length / 2 + 2}em;"
        type="text"
        bind:value={item[name]}
        on:focusout={submitChange}
      />
    {/if}
  {/if}

  {#if name !== editing || colors !== undefined}
    <Trackpad bind:position>
      <span class="field" on:click={onClick} on:keypress={undefined}>
        {value}
      </span>
    </Trackpad>
  {/if}
  <slot />
</div>

<style>
  div.container {
    display: flex;
    align-items: center;
  }
  input {
    all: unset;
    padding: 4px;
    padding-left: 9px;
    border-radius: 8px;
    border: 1px solid #bcb8b1;
    color: black;
  }
  span.field {
    padding: 5px;
    padding-left: 10px;
    padding-right: 10px;
  }
  span.field:hover {
    border-radius: 8px;
    background-color: #bcb8b1;
  }
</style>
