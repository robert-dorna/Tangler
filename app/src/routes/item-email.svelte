<script>
  export let item;
  
  const date = item.date
  const darkMode = true
</script>

<div class="item {item.status}">
  <div class="header">
    <span>{item.sender} => {item.receiver}</span>
    {#if date}
      <span>
        {#if item.status === "draft"}
          (draft)
        {/if}
        {date}
      </span>
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
  div.received {
    background-color: cornflowerblue;
  }
  div.sent {
  }
  div.draft {

  }
</style>
