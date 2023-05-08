<!-- 
THIS CODE IS A MODIFIED VERSION OF svelte-dragdroplist NPM PACKAGE TAKEN FROM
https://github.com/jwlarocque/svelte-dragdroplist AND DISTRIBUTED UNDER ISC LICENSE

Original author: John LaRocque https://github.com/jwlarocque

ISC License

Copyright 2020 John LaRocque <john@jwlarocque.com>

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee
is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE
INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE
FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
-->

<script>
    import {flip} from "svelte/animate";
    
    export let data = [];
    // export let removesItems = false;

    let ghost;
    let grabbed;

    let lastTarget;

    let mouseY = 0; // pointer y coordinate within client
    let offsetY = 0; // y distance from top of grabbed element to pointer
    let layerY = 0; // distance from top of list to top of client

    function grab(clientY, element) {
        // modify grabbed element
        grabbed = element;
        grabbed.dataset.grabY = clientY;

        // modify ghost element (which is actually dragged)
        ghost.innerHTML = grabbed.innerHTML;

        // record offset from cursor to top of element
        // (used for positioning ghost)
        offsetY = grabbed.getBoundingClientRect().y - clientY;
        drag(clientY);
    }

    // drag handler updates cursor position
    function drag(clientY) {
        if (grabbed) {
            mouseY = clientY;
            layerY = ghost.parentNode.getBoundingClientRect().y;
        }
    }

    // touchEnter handler emulates the mouseenter event for touch input
    // (more or less)
    function touchEnter(ev) {       
        drag(ev.clientY);
        // trigger dragEnter the first time the cursor moves over a list item
        let target = document.elementFromPoint(ev.clientX, ev.clientY).closest(".item");
        if (target && target != lastTarget) {
            lastTarget = target;
            dragEnter(ev, target);
        }
    }

    function dragEnter(ev, target) {
        // swap items in data
        if (grabbed && target != grabbed && target.classList.contains("item")) {
            moveDatum(parseInt(grabbed.dataset.index), parseInt(target.dataset.index));
        }
    }

    // does the actual moving of items in data
    function moveDatum(from, to) {
        let temp = data[from];
        data = [...data.slice(0, from), ...data.slice(from + 1)];
        data = [...data.slice(0, to), temp, ...data.slice(to)];
    }

    function release(ev) {
        grabbed = null;
    }

    function removeDatum(index) {
        data = [...data.slice(0, index), ...data.slice(index + 1)];
    }
</script>

<main class="dragdroplist">
    <div 
        bind:this={ghost}
        id="ghost"
        class={grabbed ? "item haunting" : "item"}
        style={"top: " + (mouseY + offsetY - layerY) + "px"}><p></p></div>
    <div 
        class="list"
        on:mousemove|stopPropagation={(ev) => drag(ev.clientY)}
        on:touchmove|stopPropagation={(ev) => drag(ev.touches[0].clientY)}
        on:mouseup|stopPropagation={release}
        on:touchend|stopPropagation={(ev) => release(ev.touches[0])}>
        {#each data as datum, i (datum.name)}
            <div 
                id={(grabbed && datum.name == grabbed.dataset.name) ? "grabbed" : ""}
                class="item" 
                data-index={i}
                data-name={datum.name}
                data-grabY="0"
                on:mousedown={function(ev) { grab(ev.clientY, this); }}
                on:touchstart={function(ev) { grab(ev.touches[0].clientY, this); }}
                on:mouseenter|stopPropagation={function(ev) { dragEnter(ev, ev.target); }}
                on:touchmove|stopPropagation|preventDefault={function(ev) { touchEnter(ev.touches[0]); }}
                animate:flip|local={{duration: 200}}
            >
                <slot item={datum}/>
            </div>
        {/each}
    </div>
</main>

<style>
    main {
        position: relative;
    }

    .list {
        cursor: grab;
        z-index: 5;
        display: flex;
        flex-direction: column;
    }

    .item {
        box-sizing: border-box;
        display: inline-flex;
        width: 100%;
        min-height: 3em;
        margin-bottom: 0.5em;
        user-select: none;
    }

    .item:last-child {
        margin-bottom: 0;
    }

    .item:not(#grabbed):not(#ghost) {
        z-index: 10;
    }

    .item > * {
        margin: auto;
    }

    #grabbed {
        opacity: 0.0;
    }

    #ghost {
        pointer-events: none;
        z-index: -5;
        position: absolute;
        top: 0;
        left: 0;
        /* opacity: 0.0; */
        background-color: white;
        border-radius: 8px;
        border: 1px solid silver;
    }

    #ghost * {
        pointer-events: none;
    }

    #ghost.haunting {
        z-index: 20;
        opacity: 1.0;
    }
</style>