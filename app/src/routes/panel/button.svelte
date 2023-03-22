<script>
  import Icon from "../lib/icon.svelte";

  export let name;
  export let color;
  export let slim = false;
  export let onClick = undefined;

  $: size = slim ? 18 : 20;
</script>

{#if onClick === undefined}
  <div class="button" class:padding={!slim}>
    <Icon {name} {color} {size} />
  </div>
{:else}
  <div
    class="button"
    class:padding={!slim}
    on:click|stopPropagation={onClick}
    on:keypress={undefined}
  >
    <Icon {name} {color} {size} />
  </div>
{/if}

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
