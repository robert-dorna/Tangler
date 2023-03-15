<script>
  import CodeBraces from "svelte-material-icons/ChevronDown.svelte";
  import Cog from "svelte-material-icons/Cog.svelte";
  import HandIcon from "svelte-material-icons/HandFrontLeftOutline.svelte";
  import Plus from "svelte-material-icons/PlusThick.svelte";

  export let types = [];
  export let emojis = [];
  export let selected;

  function select(itemtype) {
    selected = itemtype;
  }
</script>

<div class="container">
  <div class="item title-hover">
    <CodeBraces color="black" size="18" />
    <div class="name title">Items</div>
    <div class="spacer" />
    <div class="buttons">
      <Plus color="grey" size="20" />
    </div>
  </div>
  {#each types as itemtype, i (itemtype)}
    <div
      class="item item-hover"
      class:selected={itemtype === selected}
      on:click={() => select(itemtype)}
      on:keypress={undefined}
    >
      {emojis[i]}
      <div class="name">{itemtype}</div>
      <div class="spacer" />
      <div class="buttons">
        <div class="button" on:click={undefined} on:keypress={undefined}>
          <Cog color="black" size="20" />
        </div>
        <HandIcon color="black" size="20" />
      </div>
    </div>
  {/each}
</div>

<style>
  :root {
    --buttons-visibility: hidden;
  }
  div.container {
    display: flex;
    flex-direction: column;
    background-color: var(--panel-color-bg);
    border-right: 2px solid var(--panel-color-border);
    width: 20vw;
    padding-left: 15px;
    padding-top: 45px;
  }
  div.name {
    margin-left: 15px;
  }
  div.title {
    font-weight: bold;
  }
  div.item {
    display: flex;
    align-items: center;
    margin: 2px;
    margin-right: 20px;
    padding: 10px;
    padding-left: 15px;
    padding-right: 15px;
    font-size: 18px;
    border-radius: 8px;
    user-select: none;
    cursor: pointer;
  }
  div.title-hover:hover {
    --buttons-visibility: visible;
  }
  div.item-hover:hover {
    background-color: var(--panel-color-hover);
    opacity: 80%;
    --buttons-visibility: visible;
  }
  div.selected {
    background-color: var(--panel-color-hover);
  }
  div.spacer {
    display: flex;
    flex: 1;
  }
  div.buttons {
    display: flex;
    align-items: center;
    gap: 10px;
    visibility: var(--buttons-visibility);
  }
  div.button {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 5px;
    border-radius: 8px;
  }
  div.button:hover {
    background-color: var(--panel-color-button-hover);
  }
</style>
