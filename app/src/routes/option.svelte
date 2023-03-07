<script>
  import Hold from "svelte-material-icons/ArrowDownBold.svelte";

  export let Icon;
  export let text;
  export let action;
  export let index;
  export let count;

  // prettier-ignore
  $: extraClass =
    index === 0
      ? 'first-option'
      : index === count - 1
        ? 'last-option'
        : '';
</script>

<div class="option {extraClass}" on:click on:keypress={undefined}>
  <svelte:component this={Icon} color="black" size={24} />
  {text}
  {#if text === "move"}
    <div class="hold-key">
      {"("}
      <Hold color="grey" size={24} />
      Alt {")"}
    </div>
  {/if}
</div>

<style>
  div.first-option {
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
  }
  div.last-option {
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
  }
  div.option {
    display: flex;
    align-items: center;
    padding: 10px;
    gap: 10px;
  }
  div.option:hover {
    background-color: #f4f3ee;
  }
  div.hold-key {
    display: flex;
    justify-content: center;
    align-items: center;
    color: grey;
  }
</style>
