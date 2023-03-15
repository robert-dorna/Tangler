<script>
  import Styles from "./styles.svelte"
  import Navigation from "./navigation.svelte";
  import Panel from "./panel.svelte";
  import Items from "./items.svelte";
  import client from "./client.js";

  import { onMount } from "svelte";

  onMount(() => {
    client.displayConfig().then((json) => {
      displayConfig = {
        types: json.types,
        order: json.order,
        emojis: json.order.map((typename) => json.types[typename].emoji),
      };
    });
  });

  let displayConfig = {};

  // TODO: deduce or from config
  let selected = "task";
  let data = [];

  // is this good or does it have e.g. SSR problems?
  $: client.get({ method: "readall", what: selected }).then((json) => {
    data = json.result;
  });

  function refreshData() {
    client.get({ method: "readall", what: selected }).then((json) => {
      data = json.result;
    });
  }
</script>

<div class="container">
  <!-- <Navigation /> -->
  <div class="columns">
    <Panel
      bind:selected
      emojis={displayConfig.emojis}
      types={displayConfig.order}
    />
    <Items items={data} {displayConfig} on:refresh={refreshData}/>
  </div>
</div>

<style>
  div {
    display: flex;
    background-color: white;
    width: 100vw;
    height: 100vh;
  }
  div.container {
    flex: 1;
    flex-direction: column;
    font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS",
      sans-serif;
  }
  div.columns {
    flex: 1;
    flex-direction: row;
    width: 100vw;
  }
</style>
