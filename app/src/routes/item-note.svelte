<script>
  export let item;
  
  const date = item.date
  const darkMode = true
      
  $: backgroundColor = item.label == undefined
    ? (darkMode ? '#452b09' : 'antiquewhite')
    : item.label == 'feat'
      ? (darkMode ? '#008060' : 'aquamarine')
      : (darkMode ? 'cornflowerblue' : 'aqua' )
</script>

<div class="item" style="background-color: {backgroundColor};">
  <div class="header">
    {#if date}
      <div>
        {date}
      </div>
    {/if}
  </div>
  <div class="title">
    {item.title}
  </div>
  {#if item.body}
    <div class="body">
      {item.body}
    </div>
  {/if}
</div>

<style>
  div {
    display: flex;
    flex-direction: column;
  }
  div.item {
    margin: 10px;
    padding: 10px;
    padding-left: 20px;
    padding-right: 20px;
    background-color: antiquewhite;
  }
  div.header {
    flex-direction: row;
    justify-content: space-between;
    font-size: 18px;
  }
  div.note {
  }
  div.title {
    font-size: 32px;
  }
  div.body {
    padding: 10px;
    color: grey;
    font-size: 24px;
  }
</style>
