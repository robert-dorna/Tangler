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

<Hovering
  cls="menu {cls} {visible ? 'menu-options-visible-true' : 'menu-options-visible-false'}"
  {style}
  hidden={hide}
  bind:position
  on:click={handleClick}
  bind:hover
>
  <slot />
  {#if visible}
    <div class="column floating elevated options" style={menuPosition}>
      {#each options as option (option.text)}
        <MenuOption {...option}/>
      {/each}
    </div>
  {/if}
</Hovering>

<style>
  .options {
    background-color: var(--color-white);
    border-radius: var(--radius-small);
    max-height: var(--menu-height);
    overflow: scroll;
  }
  :global(.menu-options-visible-true) {
    --menu-options-visible: initial;
    --menu-options-not-visible: ;
  }
  :global(.menu-options-visible-false) {
    --menu-options-visible: ;
    --menu-options-not-visible: initial;
  }
</style>
