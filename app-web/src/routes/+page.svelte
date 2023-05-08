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

<div class="container">
  <Panel bind:selected on:edit={({ detail: { what } }) => (edit = what)} />
  <Items {items} on:refresh={refreshItems} />
  {#if edit !== null}
    <div class="g-floating qq-flex modal">
      <div class="qq-flex qq-row qq-center">
        {#if displayConfigAvailable}
          <Editor what={edit} on:discard={() => (edit = null)} />
        {/if}
      </div>
    </div>
  {/if}
</div>

<style>
  div.container {
    display: flex;
    flex-direction: row;
    flex: 1;
    width: 100vw;
    height: 100vh;
    font-family: var(--app-font-family);
    background-color: var(--page-color-bg);
  }

  div.modal {
    width: 100vw;
    height: 100vh;
  }
</style>
