<script>
  export let item;
  
  const date = item.date
  const darkMode = true
      
  // const backgroundColor = "aqua"
  // $: backgroundColor = item.label == undefined
  //   ? (darkMode ? '#452b09' : 'antiquewhite')
  //   : item.label == 'feat'
  //     ? (darkMode ? '#008060' : 'aquamarine')
  //     : (darkMode ? 'cornflowerblue' : 'aqua' )
    
  // const backgroundColor = "aqua"
  
  const backgroundColors = {
    'REMOVE': 'remove',
    'REMOVE/health': 'remove',
    'core': 'core',
    'core - priv?': 'core',
    'core - todo': 'core',
    'firma': 'firma',
    'firma - useless?': 'useless',
    'health - useless?': 'useless',
    'money': 'money',
    'nomad': 'nomad',
    'priv/firma': 'firma',
    'programming - bodypace': 'bodypace'
  }
  
  const backgroundColor = backgroundColors[item.category]

</script>

<div class="item {backgroundColor}">
  <div class="header">
    <div>
      {item.category}
    </div>
    {#if item.email}
      <div>
        {#if item.username && item.username !== item.email}
          ({item.username})
        {/if}
        {item.email}
      </div>
    {/if}
  </div>
  <div class="title">
    {item.title} <span style="color: grey;">******</span>
  </div>
  {#if item.url}
    <div class="body">
      {item.url}
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
  div.body {
    padding: 10px;
    color: grey;
    font-size: 24px;
    word-break: break-all;
  }
  div.useless {
    background-color: brown; 
  }
  div.remove {
    background-color: hotpink; 
  }
  div.core {
    background-color: cornflowerblue; 
  }
  div.firma {
    background-color: green;
  }
  div.money {
    background-color: dodgerblue;
  }
  div.nomad {
    background-color: burlywood; 
  }
  div.bodypace {
    background-color: aquamarine;
  }
</style>
