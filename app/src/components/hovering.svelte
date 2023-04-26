<script>
  export let cls = "";
  export let style = "";
  export let hide = false;
  export let elevated = false;

  export let position = { x: 0, y: 0 };
  export let hover = false;

  function hoverOn() {
    if (!hover) hover = true;
  }

  function hoverOff() {
    if (hover) hover = false;
  }

  function handleMouseMove(event) {
    position.x = event.clientX;
    position.y = event.clientY;
  }
</script>

<div
  class={cls}
  class:g-elevated={elevated}
  style="{style} {hide ? 'visibility: hidden;' : ''}"
  on:click|stopPropagation
  on:keypress={undefined}
  on:mousemove={handleMouseMove}
  on:mouseenter={hoverOn}
  on:mouseleave={hoverOff}
>
  <slot {hover} {position} />
</div>