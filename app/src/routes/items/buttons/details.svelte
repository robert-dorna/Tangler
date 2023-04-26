<script>
  import Hovering from "../../../components/hovering.svelte";
  import Icon from "../../../components/icon.svelte";

  export let color = "darkgoldenrod";
  export let hoverColor = "brown";
  export let size = 24;
  export let visible = false;

  $: style = visible ? "" : "visibility: hidden;";
</script>

<Hovering cls="g-details-container" {style} on:click let:hover>
  <Icon
    name="pencil-plus"
    color={hoverColor && hover ? hoverColor : color}
    {size}
  />
</Hovering>

<style>
  :global(div.g-details-container) {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 5px;
  }
  :global(div.g-details-container:hover) {
    border-radius: 8px;
    background-color: #bcb8b1;
  }
</style>
