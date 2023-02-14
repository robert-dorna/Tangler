<script>
  import configRaw from "../tangle_data/config.yaml?raw";
  import IconSwitch from "./icon-switch.svelte";
  import Checks from "./checks.svelte"
  // import yaml from "yaml";

  // const config = yaml.parse(configRaw);

  // const counts = Object.keys(data).reduce(
  //   (a, key) => ({ ...a, [key]: data[key].length }),
  //   {}
  // );

  // function filterData(filter) {
  //   if (!filter) return null;
  //   let filters = filter.split(".");
  //   if (!(filters[0] in data)) return null;
  //   return filters.reduce(
  //     (r, f) => (Array.isArray(r) ? r.map((o) => o[f]) : f in r ? r[f] : r),
  //     data
  //   );
  // }

  // let filter = "task";
  // $: json = filterData(filter) || counts;

  export let screens;
  export let projects;
  export let priorities;
  export let meanings;
  
  export let screen;
  export let project;
  export let priority;
  export let meaning;
</script>

<div class="container">
  <Checks checks={screens} allowOnlyOne={true} bind:selected={screen} />
  <input />
  <Checks checks={projects} bind:selected={project} />
  <Checks checks={priorities} bind:selected={priority}/>
  <Checks checks={meanings} bind:selected={meaning}/>
</div>

<style>
  div.container {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    background-color: bisque;
    width: 100vw;
    padding-top: 15px;
    padding-bottom: 15px;
  }
  input {
    margin-left: 10px;
    border-radius: 20px;
    padding: 10px;
    border-width: 3;
    border-color: chocolate;
    color: chocolate;
    width: 30vw;
  }
</style>
