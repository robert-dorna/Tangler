<script>
</script>

<div class="field">
  <slot/>
</div>

<style>
  div.field {
    display: flex;
    flex: 1;
    padding: 1px;
    padding-left: calc(var(--gap-medium) + 1px);
    padding-right: calc(var(--gap-medium) + 1px);
    border-radius: var(--radius-small);
  }
  /* div.field:hover {
    padding: 0px;
    padding-left: var(--gap-medium);
    padding-right: var(--gap-medium);

    border-radius: var(--radius-small);
    border: 1px solid var(--color-pistachio);

  } */
    /* background-color: var(--color-pistachio); */
    /* opacity: 70%; */
</style>
