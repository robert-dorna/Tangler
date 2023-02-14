<script>
  export let item;

  const backgroundColors = {
    'to buy': 'tobuy',
    'owned': 'owned',
    'remove': 'remove',
  }
  
  const backgroundColor = backgroundColors[item.status]
</script>

<div class="item {backgroundColor}">
  <div class="header">
    {item.category} / {item.status}
    {#if item.place}
      <div>
        {item.place}
      </div>
    {/if}
  </div>
  <div class="title">
    {item.title}
    {#if item.price}
      <span style="color: grey;">{item.price}</span>
    {/if}
  </div>
  {#if item.description}
    <div class="body">
      {item.description}
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
  }
  div.tobuy {
    background-color: dodgerblue;
  }
  div.owned {
    background-color: cornflowerblue; 
  }
  div.remove {
    background-color: lightcoral;
  }

</style>
