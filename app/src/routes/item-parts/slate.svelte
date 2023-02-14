<script>
  export let visible = false;
  $: background = visible ? "background" : "";
</script>

<div class="slate full {background}" style="z-index: 1;" on:click|self on:keypress={undefined}/>
{#if visible}
<div class="slate" style="z-index: 2;">
  <slot/>
</div>
{/if}

<style>
  div.slate {
    display: flex;
    position: absolute;
    
    justify-content: end;
    
    top: 0px;
    right: 0px;
  }
  div.full {
    height: 100%;
    width: 100%;
    
    /* background-color: red; */
    cursor: pointer;
  }
  div.background {
    background-color: black;
    opacity: 50%;
    /* cursor: pointer; */
  }
  div.background:hover {
    background-color: white;
    cursor: grab;
  }
</style>