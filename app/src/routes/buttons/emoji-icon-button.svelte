<script>
  export let item;
  export let displayConfig;

  $: emoji  = displayConfig.types[item._what].emoji

  function onClick() {

  }
</script>


<div class="emoji" on:click={onClick} on:keypress={undefined}>
  {emoji}
</div>


<style>
  div.emoji {
    margin-right: 10px;
  }
  div.emoji:hover {
    background-color: brown;
  }
</style>
