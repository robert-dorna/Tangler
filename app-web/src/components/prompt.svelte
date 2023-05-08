<script>
  import Icon from "./icon.svelte";
  import { createEventDispatcher } from "svelte";
  import { lang } from "../utils";

  const texts = lang.components.prompt;

  const dispatch = createEventDispatcher();
</script>

<div class="row justify container">
  <div class="row align prompt elevated">
    <div class="row flex align title">{texts.title}</div>
    <div class="row center option clickable" on:click|stopPropagation={() => dispatch("create")} on:keypress={undefined}>
      <Icon name="check" color="black" size="large" />
      {texts.create}
    </div>
    <div class="row center option clickable" on:click|stopPropagation={() => dispatch("discard")} on:keypress={undefined}>
      <Icon name="close" color="black" size="large" />
      {texts.discard}
    </div>
  </div>
</div>

<style>
  div.container {
    position: absolute;
    z-index: 1;
    left: 0px;
    bottom: var(--gap-max);
    width: 100%;
  }
  div.prompt {
    width: var(--prompt-width);
    padding-left: var(--gap-max);
    padding-right: var(--gap-max);
    border-radius: var(--radius-large);
    background-color: var(--color-white);
  }
  div.title {
    font-size: var(--font-medium);
  }
  div.option {
    padding-left: var(--gap-max);
    padding-right: var(--gap-max);
    padding-top: var(--gap-large); /* was 15 */
    padding-bottom: var(--gap-large);
  }
  div.option:hover {
    background-color: var(--color-anti-flash-white);
  }
</style>
