<script>
  import Hovering from "../../../components/hovering.svelte";
  import Icon from "../../../components/icon.svelte";

  export let color = "darkgoldenrod";
  export let hoverColor = "brown";
  export let visible = false;

  $: style = visible ? "" : "visibility: hidden;";
</script>

<Hovering cls="g-row-centered g-details-container" {style} on:click let:hover>
  <Icon
    name="pencil-plus"
    color={hoverColor && hover ? hoverColor : color}
    size="medium"
  />
</Hovering>

<style>
  :global(div.g-details-container) {
    padding: var(--gap-small);
  }
  :global(div.g-details-container:hover) {
    border-radius: var(--radius-small);
    background-color: var(--color-silver);
  }
</style>
