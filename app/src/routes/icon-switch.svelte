<script>
  import Cog from 'svelte-material-icons/Cog.svelte'
  import CogOutline from 'svelte-material-icons/CogOutline.svelte';
  import CodeBraces from 'svelte-material-icons/CodeBraces.svelte';
  import CodeBracesBox from 'svelte-material-icons/CodeBracesBox.svelte';
  import CodeBrackets from 'svelte-material-icons/CodeBrackets.svelte';
  import CodeArray from 'svelte-material-icons/CodeArray.svelte';
  
  const Icons = {
    cog: {
      normal: Cog,
      outline: CogOutline,
    },
    brackets: {
      outline: CodeBrackets,
      normal: CodeArray,
    },
    braces: {
      outline: CodeBraces,
      normal: CodeBracesBox,
    }
  }
  
  export let name;

  let Icon = Icons[name].normal
  let IconOutline = Icons[name].outline
  
  export let lock = false;
  export let selected = true

  function handleClick() {
    if (!lock) {
      selected = !selected
    }
  }
</script>

<div on:click={handleClick}>
  {#if selected}
    <Icon color="chocolate" size=40 />
  {:else}
    <IconOutline color="chocolate" size=40 />
  {/if}
</div>

<style>
  div {
    display: flex;
  }
</style>