<script>
  import Options from "svelte-material-icons/FormatListBulletedType.svelte";
</script>

<div class="container">
  <div class="options">
    <Options color="white" size={32} />
  </div>
  <input placeholder="Search for items that contain..." />
</div>

<style>
  div.container {
    display: flex;
    flex-direction: row;
    align-items: center;
    background-color: #172a3a;
    width: 100vw;
    padding-top: 15px;
    padding-bottom: 15px;
  }
  div.options {
    margin-top: 3px;
    padding-left: 30px;
  }
  input {
    all: unset;
    background-color: #172a3a;
    color: #f4f3ee;
    border: 1px solid #bcb8b1;
    border-radius: 8px;
    width: 30vw;
    height: 40px;
    font-size: 18px;
    padding-left: 15px;
    margin-left: 25px;
  }
</style>
