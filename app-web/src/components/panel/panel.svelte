<script>
  import PanelItem from "./panel-item.svelte";
  import IconButton from "../icon-button.svelte";
  import { space, spaces, order, emojis, type } from "../../utils";

  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  function onCreate() {
    alert("create");
  }
  function onEdit(typeName, i) {
    dispatch("edit", { what: typeName });
  }
  function onMove(typeName, i) {
    alert("move");
  }
</script>

<div class="column panel">
  <PanelItem id="title" emoji="" name="Spaces" />
  {#each $spaces as spaceName (spaceName)}
    <PanelItem
      emoji="🪐"
      name={spaceName}
      selected={spaceName === $space}
      on:click={() => space.set(spaceName)}
    />
  {/each}

  <PanelItem id="title" emoji="" name="Defined types">
    <div class="row align buttons">
      <IconButton name="plus" color="grey" size="small" on:click={onCreate} />
    </div>
  </PanelItem>
  {#each $order as typeName, i ($space + typeName)}
    <PanelItem
      emoji={$emojis[i]}
      name={typeName}
      selected={typeName === $type}
      on:click={() => type.set(typeName)}
    >
      <div class="row align buttons">
        <IconButton
          name="cog-outline"
          color="black"
          size="small"
          on:click={() => onEdit(typeName, i)}
        />
        <IconButton
          name="hand-outline"
          color="black"
          size="small"
          on:click={() => onMove(typeName, i)}
        />
      </div>
    </PanelItem>
  {/each}
</div>

<style>
  .panel {
    border-right: var(--gap-line) solid var(--panel-color-border);
    padding-left: var(--gap-large);
    padding-top: var(--gap-large);
    width: var(--panel-width);
    margin-top: var(--gap-medium);
    margin-bottom: var(--gap-medium);
    overflow: scroll;
  }
  .buttons {
    gap: var(--gap-medium);

    /* prettier-ignore */
    visibility:
      var(--panel-item-hover-true, visible)
      var(--panel-item-hover-false, hidden);
  }

  :global(.panel .panel-item#title > .name) {
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
