<script>
  import Icon from "../icon.svelte";

  export let icon;
  export let emoji = undefined;
  export let text;
  export let textColor = undefined;
  export let action;
</script>

<!-- TODO: fix open menu on options change -->
<div class="row align menu-option" on:click|stopPropagation={action} on:keypress={undefined}>
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
  .menu-option {
    padding: var(--gap-medium);
    gap: var(--gap-medium);
  }
  .menu-option:hover {
    background-color: var(--color-isabelline);
  }
  .emoji {
    font-size: var(--font-large);
    padding: var(--gap-small);
  }
</style>
