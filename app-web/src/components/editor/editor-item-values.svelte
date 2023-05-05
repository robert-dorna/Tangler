<script>
  import Menu from "../menu/menu.svelte";

  export let values;

  // prettier-ignore
  const options = [
    // { icon: 'hand-outline', text: "move",         action: () => undefined },
    { icon: 'pencil-outline', text: "rename",       action: () => undefined },
    { icon: 'color-picker',   text: "change color", action: () => alert('pick color') },
    { icon: 'trash',          text: "delete",       action: () => alert('delete') },
  ];
</script>

<div class="g-row-aligned values">
  {#if values}
    {#each Object.keys(values) as value (value)}
      <div class="g-row-aligned value l-value" style:--color={values[value]} style="color: {values[value]}; border: 1px solid {values[value]}">
        <Menu {options} loseFocus>
          <div class="name" style:--color={values[value]}>{value}</div>
        </Menu>
      </div>
    {/each}
  {/if}
</div>

<style>
  .values {
    padding: var(--gap-large);
    flex-wrap: wrap;
  }
  :global(.l-value) {
    --value-hover-true: ;
    --value-hover-false: inherit;
  }
  :global(.l-value:hover) {
    --value-hover-true: inherit;
    --value-hover-false: ;
  }
  .value {
    border-radius: var(--radius-small);
    background-color: var(--color-white);
    margin: var(--gap-small);
    padding: var(--gap-medium);
    gap: var(--gap-small);
  }
  .value:hover {
    /* TODO: figure out a way to make --color lighter and use it without inverted text color */
    background-color: var(--color);
  }
  .name {
    /* prettier-ignore */
    color: 
      var(--value-hover-true, white)
      var(--value-hover-false, --color);
  }
</style>
