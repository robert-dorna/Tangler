<script>
  import Separator from "./item-parts/separator.svelte";
  import Options from "./item-parts/options.svelte";
  import Date from "./item-parts/date.svelte";
  import Spaced from "./bricks/spaced.svelte";
  import Row from "./bricks/row.svelte";
  import Title from "./item-parts/title.svelte";
  import Body from "./item-parts/body.svelte";
  import Content from "./item-parts/content.svelte";
  import Slate from "./item-parts/slate.svelte";
  import TrashCan from "svelte-material-icons/TrashCan.svelte";

  export let controlMode = false;

  export let item;

  export let source = undefined;
  export let edited = false;

  export let onClick = undefined;
  export let onDelete = undefined;

  $: editable = source !== undefined;
  $: highlightHover = onClick !== undefined && !controlMode;

  const priorityColors = { p1: "red", p2: "orange", p3: "yellow", p4: "white" };
  const labelColors = {
    feat: ["aquamarine", "#008060"], // light, dark
    cleanup: ["aqua", "cornflowerblue"],
    unknown: ["antiquewhite", "#452b09"],
  };
  $: backgroundColor = `background-color: ${
    (labelColors[item.label] || labelColors.unknown)[1]
  };`;
  $: borderLeft = `border-left: 10px solid ${priorityColors[item.priority]};`;
  // $: style = `${backgroundColor} ${borderLeft}`;
  // $: style = `${borderLeft}`;
  $: style = ``;

  const changeHighlights = [
    ["title", "color: goldenrod;"],
    ["label", "color: goldenrod;"],
    ["priority", "color: goldenrod;"],
    ["project", "color: goldenrod;"],
    ["due_date", "color: goldenrod;"],
    ["body", "color: goldenrod;"],
  ];

  $: styles =
    source === undefined
      ? changeHighlights.reduce((c, style) => ({ ...c, [style[0]]: "" }), {})
      : changeHighlights.reduce(
          (c, style) => ({
            ...c,
            [style[0]]: source[style[0]] !== item[style[0]] ? style[1] : "",
          }),
          {}
        );

  $: {
    let newEdited = false;
    for (let style in styles) {
      if (styles[style] !== "") {
        newEdited = true;
      }
    }
    edited = newEdited;
  }

  const labels = ["feat", "cleanup"];
  const projects = ["priv", "health", "nomad", "JDG"];
  const priorities = ["p1", "p2", "p3", "p4"];
</script>

<Content {style} {highlightHover}>
  ✅<Title bind:value={item.title} {editable} style={styles.title} />
  <Spaced>
    <Row>
      {#if editable}
        <Options
          options={priorities}
          bind:value={item.priority}
          {editable}
          style={styles.priority}
        />
        <Separator />
      {/if}
      <Options
        options={projects}
        bind:value={item.project}
        {editable}
        style={styles.project}
      />
      <Separator />
      <Options
        options={labels}
        bind:value={item.label}
        {editable}
        style={styles.label}
      />
    </Row>
    <Date bind:value={item.due_date} {editable} style={styles.due_date} />
  </Spaced>
  <!-- <Body bind:value={item.body} {editable} style={styles.body} /> -->
  {#if !editable}
    <Slate on:click={() => { if (!controlMode) onClick() }} visible={controlMode}>
      <div class="button" on:click={onDelete} on:keydown={undefined}>
        <TrashCan color="white" size="40" />
      </div>
    </Slate>
  {/if}
</Content>

<style>
  div.button {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 15px;
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background-color: lightsalmon;
    /* box-shadow: ; */
    box-shadow: rgba(0, 0, 0, 0.3) 0px 19px 38px,
      rgba(0, 0, 0, 0.22) 0px 15px 12px;
    /* opacity: 90%; */
  }
  div.button:hover {
    /* opacity: 100%;  */
    background-color: crimson;
    cursor: pointer;
  }
</style>
