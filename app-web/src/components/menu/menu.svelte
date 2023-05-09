<script>
  import Tooltip from "../tooltip.svelte";
  import MenuOption from "./menu-option.svelte";

  export let cls = "";
  export let style = "";
  export let hide = false;

  export let focus = undefined;
  export let loseFocus = false;

  export let options = [];
</script>

<Tooltip cls="menu {cls}" {style} {hide} bind:focus {loseFocus}>
  <slot />
  <div slot="tooltip" class="column floating-menu elevated options" let:menuPosition style={menuPosition} >
    {#each options as option (option.text)}
      <MenuOption {...option} bind:focus />
    {/each}
  </div>
</Tooltip>

<style>
  :global(.menu) {
    --menu-options-visible: --tooltip-visible;
    --menu-options-not-visible: --tooltip-not-visible;
  }
  .options {
    background-color: var(--color-white);
    border-radius: var(--radius-small);
    max-height: var(--menu-height);
    overflow: scroll;
  }
</style>
