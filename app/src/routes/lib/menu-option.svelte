<script>
  import Icon from "./icon.svelte";

  export let icon;
  export let emoji = undefined;
  export let text;
  export let textColor = undefined;
  export let action;
  export let index;
  export let count;
</script>

<!-- TODO: fix open menu on options change -->
<div
  class="option"
  class:first-option={index === 0}
  class:last-option={index === count - 1}
  on:click|stopPropagation={action}
  on:keypress={undefined}
>
  {#if emoji !== undefined}
    <div class="emoji">
      {emoji}
    </div>
  {:else}
    <Icon name={icon} color="black" size={24} />
  {/if}
  {#if textColor !== undefined}
    <span style="color: {textColor};">{text}</span>
  {:else}
    {text}
  {/if}
</div>

<style>
  div.option {
    display: flex;
    align-items: center;
    padding: 10px;
    gap: 10px;
  }
  div.option:hover {
    background-color: #f4f3ee;
  }
  div.first-option {
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
  }
  div.last-option {
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
  }
  div.emoji {
    font-size: 22px;
    padding: 5px;
  }
</style>
