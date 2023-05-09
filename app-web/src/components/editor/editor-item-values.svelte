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

<div class="row align editor-item-values">
  {#if values}
    {#each Object.keys(values) as value (value)}
      <div class="row align value-container" style:--color={values[value]}>
        <!-- <Menu {options} loseFocus> -->
        <div class="value">{value}</div>
        <!-- </Menu> -->
      </div>
    {/each}
  {/if}
</div>

<style>
  .editor-item-values {
    padding: var(--gap-large);
    flex-wrap: wrap;
  }
  .value-container {
    /* even with Menu, this is probably useless. Just set color and it will be inherited
    by the menu-option text */
    --value-hover-true: ;
    --value-hover-false: inherit;

    border: var(--gap-line) solid var(--color);
    color: var(--color);

    border-radius: var(--radius-small);
    background-color: var(--color-white);
    margin: var(--gap-small);
    padding: var(--gap-medium);
    gap: var(--gap-small);
  }
  .value-container:hover {
    --value-hover-true: inherit;
    --value-hover-false: ;

    /* TODO: figure out a way to make --color lighter and use it without inverted text color */
    background-color: var(--color);
  }
  .value {
    /* prettier-ignore */
    color: 
      var(--value-hover-true, white)
      var(--value-hover-false, --color);
  }
</style>
