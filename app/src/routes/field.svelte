<script>
  import client from "./client";

  export let name;
  export let style = undefined;
  export let colors = undefined;

  export let item;

  export let editing;

  let value = item[name] || "?";

  let input = null;
  $: hasInput = input !== undefined && input !== null;

  function onClick() {
    editing = name;
  }

  $: if (hasInput) input.focus();

  function submitChange() {
    editing = undefined;
    if (value !== item[name]) {
      client.update({
        what: item["_what"],
        _id: item["_id"],
        [name]: value,
      });
    }
  }

  function handleKeyPress(event) {
    if (hasInput) {
      if (event.key === "Escape" || event.key === "Enter") {
        submitChange();
      }
    }
  }
</script>

<svelte:window on:keyup={handleKeyPress} />
<div
  style="{style} {colors && value in colors ? `color: ${colors[value]};` : ''}"
  on:click|self
  on:keypress={undefined}
>
  {#if name === editing}
    <input
      bind:this={input}
      style="width: {value.length / 2 + 2}em;"
      type="text"
      bind:value
      on:focusout={submitChange}
    />
  {:else}
    <span class="field" on:click={onClick} on:keypress={undefined}>
      {value}
    </span>
  {/if}
  <slot />
</div>

<style>
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
