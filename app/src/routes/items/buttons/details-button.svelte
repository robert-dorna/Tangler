<script>
  import PencilPlus from "svelte-material-icons/PencilPlus.svelte";

  export let color = 'darkgoldenrod';
  export let hoverColor = 'brown';
  export let size = 24;
  export let visible = false;

  $: style = visible ? "" : "visibility: hidden;";

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
  {style}
  on:mouseenter={hoverOn}
  on:mouseleave={hoverOff}
  on:click|stopPropagation
  on:keypress={undefined}
>
  <PencilPlus color={currentColor} {size} />
</div>

<style>
  div.container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 5px;
  }
  div.container:hover {
    border-radius: 8px;
    background-color: #bcb8b1;
  }
</style>
