<script>
  import Trackpad from "./trackpad.svelte";
  import DotsVertical from "svelte-material-icons/DotsVertical.svelte";
  import Option from "../option.svelte";

  export let visible = false;
  export let options = [];
  export let editing;

  let position = { x: 0, y: 0 };
  let menuPosition = "";

  $: showOptions = editing === true;

  function handleClick() {
    editing = true;
    menuPosition = `left: ${position.x}px; top: ${position.y}px;`;
  }

  $: style = !visible
    ? "visibility: hidden;"
    : showOptions
    ? "border-radius: 8px; background-color: #bcb8b1;"
    : "";
</script>

<Trackpad bind:position on:click={handleClick}>
  <div class="container" {style}>
    <DotsVertical color="grey" size={30} />
    {#if showOptions}
      <div class="options" style={menuPosition}>
        {#each options as option, i (option.text)}
          <Option
            {...option}
            index={i}
            count={options.length}
            on:click={() => {
              // TODO: fix open menu on options change
              option.action();
              // editing = false;
            }}
          />
        {/each}
      </div>
    {/if}
  </div>
</Trackpad>

<style>
  div.container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 5px;
    margin-left: 19px;
  }
  div.container:hover {
    border-radius: 8px;
    background-color: #bcb8b1;
  }
  div.options {
    display: flex;
    flex-direction: column;
    background-color: white;
    border-radius: 8px;
    position: absolute;
    z-index: 1;
    box-shadow: 8px 8px 24px 0px rgba(66, 68, 90, 1);
  }
</style>
