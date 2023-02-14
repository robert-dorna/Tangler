<script>
  export let checks = [];
  export let selected = [];
  export let allowOnlyOne = false;
  
  function checkStyle(check, sel) {
    return sel.indexOf(check) == -1 ? 'check-outline' : 'check-inline'
  }
  
  function handleClick(check) {
    if (allowOnlyOne) {
      selected = [check]
    }
    else {
      if (selected.indexOf(check) === -1) {
        selected = [...selected, check]
      }
      else {
        selected = selected.filter(v => v !== check)
      }
    }
  }
</script>

<div class="container">
  {#each checks as check}
    <div on:click={() => handleClick(check)} class="check {checkStyle(check, selected)}">
      {check}
    </div>
  {/each}
</div>
  
<style>
  div.container {
    display: flex;
    justify-content: center;
  }
  div.check {
    display: flex;
    border-radius: 10px;
    margin: 10px;
    padding: 10px;
    padding-left: 15px;
    padding-right: 15px;
  }
  div.check-inline {
    background-color: chocolate;
  }
  div.check-outline {
    background-color: navajowhite;
  }
</style>
  