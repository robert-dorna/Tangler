<script>
  export let position = { x: 0, y: 0 };

  function handleMouseMove(event) {
    position.x = event.clientX;
    position.y = event.clientY;
  }
</script>

<div
  on:click|stopPropagation
  on:keypress={undefined}
  on:mousemove={handleMouseMove}
>
  <slot />
</div>
