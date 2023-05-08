<script>
  import Icon from "../icon.svelte";

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
  class="qq-row qq-align option"
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
    <Icon name={icon} color="black" size="medium" />
  {/if}
  {#if textColor !== undefined}
    <span style="color: {textColor};">{text}</span>
  {:else}
    {text}
  {/if}
</div>

<style>
  div.option {
    padding: var(--gap-medium);
    gap: var(--gap-medium);
  }
  div.option:hover {
    background-color: var(--color-isabelline);
  }
  div.first-option {
    border-top-left-radius: var(--radius-small);
    border-top-right-radius: var(--radius-small);
  }
  div.last-option {
    border-bottom-left-radius: var(--radius-small);
    border-bottom-right-radius: var(--radius-small);
  }
  div.emoji {
    font-size: var(--font-large);
    padding: var(--gap-small);
  }
</style>
