<script>
  import IconButton from "./icon-button.svelte";

  export let cls = "";

  export let nameOn;
  export let nameOff;
  export let color;
  export let size;

  export let toggled = false;
</script>

<IconButton
  cls="icon-switch {cls} {toggled ? 'icon-switch-is-toggled' : 'icon-switch-is-not-toggled'}"
  name={toggled ? nameOn : nameOff}
  {color}
  {size}
  on:click={() => (toggled = !toggled)}
/>

<style>
  :global(.icon-switch-is-toggled) {
    --icon-switch-is-on: initial;
    --icon-switch-is-off: ;
  }
  :global(.icon-switch-is-not-toggled) {
    --icon-switch-is-on: ;
    --icon-switch-is-off: initial;
  }
</style>
