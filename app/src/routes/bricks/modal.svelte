<script>
  export let visible = false;
  export let style;
</script>

<svelte:window on:keyup on:keydown />
{#if visible}
  <div class="slate shade" />
  <div
    class="slate"
    {style}
    on:keydown={() => undefined}
    on:click|self
  >
    <slot/>
  </div>
{/if}

<style>
  div {
    display: flex;
    flex-direction: column;
  }
  div.shade {
    opacity: 80%;
    z-index: 1;
    background-color: black;
    /* backdrop-filter: blur(6px); */
  }
  div.slate {
    position: fixed;
    z-index: 2;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
  }
</style>