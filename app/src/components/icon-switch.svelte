<script>
  import IconButton from "./icon-button.svelte";

  export let cls = "";

  export let nameOn;
  export let nameOff;
  export let color;
  export let size;

  export let toggled = false;
</script>

<IconButton cls="{cls} {toggled ? 'toggle-true' : 'toggle-false'}" name={toggled ? nameOn : nameOff} {color} {size} on:click={() => (toggled = !toggled)} />

<style>
  :global(div.toggle-true) {
    --button-switch-is-on: initial;
    --button-switch-is-off: ;
  }
  :global(div.toggle-false) {
    --button-switch-is-on: ;
    --button-switch-is-off: initial;
  }
</style>
