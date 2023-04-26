<script>
  import Icon from "./icon.svelte";

  export let cls = "";

  export let name;
  export let color;
  export let size;
</script>

<div
  class={cls}
  on:click|stopPropagation
  on:keypress={undefined}
>
  <Icon {name} {color} {size} />
</div>