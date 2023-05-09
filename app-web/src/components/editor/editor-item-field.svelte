<script>
</script>

<div class="flex editor-item-field">
  <slot />
</div>

<style>
  :root {
    --border-width: 1px;
  }
  .editor-item-field {
    padding: var(--border-width);
    padding-left: calc(var(--gap-medium) + var(--border-width));
    padding-right: calc(var(--gap-medium) + var(--border-width));
    border-radius: var(--radius-small);
  }
  /* div.editor-item-field:hover {
    padding: 0px;
    padding-left: var(--gap-medium);
    padding-right: var(--gap-medium);

    border-radius: var(--radius-small);
    border: var(--border-width) solid var(--color-pistachio);
  } */

  /* background-color: var(--color-pistachio); */
  /* opacity: 70%; */
</style>
