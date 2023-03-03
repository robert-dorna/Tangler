<script>
  import Trackpad from "./trackpad.svelte";

  export let item;
  export let displayConfig;
  export let editing;

  export let value;

  $: types = displayConfig.types
  $: what = item._what
  $: typeConfig = types[what]
  $: emoji = typeConfig.emoji

  let style = "";

  function onClick() {
    editing = "_what";
    style = `left: ${position.x}px; top: ${position.y}px;`;
  }

  $: values = displayConfig.order;

  let position = { x: 0, y: 0 };

  function onSelect(v) {
    value = v;
    item['title'] = 'costam'
    editing = false;
  }
</script>

<Trackpad bind:position>
  <div class="emoji" on:click|self={onClick} on:keypress={undefined}>
    {emoji}
    {#if editing === "_what"}
      <div class="container" {style}>
        <div class="wrap">
          {#each values as v (v)}
            <div
              class="value"
              on:keypress={undefined}
              on:click={() => onSelect(v)}
            >
              {displayConfig.types[v].emoji}
              {v}
            </div>
          {/each}
        </div>
      </div>
    {/if}
  </div>
</Trackpad>

<style>
  div.emoji {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-right: 5px;
    padding: 5px;
  }
  div.emoji:hover {
    border-radius: 8px;
    background-color: #bcb8b1;
  }
  div.container {
    display: flex;
    flex-direction: column;
    background-color: white;
    border-radius: 8px;
    padding: 2px;
    position: absolute;
    z-index: 1;
    box-shadow: 8px 8px 24px 0px rgba(66, 68, 90, 1);
  }
  div.wrap {
    display: flex;
    flex-direction: column;
    max-height: 20vw;
    /*
      Cannot use wrap because of a bug
      https://stackoverflow.com/questions/33891709/when-flexbox-items-wrap-in-column-mode-container-does-not-grow-its-width
    */
    /* flex-wrap: wrap; */
    overflow: scroll;
  }
  div.value {
    display: flex;
    background-color: white;
    padding: 20px;
  }
  div.value:hover {
    background-color: #f4f3ee;
  }
</style>
