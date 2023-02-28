<script>
  import CodeBraces from "svelte-material-icons/ChevronDown.svelte";

  export let types = [];
  export let emojis = [];
  export let selected;

  function select(itemtype) {
    selected = itemtype;
  }
</script>

<div class="container">
  <div class="title">
    <div class="abc">
      <CodeBraces color="black" size="18" />
    </div>
    <span class="titlename"> Items </span>
  </div>
  {#each types as itemtype, i}
    <span
      class="item {itemtype === selected ? 'selected' : ''}"
      on:click={() => select(itemtype)}
      on:keypress={undefined}
    >
      {emojis[i]}
      <span class="itemname">{itemtype}</span>
    </span>
  {/each}
</div>

<style>
  div.abc {
    display: flex;
  }
  div.container {
    display: flex;
    flex-direction: column;
    background-color: #eef0f2;
    width: 12vw;
    padding-left: 15px;
    padding-top: 45px;
  }
  span.titlename {
    margin-left: 14px;
  }
  span.item {
    font-size: 16px;
    margin: 2px;
    padding: 6px;
    padding-left: 15px;
    margin-right: 20px;
    user-select: none;
    cursor: pointer;
    border-radius: 8px;
  }
  span.item:hover {
    background-color: #bcb8b1;
    opacity: 80%;
  }
  span.selected {
    background-color: #bcb8b1;
  }
  span.itemname {
    margin-left: 10px;
  }
  div.title {
    display: flex;
    flex-direction: row;
    font-size: 16px;
    color: black;
    font-weight: bold;
    padding-left: 20px;
    margin-bottom: 10px;
  }
</style>
