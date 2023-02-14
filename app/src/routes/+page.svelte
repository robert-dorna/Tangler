<script>
  import Navigation from "./navigation.svelte";
  import Items from "./items.svelte";
  import ItemModal from "./item-modal.svelte";
  import client from "./client.js";
  import utils from "./utils.js";

  const layouts = {
    tasks: ["check", "task", "note"],
    stuff: ["account", "item"], // file
    comm: ["contact", "email"],
    timeline: ["journal", "transaction"],
  };

  let data = Object.keys(layouts).reduce((a, c) => ({ ...a, [c]: [] }), {});

  const screens = ["tasks", "stuff", "comm", "timeline"];
  const projects = ["priv", "health", "nomad", "JDG"];
  const priorities = ["p1", "p2", "p3", "p4"];
  const meanings = ["feat", "cleanup"];

  $: screen = screens[0];
  $: project = projects;
  $: priority = priorities;
  $: meaning = meanings;

  $: layout = layouts[screen];

  const whats = Object.keys(layouts)
    .reduce((a, c) => [...a, layouts[c].join()], [])
    .join(",");

  client.get({ method: "read", what: whats }).then((json) => {
    data = json.result;
  });

  let controlMode = false;

  let modalVisible = false;
  
  $: if (modalVisible) controlMode = false;

  function handleKeyDown(event) {
    if (event.key === "Control" && !modalVisible) controlMode = true;
  }

  function handleKeyUp(event) {
    if (event.key === "Control") controlMode = false;
  }

  let modalItem = null;
  let modalSource = null;
  let modalEdited = false;

  let modalMethod = undefined;
  let modalItemtype = undefined;
  let modalIndex = undefined;

  $: if (!modalVisible) {
    modalItem = null;
    modalSource = null;
    modalEdited = false;

    modalMethod = undefined;
    modalItemtype = undefined;
    modalIndex = undefined;
  }

  async function refresh(itemtype) {
    return client
      .get({
        method: "read",
        what: itemtype,
      })
      .then((json) => {
        data = {
          ...data,
          [itemtype]: json.result,
        };
        modalVisible = false;
      });
  }

  function remove(itemtype, index) {
    client
      .get({
        method: "delete",
        what: itemtype,
        index,
      })
      .then(() => refresh(itemtype));
  }

  function update() {
    client
      .get({
        method: "update",
        what: modalItemtype,
        index: modalIndex,
        ...utils.diffObjects(modalSource, modalItem),
      })
      .then(() => refresh(modalItemtype));
  }

  function create() {
    client
      .get({
        method: "create",
        what: modalItemtype,
        index: modalIndex,
        ...modalItem,
      })
      .then(() => refresh(modalItemtype))
      .then(() => {
        controlMode = false;
      });
  }

  function triggerUpdateModal(itemtype, item, index) {
    modalItem = { ...item };
    modalSource = { ...item };
    modalEdited = false;

    modalMethod = "update";
    modalItemtype = itemtype;
    modalIndex = index;

    modalVisible = true;
  }

  function triggerCreateModal(itemtype, index = undefined) {
    modalItem = {
      due_date: new Date().toISOString().slice(0, 10),
      label: "cleanup",
      priority: "p2",
      project: "priv",
      title: "do X",
    };

    modalSource = {};
    modalEdited = true;

    modalMethod = "create";
    modalItemtype = itemtype;
    modalIndex = index;

    modalVisible = true;
  }
</script>

<svelte:window on:keydown={handleKeyDown} on:keyup={handleKeyUp}/>
<div class="container">
  <Navigation
    {screens}
    {projects}
    {priorities}
    {meanings}
    bind:screen
    bind:project
    bind:priority
    bind:meaning
  />
  <div class="columns">
    {#each layout as itemtype (itemtype)}
      <Items
        {itemtype}
        {controlMode}
        items={data[itemtype]}
        onSelect={(item, index) => triggerUpdateModal(itemtype, item, index)}
        onCreate={(index) => triggerCreateModal(itemtype, index)}
        onDelete={(index) => remove(itemtype, index)}
      />
    {/each}
  </div>
</div>
<ItemModal
  bind:visible={modalVisible}
  onSubmit={() => (modalMethod === "create" ? create() : update())}
  itemtype={modalItemtype}
  bind:item={modalItem}
  source={modalSource}
  edited={modalEdited}
/>

<style>
  div {
    display: flex;
  }
  div.container {
    flex: 1;
    flex-direction: column;
  }
  div.columns {
    flex: 1;
    flex-direction: row;
  }
</style>
