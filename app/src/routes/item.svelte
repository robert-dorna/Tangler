<script>
  export let item;
  export let displayConfig = {};
  export let indent = 15;

  let layout = displayConfig[item['_what']]
  
  $: children = item['_children']
	
	let open = true;
	
	function toggleOpen() {
		open = !open;
	}

  // $: displayItem = width === undefined || width > 1000
  // background-color: dodgerblue;
  // background-color: cornflowerblue;
  // background-color: lightcoral;
  // background-color: antiquewhite;
  // background-color: green;
  // background-color: dodgerblue;
  // background-color: burlywood;
  // background-color: aquamarine;
  // background-color: cornflowerblue;
  // background-color: hotpink;
  // background-color: brown;
</script>


<div class="container" style="padding-left: {indent}px;" on:click={toggleOpen}>
  <div class="title">
    <!-- what: {item['_what']} -->
    {#each layout as element (element)}
      <span style={element.style}>
        {element.field
          ? (element.pretext || "") + item[element.field]
          : element.text}
      </span>
    {/each}
  </div>
</div>


{#if open}
	{#each children as child}
		<svelte:self item={child} {displayConfig} indent={indent + 32}/>
	{/each}
{/if}

<style>
  div.container {
    display: flex;
    flex-wrap: wrap-reverse;
    flex-direction: row;
    align-items: center;
    border-radius: 8px;
    padding: 15px;
    margin: 3px;
    user-select: none;
    cursor: pointer;
  }
  div.container:hover {
    background-color: #BCB8B1;
    opacity: 80%;
  }
  div.title {
    display: flex;
    font-size: 22px;
  }
</style>
