<script>
</script>

<div class="field">
  <slot/>
</div>

<style>
  div.field {
    display: flex;
    flex: 1;
    padding-left: var(--gap-medium);
    padding-right: var(--gap-medium);
    border-radius: var(--radius-small);
  }
  div.field:hover {
    background-color: var(--color-pistachio);
    /* opacity: 70%; */
  }
</style>
