<script>
  import Navigation from "./navigation.svelte";
  import Panel from "./panel.svelte";
  import Items from "./items.svelte";
  import client from "./client.js";

  let displayConfig = {};
  let types = [];
  client.displayConfig().then((json) => {
    displayConfig = json.types;
    types = json.order;
  });

  $: emojis = types.map((typename) => displayConfig[typename].emoji);

  let selected = "task";
  let data = [];

  $: client.get({ method: "readall", what: selected }).then((json) => {
    data = json.result;
  });
</script>

<div class="container">
  <Navigation />
  <div class="columns">
    <Panel bind:selected {emojis} {types} />
    <Items items={data} {displayConfig} />
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
