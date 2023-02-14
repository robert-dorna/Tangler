<script>
  export let style = '';
  export let highlightHover = false;
  
  $: highlight = highlightHover ? 'highlight' : ''
</script>

<div
  class="container {highlight}"
  {style}
  on:keydown={() => undefined}
>
  <!-- on:click|self -->
  <slot />
</div>

<style>
  div.container {
    display: flex;
    position: relative;

    flex-direction: column;
    margin: 10px;
    padding: 20px;
    
    /* cursor: pointer; */
  }
  div.highlight:hover {
    opacity: 80%;
  }
</style>