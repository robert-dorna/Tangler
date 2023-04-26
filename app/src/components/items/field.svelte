<script>
  import { createEventDispatcher } from "svelte";
  import Menu from "../menu/menu.svelte";
  import { client } from "../../utils";

  const dispatch = createEventDispatcher();

  // those 3 are from _gui.yaml (displayConfig)
  export let name;
  export let style = undefined;
  export let colors = undefined;

  export let item;
  export let editing;

  let originalValue = item[name];
  let input = null;

  function submitChange() {
    editing = false;
    if (item[name] !== originalValue && item["_id"] !== 'new') {
      client
        .update({
          what: item["_what"],
          _id: item["_id"],
          [name]: item[name],
        })
        .then(() => {
          dispatch("refresh");
          originalValue = item[name];
        });
    }
  }

  function handleKeyPress(event) {
    if (input) {
      if (event.key === "Escape" || event.key === "Enter") {
        submitChange();
      }
    }
  }

  $: value = item[name] || "?";
  $: if (input) input.focus();

  const options =
    colors === undefined
      ? []
      : Object.keys(colors).map((value) => {
          return {
            text: value,
            textColor: colors[value],
            action: () => {
              item[name] = value;
              submitChange();
            },
          };
        });
</script>

<svelte:window on:keyup={handleKeyPress} />
<div
  class="container"
  style="{style} {colors && value in colors ? `color: ${colors[value]};` : ''}"
  on:keypress={undefined}
>
  {#if colors !== undefined}
    <Menu bind:focus={editing} {options}>
      <span class="field">
        {value}
      </span>
    </Menu>
  {:else if name === editing}
    <input
      bind:this={input}
      style="width: {value.length / 2 + 2}em;"
      type="text"
      bind:value={item[name]}
      on:focusout={submitChange}
      on:click|stopPropagation={() => undefined}
    />
  {:else}
    <span
      class="field"
      on:click|stopPropagation={() => (editing = name)}
      on:keypress={undefined}
    >
      {value}
    </span>
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
