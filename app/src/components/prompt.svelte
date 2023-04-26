<script>
  import Icon from "./icon.svelte";
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();
</script>

<div class="container">
  <div class="prompt g-elevated">
    <div class="title">What to do with new item?</div>
    <div
      class="option"
      on:click|stopPropagation={() => dispatch("create")}
      on:keypress={undefined}
    >
      <Icon name="check" color="black" size={30} />
      Create
    </div>
    <div
      class="option"
      on:click|stopPropagation={() => dispatch("discard")}
      on:keypress={undefined}
    >
      <Icon name="close" color="black" size={30} />
      Discard
    </div>
  </div>
</div>

<style>
  div.container {
    display: flex;
    z-index: 1;
    bottom: 30px;
    left: 0px;
    position: absolute;
    width: 100%;
    justify-content: center;
  }
  div.prompt {
    display: flex;
    width: 40vw;
    padding-left: 40px;
    padding-right: 40px;
    align-items: center;
    border-radius: var(--radius-large);
    background-color: white;
  }
  div.title {
    display: flex;
    flex: 1;
    font-size: 20px;
    align-items: center;
  }
  div.option {
    display: flex;
    padding-left: 30px;
    padding-right: 30px;
    padding-top: 15px;
    padding-bottom: 15px;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    user-select: none;
  }
  div.option:hover {
    background-color: #eef0f2;
  }
</style>
