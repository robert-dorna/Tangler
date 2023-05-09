<script>
  import Icon from "./icon.svelte";
  import { createEventDispatcher } from "svelte";
  import { lang } from "../utils";

  const texts = lang.components.prompt;

  const dispatch = createEventDispatcher();
</script>

<div class="row justify floating max-width prompt-container">
  <div class="row align elevated prompt">
    <div class="row flex align title">{texts.title}</div>
    <div class="row center clickable option" on:click|stopPropagation={() => dispatch("create")} on:keypress={undefined}>
      <Icon name="check" color="black" size="large" />
      {texts.create}
    </div>
    <div class="row center clickable option" on:click|stopPropagation={() => dispatch("discard")} on:keypress={undefined}>
      <Icon name="close" color="black" size="large" />
      {texts.discard}
    </div>
  </div>
</div>

<style>
  .prompt-container {
    left: 0px;
    bottom: var(--gap-max);
  }
  .prompt {
    width: var(--prompt-width);
    padding-left: var(--gap-max);
    padding-right: var(--gap-max);
    border-radius: var(--radius-large);
    background-color: var(--color-white);
  }
  .title {
    font-size: var(--font-medium);
  }
  .option {
    padding-left: var(--gap-max);
    padding-right: var(--gap-max);
    padding-top: var(--gap-large);
    padding-bottom: var(--gap-large);
  }
  .option:hover {
    background-color: var(--color-anti-flash-white);
  }
</style>
