<script>
  import Expanded from "svelte-material-icons/ChevronDown.svelte";
  import Expand from "svelte-material-icons/ChevronUp.svelte";
  import Dot from "svelte-material-icons/CircleSmall.svelte";
  import DotsHorizontal from "svelte-material-icons/DotsHorizontal.svelte";
  import DotsVertical from "svelte-material-icons/DotsVertical.svelte";
  import Up from "svelte-material-icons/MenuUpOutline.svelte";
  import Down from "svelte-material-icons/MenuDownOutline.svelte";
  import Top from "svelte-material-icons/FormatVerticalAlignTop.svelte";
  import Tree from "svelte-material-icons/FileTree.svelte";

  import Check from "svelte-material-icons/Check.svelte";
  import Plus from "svelte-material-icons/PlusThick.svelte";
  import PencilPlus from "svelte-material-icons/PencilPlus.svelte";
  import PencilOutline from "svelte-material-icons/PencilOutline.svelte";
  import SelectColor from "svelte-material-icons/SelectColor.svelte";
  import Trash from "svelte-material-icons/DeleteForeverOutline.svelte";
  import Cancel from "svelte-material-icons/Cancel.svelte";
  import Close from "svelte-material-icons/Close.svelte";

  import Cog from "svelte-material-icons/Cog.svelte";
  import CogOutline from "svelte-material-icons/CogOutline.svelte";
  import Hand from "svelte-material-icons/HandFrontLeft.svelte";
  import HandOutline from "svelte-material-icons/HandFrontLeftOutline.svelte";

  import Eraser from "svelte-material-icons/Eraser.svelte"
  import Eye from "svelte-material-icons/Eye.svelte"
  import EyeOutline from "svelte-material-icons/EyeOutline.svelte"


  // prettier-ignore
  const icons = {
    'expanded': Expanded,
    'expand': Expand,
    'dot': Dot,
    'dots-v': DotsVertical,
    'dots-h': DotsHorizontal,
    'up': Up,
    'down': Down,
    'top': Top,
    'tree': Tree,

    'check': Check,
    'plus': Plus,
    'pencil-plus': PencilPlus,
    'pencil-outline': PencilOutline,
    'color-picker': SelectColor,
    'trash': Trash,
    'cancel': Cancel,
    'close': Close,

    'cog': Cog,
    'cog-outline': CogOutline,
    'hand': Hand,
    'hand-outline': HandOutline,

    'eraser': Eraser,
    'eye': Eye,
    'eye-outline': EyeOutline,
  };

  export let name;
  export let color;
  export let size;

  const sizes = {
    small: 20,
    medium: 24,
    large: 30,
  };

  $: icon = name === "dots" ? undefined : icons[name];
  $: actualSize = sizes[size] || sizes.large;

  $: if(icon === undefined && name !== "dots") console.warn('Icon.svelte: unknown icon name:', name)
</script>

{#if name === "dots"}
  <Dot {color} size={actualSize} />
  <Dot {color} size={actualSize} />
{:else}
  <svelte:component this={icon} {color} size={actualSize} />
{/if}
