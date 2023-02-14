<script>
  import Modal from "./bricks/modal.svelte";
  import Item from "./item.svelte";

  export let visible = false;
  export let onSubmit;

  export let itemtype;
  
  export let item;
  export let source;
  export let edited;

  $: enableBackground = !edited;

  let controlPressed = false;

  $: if (!visible) {
    controlPressed = false;
    edited = false;
  }

  function handleBackgroundClick() {
    if (enableBackground) visible = !visible;
  }

  function handleKeyDown(event) {
    if (!visible) return;
    if (event.key === "Control") controlPressed = true;
  }

  function handleKeyUp(event) {
    if (!visible) return;
    if (event.key === "Control") controlPressed = false;
    else if (event.key === "Escape") visible = false;
    else if (event.key === "Enter" && controlPressed) {
      controlPressed = false;
      if (!edited) visible = false;
      else onSubmit();
    }
  }
</script>

<Modal
  style="justify-content: center; align-items: center;"
  on:click={handleBackgroundClick}
  on:keydown={handleKeyDown}
  on:keyup={handleKeyUp}
  bind:visible
>
  <Item {itemtype} bind:item {source} bind:edited />
</Modal>
