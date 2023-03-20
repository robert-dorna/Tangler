<script>
  import Styles from "./styles.svelte";
  import Panel from "./panel/panel.svelte";
  import Items from "./items/items.svelte";
  import client from "./client";
  import { displayConfig, newItem } from "./stores";

  import { onMount } from "svelte";

  onMount(() => {
    displayConfig.fetch();
  });

  // TODO: deduce or from config
  let selected = "task";
  let items = [];

  function refreshData() {
    client.get({ method: "readall", what: selected }).then((json) => {
      items = json.result;
    });
  }

  // is this good or does it have e.g. SSR problems?
  $: if (selected) refreshData()
  $: if ($newItem.anchorId === null) refreshData()
</script>

<div class="container">
  <Panel bind:selected />
  <Items {items} on:refresh={refreshData} />
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
