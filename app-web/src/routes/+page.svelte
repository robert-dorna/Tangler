<script>
  import { onMount } from "svelte";
  import Editor from "../components/editor/editor.svelte";
  import Items from "../components/items/items.svelte";
  import Panel from "../components/panel/panel.svelte";
  import { client, displayConfig, displayConfigAvailable } from "../utils";
  import "./styles.svelte";

  onMount(() => {
    displayConfig.fetch();
  });

  // // TODO: deduce it or load from config
  let selected = null;
  let items = [];

  function refreshItems() {
    client.get({ method: "readall", what: selected }).then((json) => {
      items = json.result;
    });
  }

  $: if ($displayConfigAvailable && selected === null) selected = $displayConfig.order[0]
  // // TODO: check is this good or does it have e.g. SSR problems?
  $: if (selected && $displayConfigAvailable) refreshItems();

  let edit = null;

  function onEdit(event) {
    edit = event.detail.what;
  }
</script>

<div class="row flex screen-size application">
  <Panel bind:selected on:edit={onEdit} />
  <Items {items} on:refresh={refreshItems} />
  {#if edit !== null}
    <div class="flex screen-size floating-editor">
      <div class="row flex center">
        {#if $displayConfigAvailable}
          <Editor what={edit} on:discard={() => (edit = null)} on:edit={onEdit} on:refresh={refreshItems}/>
        {/if}
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
