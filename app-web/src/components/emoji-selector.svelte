<script>
  import { onMount } from "svelte";
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  let picker = null;

  onMount(async () => {
    // todo: if localStorage is required,
    // make sure localStorage is available before loading (browser $app/env)

    const { createPicker } = await import("picmo");
    const rootElement = document.querySelector("#pickerContainer");
    picker = createPicker({ rootElement });
    picker.addEventListener("emoji:select", (event) => {
      dispatch("emoji", event.emoji);
    });
  });
</script>

<div id="pickerContainer" />
