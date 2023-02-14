<script>
  import ItemTask from "./item-task.svelte";
  import ItemNote from "./item-note.svelte";
  import ItemCheck from "./item-check.svelte";
  import ItemAccount from "./item-account.svelte";
  import ItemItem from "./item-item.svelte";
  import ItemEmail from "./item-email.svelte";
  import ItemTransaction from "./item-transaction.svelte";

  export let itemtype;

  export let controlMode = false;

  export let item;

  export let source = undefined;
  export let edited = false;

  export let onClick = undefined;
  export let onDelete = undefined;

  // prettier-ignore
  const Item =
    itemtype === "task" ? ItemTask
    : itemtype === "check" ? ItemCheck
    : itemtype === "note" ? ItemNote
    : itemtype === "account" ? ItemAccount
    : itemtype === "item" ? ItemItem
    : itemtype === "email" ? ItemEmail
    : itemtype === "transaction" ? ItemTransaction
    : undefined
</script>

{#if Item === undefined}
  <div>- {item.title}</div>
{:else}
  <Item {controlMode} bind:item {source} bind:edited {onClick} {onDelete} />
{/if}
