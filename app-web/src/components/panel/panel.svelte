<script>
  import PanelItem from "./panel-item.svelte";
  import IconButton from "../icon-button.svelte";
  import { displayConfig } from "../../utils";

  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  export let selected;

  function onCreate() {
    alert("create");
  }
  function onEdit(typeName, i) {
    dispatch("edit", { what: typeName });
  }
  function onMove(typeName, i) {
    alert("move");
  }

  $: emojis = $displayConfig.emojis || [];
  $: types = $displayConfig.order || [];
</script>

<div class="column panel">
  <PanelItem id="title" emoji="" name="Items">
    <IconButton name="plus" color="grey" size="small" on:click={onCreate} />
  </PanelItem>
  {#each types as typeName, i (typeName)}
    <PanelItem emoji={emojis[i]} name={typeName} selected={typeName === selected} on:click={() => (selected = typeName)}>
      <div class="row align buttons">
        <IconButton name="cog-outline" color="black" size="small" on:click={() => onEdit(typeName, i)} />
        <IconButton name="hand-outline" color="black" size="small" on:click={() => onMove(typeName, i)} />
      </div>
    </PanelItem>
  {/each}
</div>

<style>
  .panel {
    background-color: var(--panel-color-bg);
    border-right: var(--gap-tiny) solid var(--panel-color-border);
    padding-left: var(--gap-large);
    padding-top: var(--gap-large);
    width: var(--panel-width);
  }
  .buttons {
    gap: var(--gap-medium);

    /* prettier-ignore */
    visibility:
      var(--panel-item-hover-true, visible)
      var(--panel-item-hover-false, hidden);
  }

  :global(.panel .panel-item#title > .name) {
    font-weight: bold;
    margin-left: 0px;
  }

  :global(.panel .panel-item:not(#title):hover) {
    background-color: var(--panel-color-hover);
    opacity: var(--opacity-hover);
  }

  :global(.panel .icon-button) {
    border-radius: var(--radius-small);
    padding: var(--gap-small);
  }

  :global(.panel .icon-button:hover) {
    background-color: var(--panel-color-button-hover);
  }
</style>
