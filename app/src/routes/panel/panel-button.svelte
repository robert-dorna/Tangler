<script>
  import ExpandedIcon from "svelte-material-icons/ChevronDown.svelte";
  import CogIcon from "svelte-material-icons/Cog.svelte";
  import HandIcon from "svelte-material-icons/HandFrontLeftOutline.svelte";
  import PlusIcon from "svelte-material-icons/PlusThick.svelte";

  export let name;
  export let color;
  export let slim = false;

  const icons = {
    down: ExpandedIcon,
    cog: CogIcon,
    hand: HandIcon,
    plus: PlusIcon,
  };

  $: icon = icons[name];

  $: size = slim ? 18 : 20;
</script>

<div class="button" class:padding={!slim} on:click on:keypress={undefined}>
  <svelte:component this={icon} {color} {size} />
</div>

<style>
  div.button {
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
  }
  div.padding {
    padding: 5px;
  }
  div.padding:hover {
    background-color: var(--panel-color-button-hover);
  }
</style>
