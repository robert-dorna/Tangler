<script>
  import "./styles.svelte";

  import Panel from "../components/panel/panel.svelte";
  import Items from "../components/items/items.svelte";

  import Editor from "../components/editor/editor.svelte";

  import { client, displayConfig, displayConfigAvailable } from "../utils";

  import { onMount } from "svelte";

  onMount(() => {
    displayConfig.fetch();
  });

  // // TODO: deduce it or load from config
  let selected = "task";
  let items = [];

  function refreshItems() {
    client.get({ method: "readall", what: selected }).then((json) => {
      items = json.result;
    });
  }

  // // TODO: check is this good or does it have e.g. SSR problems?
  $: if (selected && $displayConfigAvailable) refreshItems();

  let edit = null;
</script>

<div class="row flex screen-size container">
  <Panel bind:selected on:edit={({ detail: { what } }) => (edit = what)} />
  <Items {items} on:refresh={refreshItems} />
  {#if edit !== null}
    <div class="flex screen-size floating">
      <div class="row flex center">
        {#if displayConfigAvailable}
          <Editor what={edit} on:discard={() => (edit = null)} />
        {/if}
      </div>
    </div>
  {/if}
</div>

<style>
  .container {
    font-family: var(--app-font-family);
    background-color: var(--page-color-bg);
  }
</style>
