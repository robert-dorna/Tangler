<script>
  export let hover = false;

  function hoverOn() {
    if (!hover) hover = true;
  }

  function hoverOff() {
    if (hover) hover = false;
  }
</script>


<div
  class="flex"
  on:mouseenter={hoverOn}
  on:mouseleave={hoverOff}
  on:click
  on:keypress={undefined}
>
  <slot/>
</div>

<style>
  div.flex {
    display: flex;
    flex: 1;
    flex-direction: column;
  }
</style>