<script>
  import Icon from "../../../components/icon.svelte";
</script>

<div class="container" on:click|stopPropagation on:keypress={undefined}>
  <Icon name="check" color="grey" size={30} />
</div>

<style>
  div.container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 5px;
    margin-left: 19px;
  }
  div.container:hover {
    border-radius: 8px;
    background-color: #bcb8b1;
  }
</style>
