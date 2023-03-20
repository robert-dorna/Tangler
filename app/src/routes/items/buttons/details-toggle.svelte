<script>
  import Dot from "svelte-material-icons/CircleSmall.svelte";
  import Dots from "svelte-material-icons/DotsHorizontal.svelte";

  export let detailed = false;
  export let color = 'darkgoldenrod';
  export let hoverColor = 'brown';
  export let size = 24;

  const extraPadding = "padding-left: 5px; padding-right: 5px;";

  function handleClick() {
    detailed = !detailed;
  }

  let hover = false;

  function hoverOn() {
    if (!hover) hover = true;
  }
  function hoverOff() {
    if (hover) hover = false;
  }

  $: currentColor = hoverColor && hover ? hoverColor : color;
</script>

<div
  class="container"
  style={!detailed ? extraPadding : ""}
  on:click|stopPropagation={handleClick}
  on:keypress={undefined}
  on:mouseenter={hoverOn}
  on:mouseleave={hoverOff}
>
  {#if detailed}
    <Dot color={currentColor} {size} />
    <Dot color={currentColor} {size} />
  {:else}
    <Dots color={currentColor} {size} />
  {/if}
</div>

<style>
  div.container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding-top: 5px;
    padding-bottom: 5px;
  }
  div.container:hover {
    border-radius: 8px;
    background-color: #bcb8b1;
  }
</style>
