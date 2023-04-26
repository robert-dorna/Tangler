<style>
  :global(:root) {

    /* fonts */
    --app-font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS",
      sans-serif;

    /* sizes */
    --font-medium: 18px;

    --gap-line: 1px;
    --gap-tiny: 2px;
    --gap-small: 5px;
    --gap-medium: 10px;
    --gap-large: 20px;

    --radius-small: 8px;
    --radius-large: 40px;

    --panel-width: 20vw;

    /* --width-chunk */

    /* palette */
    --color-mint-cream: #F5FFFA;
    --color-nyanza: #E9FFDB;
    --color-tea-green: #D0F0C0;
    --color-pistachio: #93C572;

    --color-taupe: #463F3A;
    --color-battleship-grey: #8A817C;
    --color-silver: #BCB8B1;
    --color-isabelline: #F4F3EE;
    --color-melon: #E0AFA0;

    --color-sandy-brown: #FC9E4F;
    --color-cinnabar: #F4442E;
    --color-field-drab: #6A5837;
    --color-prussian-blue: #172A3A;

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

  :global(div.g-elevated) {
    box-shadow: 8px 8px 24px 0px rgba(66, 68, 90, 1);
  }

  :global(div.g-flex) {
    display: flex;
    flex: 1;
  }

  :global(div.g-row) {
    display: flex;
    flex-direction: row;
  }

  :global(div.g-row-aligned) {
    display: flex;
    flex-direction: row;
    align-items: center;
  }

  :global(div.g-row-centered) {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
  }

  :global(div.g-column) {
    display: flex;
    flex-direction: column;
  }

  :global(div.g-column-aligned) {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  :global(div.g-clickable) {
    user-select: none;
    cursor: pointer;
  }
</style>
