<script>
  import Hovering from "../hovering.svelte";
  import MenuOption from "./menu-option.svelte";

  export let cls = "";
  export let style = "";
  export let hide = false;

  export let options = [];
  export let focus = undefined;
  export let loseFocus = false;

  const focusKey = Symbol();

  let hover = false;

  let position = { x: 0, y: 0 };
  let menuPosition = "";

  function handleClick() {
    focus = focusKey;
    menuPosition = `left: ${position.x}px; top: ${position.y}px;`;
  }

  $: visible = focus === focusKey;
  $: if (!hover && loseFocus) focus = undefined;
</script>

<Hovering cls="{cls} {visible ? 'visible-true' : 'visible-false'}" {style} {hide} bind:position on:click={handleClick} bind:hover>
  <slot />
  {#if visible}
    <div class="qq-column g-floating options g-elevated" style={menuPosition}>
      {#each options as option, i (option.text)}
        <MenuOption {...option} index={i} count={options.length} />
      {/each}
    </div>
  {/if}
</Hovering>

<style>
  div.options {
    background-color: var(--color-white);
    border-radius: var(--radius-small);
    max-height: var(--menu-height);
    overflow: scroll;
  }
  :global(div.visible-true) {
    --menu-is-visible: initial;
    --menu-is-not-visible: ;
  }
  :global(div.visible-false) {
    --menu-is-visible: ;
    --menu-is-not-visible: initial;
  }
</style>
