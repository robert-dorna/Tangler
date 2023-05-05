<script>
  import Icon from "./icon.svelte";

  export let cls = "";
  export let hidden = false;

  export let name;
  export let color;
  export let size;
</script>

<div class={cls} class:g-hidden={hidden} on:click|stopPropagation on:keypress={undefined}>
  <Icon {name} {color} {size} />
</div>
