<script>
  import Check from "svelte-material-icons/Check.svelte";
  import Close from "svelte-material-icons/Close.svelte";

  export let onConfirm;
  export let onDiscard;
</script>

<div class="container">
  <div class="prompt">
    <div class="title">What to do with new item?</div>
    <div class="option" on:click={onConfirm} on:keypress={undefined}>
      <Check color="black" size={30} />
      Create
    </div>
    <div class="option" on:click={onDiscard} on:keypress={undefined}>
      <Close color="black" size={30} />
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
    border-radius: 40px;
    box-shadow: 8px 8px 24px 0px rgba(66, 68, 90, 1);
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
