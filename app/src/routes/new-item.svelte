
<div id="parent" on:click on:keyup={undefined}>
  <span class="addnew">
    +
  </span>
</div>

<style>
  #parent {
    background-color: aliceblue;
    /* height: 5vh; */
    height: 1vh;
    display: flex;
    color: white;
    font-size: 64px;
    font-weight: bold;
    margin: 0px;
    line-height: 66%;
    user-select: none;
    cursor: pointer;
    justify-content: center;
    align-items: center;
    /* margin: 5px; */
    /* border-radius: 30px; */
    /* width: 10vw; */
    text-align: center;
    vertical-align: center;
    margin-left: 15px;
    margin-right: 15px;
  }
  #parent:hover {
    opacity: 80%;
    /* align-self: center; */
    height: 5vh;
    background-color: grey;
  }
  #parent span.addnew {
    display: none;    
  }
  #parent:hover span.addnew {
    display: flex;    
  }
</style>