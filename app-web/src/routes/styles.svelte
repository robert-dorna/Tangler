<style>
  :global(:root) {
    /* fonts */

    --app-font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS", sans-serif;

    /* sizes */
    --font-small: 18px;
    --font-medium: 20px;
    --font-large: 22px;
    --font-header: 26px;

    --gap-line: 1px;
    --gap-tiny: 2px;
    --gap-small: 5px;
    --gap-medium: 10px;
    --gap-large: 20px;
    --gap-max: 30px;

    --radius-small: 8px;
    --radius-large: 40px;

    --panel-width: 20vw;
    --items-width: 700px;
    --item-width: 65vw;
    --prompt-width: 40vw;
    --menu-height: 40vh;

    /* --width-chunk */

    /* palette */
    --color-white: white;
    --color-black: black;

    --color-mint-cream: #f5fffa;
    --color-anti-flash-white: #eef0f2;
    --color-nyanza: #e9ffdb;
    --color-tea-green: #d0f0c0;
    --color-pistachio: #93c572;

    --color-taupe: #463f3a;
    --color-battleship-grey: #8a817c;
    --color-silver: #bcb8b1;
    --color-isabelline: #f4f3ee;
    --color-melon: #e0afa0;

    --color-sandy-brown: #fc9e4f;
    --color-cinnabar: #f4442e;
    --color-field-drab: #6a5837;
    --color-prussian-blue: #172a3a;

    /* effects */
    --opacity-hover: 80%;

    /* +page */
    --page-color-bg: white;

    /* panel */
    --panel-color-bg: var(--color-mint-cream);
    --panel-color-border: var(--color-nyanza);
    --panel-color-hover: var(--color-tea-green);
    --panel-color-button-hover: var(--color-pistachio);
  }

  /* effects */
  :global(div.elevated) {
    box-shadow: 8px 8px 24px 0px rgba(66, 68, 90, 1);
  }

  :global(div.floating-panel) {
    position: absolute;
    z-index: 1;
  }

  :global(div.floating-editor) {
    position: absolute;
    z-index: 2;
  }

  :global(div.floating-menu) {
    position: absolute;
    z-index: 30;
  }

  :global(div.hidden) {
    visibility: hidden;
  }

  :global(div.clickable) {
    user-select: none;
    cursor: pointer;
  }

  /* layout */
  :global(.screen-size) {
    width: 100vw;
    height: 100vh;
  }

  :global(.max-width) {
    width: 100%;
  }

  :global(.flex) {
    display: flex;
    flex: 1;
  }

  :global(.row) {
    display: flex;
    flex-direction: row;
  }

  :global(.row-reverse) {
    display: flex;
    flex-direction: row-reverse;
  }

  :global(.column) {
    display: flex;
    flex-direction: column;
  }

  :global(.align) {
    align-items: center;
  }

  :global(.justify) {
    justify-content: center;
  }

  :global(.center) {
    align-items: center;
    justify-content: center;
  }

  :global(.wrap-reverse) {
    flex-wrap: wrap-reverse;
  }
</style>
