<script>
  import "./styles.svelte";

  import Panel from "../components/panel/panel.svelte"
  import Items from "../components/items/items.svelte";

  import client from "../client";
  import { displayConfig, displayConfigAvailable } from "../stores";

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
</script>

<div class="container">
  <Panel bind:selected />
  <Items {items} on:refresh={refreshItems} />
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
</style>
