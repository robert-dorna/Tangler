<script>
  import client from "../client";
  import { LOCATION, movingItem, newItem } from "../stores";

  import HandIcon from "svelte-material-icons/HandFrontLeftOutline.svelte";
  import UpIcon from "svelte-material-icons/MenuUpOutline.svelte";
  import DownIcon from "svelte-material-icons/MenuDownOutline.svelte";
  import TreeIcon from "svelte-material-icons/FileTree.svelte";
  import TopIcon from "svelte-material-icons/FormatVerticalAlignTop.svelte";
  import TrashIcon from "svelte-material-icons/DeleteForeverOutline.svelte";
  import CancelIcon from "svelte-material-icons/Cancel.svelte";

  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  export let item;

  export const allOptions = {
    // prettier-ignore
    normal: [
      { Icon: HandIcon, text: "move", action: () => { $movingItem = { what: item._what, _id: item._id }; } },
      { Icon: UpIcon, text: "create above", action: () => { newItem.select(item, LOCATION.ABOVE) } },
      { Icon: UpIcon, text: "create below", action: () => { newItem.select(item, LOCATION.BELOW) } },
      { Icon: UpIcon, text: "create child", action: () => { newItem.select(item, LOCATION.CHILD) } },
      { Icon: TopIcon, text: "detach top", action: () => { detachItem() } },
      { Icon: TrashIcon, text: "delete", action: () => { deleteItem() } },
    ],

    // prettier-ignore
    moveTarget: [
      { Icon: CancelIcon, text: "cancel move", action: () => { $movingItem = null; } },
      { Icon: UpIcon, text: "place above", action: () => { moveItem(LOCATION.ABOVE); } },
      { Icon: DownIcon, text: "place below", action: () => { moveItem(LOCATION.BELOW); } },
      { Icon: TreeIcon, text: "place as child ", action: () => { moveItem(LOCATION.CHILD); } },
    ],

    // prettier-ignore
    markedForMove: [
      { Icon: CancelIcon, text: "cancel move", action: () => { $movingItem = null; } },
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
