<script>
  import Navigation from "./navigation.svelte";
  import Panel from "./panel.svelte";
  import Items from "./items.svelte";
  import client from "./client.js";

  // import { JSONEditor } from 'svelte-jsoneditor'

  let displayConfig = {};
  client.displayConfig().then((json) => {
    displayConfig = {
      types: json.types,
      order: json.order,
      emojis: json.order.map((typename) => json.types[typename].emoji)
    }
  });

  // $: content = {
  //   text: undefined,
  //   json: { ...displayConfig },
  // }

  let selected = "task";
  let data = [];

  $: client.get({ method: "readall", what: selected }).then((json) => {
    data = json.result;
  });
</script>

<div class="container">
  <Navigation />
  <div class="columns">
    <Panel bind:selected emojis={displayConfig.emojis} types={displayConfig.order} />
    <Items items={data} {displayConfig} />
  </div>
</div>

<!-- <div class="overlay">
  <JSONEditor bind:content/>
</div> -->

<style>
  div {
    display: flex;
    background-color: white;
    width: 100vw;
    height: 100vh;
  }
  div.overlay {
    z-index: 1;
    position: absolute;
    top: 20vh;
    left: 20vw;
    width: 60vw;
    height: 60vh;
    justify-content: center;
    align-items: center;
    background-color: brown;
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
