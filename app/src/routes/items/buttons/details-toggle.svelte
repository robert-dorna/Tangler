<script>
  import Hovering from "../../../components/hovering.svelte";
  import Icon from "../../../components/icon.svelte";

  export let detailed = false;
  export let color = "darkgoldenrod";
  export let hoverColor = "brown";
  export let size = 24;

  let hover = false;

  $: currentColor = hoverColor && hover ? hoverColor : color;
  $: cls = `g-details-toggle-container ${!detailed ? "g-details-toggle-extra-padding" : ""}`;
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
    display: flex;
    justify-content: center;
    align-items: center;
    padding-top: 5px;
    padding-bottom: 5px;
  }
  :global(div.g-details-toggle-container:hover) {
    border-radius: 8px;
    background-color: #bcb8b1;
  }
  :global(div.g-details-toggle-extra-padding) {
    padding-left: 5px;
    padding-right: 5px;
  }
</style>
