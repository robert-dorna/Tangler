<script>
  import Hovering from "./hovering.svelte";

  export let cls = "";
  export let style = "";
  export let hide = false;

  export let focus = undefined;
  export let loseFocus = false;

  const focusKey = Symbol();

  let hover = false;

  let position = { x: 0, y: 0 };
  let menuPosition = "";

  function handleClick() {
    if (focus !== focusKey) {
      focus = focusKey;
      menuPosition = `left: ${position.x}px; top: ${position.y}px;`;
    }
  }

  $: visible = focus === focusKey;
  $: if (!hover && loseFocus) focus = undefined;
</script>

<Hovering
  cls="tooltip clickable {cls} {visible ? 'tooltip-visible-true' : 'tooltip-visible-false'}"
  {style}
  hidden={hide}
  bind:position
  on:click={handleClick}
  bind:hover
>
  <slot />
  {#if visible}
    <slot name="tooltip" {menuPosition} />
  {/if}
</Hovering>

<style>
  :global(.tooltip-visible-true) {
    --tooltip-visible: initial;
    --tooltip-not-visible: ;
  }
  :global(.tooltip-visible-false) {
    --tooltip-visible: ;
    --tooltip-not-visible: initial;
  }
</style>
