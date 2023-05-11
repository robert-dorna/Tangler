<script>
  import { createEventDispatcher } from "svelte";
  import Menu from "../menu/menu.svelte";
  import { client } from "../../utils";

  const dispatch = createEventDispatcher();

  export let name;
  export let style = undefined;
  export let values = undefined;

  export let width = undefined;

  $: widthStyle = width === 0 ? "display: flex; flex: 1" : `width: ${width}px; margin-left: 35px`;
  $: actualStyle = style !== undefined ? style : width === undefined ? "" : `${widthStyle}; font-size: 22px;`;

  export let item;
  export let editing;

  let originalValue = item[name];
  let input = null;

  function submitChange() {
    editing = false;
    if (item[name] !== originalValue && item["_id"] !== "new") {
      client.oldapi
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

  $: isEnum = values !== undefined && typeof values === "object";

  $: options = !isEnum
    ? []
    : Object.keys(values).map((value) => {
        return {
          text: value,
          textColor: values[value],
          action: () => {
            item[name] = value;
            submitChange();
          },
        };
      });
</script>

<svelte:window on:keyup={handleKeyPress} />
<div class="field" style="{actualStyle} {isEnum && value in values ? `color: ${values[value]};` : ''}" on:keypress={undefined}>
  {#if isEnum}
    <Menu bind:focus={editing} {options}>
      <span class="value">
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
    <span class="value" on:click|stopPropagation={() => (editing = name)} on:keypress={undefined}>
      {value}
    </span>
  {/if}
  <slot />
</div>

<style>
  .field {
    display: flex;
    align-items: center;
  }
  input {
    all: unset;
    padding: calc(var(--gap-small) - var(--gap-line));
    padding-left: calc(var(--gap-medium) - var(--gap-line));
    border-radius: var(--radius-small);
    border: var(--gap-line) solid var(--color-silver);
    color: var(--color-black);
  }
  span.value {
    padding: var(--gap-small);
    padding-left: var(--gap-medium);
    padding-right: var(--gap-medium);
  }
  span.value:hover {
    border-radius: var(--radius-small);
    border: 1px solid var(--color-silver);
    /* background-color: var(--color-silver); */
  }
</style>
