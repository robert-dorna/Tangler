<script>
  import client from "../../client";
  import { LOCATION, movingItem, newItem } from "../../stores";

  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  export let item;

  // prettier-ignore
  export const allOptions = {
    normal: [
      { icon: 'hand-outline',   text: "move",           action: () => { $movingItem = { what: item._what, _id: item._id }; } },
      { icon: 'up',             text: "create above",   action: () => { newItem.select(item, LOCATION.ABOVE) } },
      { icon: 'down',           text: "create below",   action: () => { newItem.select(item, LOCATION.BELOW) } },
      { icon: 'tree',           text: "create child",   action: () => { newItem.select(item, LOCATION.CHILD) } },
      { icon: 'top',            text: "detach top",     action: () => { detachItem() } },
      { icon: 'trash',          text: "delete",         action: () => { deleteItem() } },
    ],
    moveTarget: [
      { icon: 'cancel',       text: "cancel move",      action: () => { $movingItem = null; } },
      { icon: 'up',           text: "place above",      action: () => { moveItem(LOCATION.ABOVE); } },
      { icon: 'down',         text: "place below",      action: () => { moveItem(LOCATION.BELOW); } },
      { icon: 'tree',         text: "place as child ",  action: () => { moveItem(LOCATION.CHILD); } },
    ],
    markedForMove: [
      { icon: 'cancel',       text: "cancel move",      action: () => { $movingItem = null; } },
    ],
  };

  export let options = allOptions.normal;

  $: itemIsMarkedForMove =
    $movingItem !== null &&
    $movingItem.what === item._what &&
    $movingItem._id === item._id;

  $: itemIsMoveTarget = $movingItem !== null && !itemIsMarkedForMove;

  $: options = itemIsMoveTarget
    ? allOptions.moveTarget
    : itemIsMarkedForMove
    ? allOptions.markedForMove
    : allOptions.normal;

  function detachItem() {
    client
      .unlink({ what: item["_what"], _id: item["_id"] })
      .then(() => dispatch("refresh"))
      .catch(() => alert("error on detach"));
  }

  function deleteItem() {
    client
      .get({ method: "delete", what: item["_what"], _id: item["_id"] })
      .then(() => dispatch("refresh"))
      .catch(() => alert("error on delete"));
  }

  function moveItem(location) {
    client
      .move({
        location:
          location === LOCATION.ABOVE
            ? "above"
            : location === LOCATION.BELOW
            ? "below"
            : "child",
        what: $movingItem.what,
        id: $movingItem._id,
        to_what: item._what,
        to_id: item._id,
      })
      .then(() => {
        dispatch("refresh");
        $movingItem = null;
      })
      .catch(() => alert("error on move"));
  }
</script>
