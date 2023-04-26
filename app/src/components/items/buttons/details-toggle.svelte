<script>
  import Hovering from "../../../components/hovering.svelte";
  import Icon from "../../../components/icon.svelte";

  export let detailed = false;
  export let color = "darkgoldenrod";
  export let hoverColor = "brown";
  export let size = 24;

  let hover = false;

  $: currentColor = hoverColor && hover ? hoverColor : color;
  $: cls = `g-row-centered g-details-toggle-container ${!detailed ? "g-details-toggle-extra-padding" : ""}`;
</script>

<Hovering {cls} bind:hover on:click={() => (detailed = !detailed)}>
  {#if detailed}
    <Icon name="dot" color={currentColor} {size} />
    <Icon name="dot" color={currentColor} {size} />
  {:else}
    <Icon name="dots-h" color={currentColor} {size} />
  {/if}
</Hovering>

<!-- TODO: figure out a way to avoid global classes here or complicated names -->
<style>
  :global(div.g-details-toggle-container) {
    padding-top: var(--gap-small);
    padding-bottom: var(--gap-small);
  }
  :global(div.g-details-toggle-container:hover) {
    border-radius: var(--radius-small);
    background-color: var(--color-silver);
  }
  :global(div.g-details-toggle-extra-padding) {
    padding-left: var(--gap-small);
    padding-right: var(--gap-small);
  }
</style>
