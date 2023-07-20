<script>
  import { onMount } from "svelte";
  import Editor from "../components/editor/editor.svelte";
  import Items from "../components/items/items.svelte";
  import Panel from "../components/panel/panel.svelte";
  import { fetch, itemsLoad } from "../utils";
  import "./styles.svelte";

  onMount(() => {
    fetch();
  });

  function refreshItems() {
    itemsLoad.set(true);
  }

  let edit = null;

  function onEdit(event) {
    edit = event.detail.what;
  }
</script>

<div class="row flex screen-size application">
  <Panel on:edit={onEdit} />
  <Items on:refresh={refreshItems} />
  {#if edit !== null}
    <div class="flex screen-size floating-editor">
      <div class="row flex center">
        <Editor what={edit} on:discard={() => (edit = null)} on:edit={onEdit} on:refresh={refreshItems} />
      </div>
    </div>
  {/if}
</div>

<style>
  .application {
    font-family: var(--app-font-family);
    background-color: var(--page-color-bg);
  }
</style>
