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
    <span>{item.category}/{item.group} -- {item.account} -- {item.address}</span>
    <span>
      ({item.method})
      {#if date}
        {date}
      {/if}
    </span>
  </div>
  <div class="title">
    {item.title} <span class="paid">{item.paid}</span>
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
  div.title {
    font-size: 32px;
    flex-direction: row;
    justify-content: space-between;
  }
  span.paid {
    text-align: right;
    min-width: 10vw;
    color: grey;
  }
  div.body {
    padding: 10px;
    color: grey;
    font-size: 24px;
  }
</style>
