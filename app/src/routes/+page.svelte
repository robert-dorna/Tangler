<script>
  import Navigation from "./navigation.svelte";
  import Panel from "./panel.svelte";
  import client from "./client.js";
  import Items from "./items.svelte";

  let displayConfig = {};
  client.displayConfig().then(json => {
    displayConfig = json
  })

  let types = [];
  let emojis = [];
  client.types().then((json) => {
    types = json.map((desc) => desc.name);
    emojis = json.map((desc) => desc.emoji);
  });

  let selected = "account";
  let data = []
  
  $: client.get({ method: "readall", what: selected }).then((json) => {
    data = json.result;
  });
</script>

<div class="container">
  <Navigation />
  <div class="columns">
    <Panel bind:selected {emojis} types={types} />
    <Items
      itemtype={selected}
      items={data}
      {displayConfig}
    />
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
