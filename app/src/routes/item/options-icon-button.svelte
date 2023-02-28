<script>
  import DotsVertical from "svelte-material-icons/DotsVertical.svelte";
  import Option from "../option.svelte";

  export let visible = false;
  export let options = [];

  let showOptions = false;

  $: style = !visible
    ? "visibility: hidden;"
    : showOptions
    ? "border-radius: 8px; background-color: #bcb8b1;"
    : "";

  $: if (!visible) showOptions = false;

  let position = { x: 0, y: 0 };
  function handleMouseMove(event) {
    position.x = event.clientX;
    position.y = event.clientY;
  }

  let optionsPosition = "";

  function handleClick() {
    showOptions = true;
    optionsPosition = `left: ${position.x}px; top: ${position.y}px;`;
  }
</script>

<div
  class="container"
  {style}
  on:click={handleClick}
  on:keypress={undefined}
  on:mousemove={handleMouseMove}
>
  <DotsVertical color="grey" size={30} />
  {#if showOptions}
    <div class="options" style={optionsPosition}>
      {#each options as option, i (option.text)}
        <Option {...option} index={i} count={options.length} />
      {/each}
    </div>
  {/if}
</div>

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
