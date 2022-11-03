<script lang="ts">
  import { popups } from '../lib/store'
  import { crossfade } from 'svelte/transition'
  import { flip } from 'svelte/animate'
  import { quintOut } from 'svelte/easing'

  const deleteNotif = (e: Event) => {
    const btn = e.target as HTMLButtonElement
    const popupId = btn.dataset.id
    $popups.forEach((item) => {
      if (item.id === popupId) {
        console.log('found it!')
        clearTimeout(item.timerId)
      }
    })
    $popups = $popups.filter((item, idx) => item.id !== popupId)
  }

  const autoRemove = (id) => {
    console.log('inside autoRemove ', id)
    $popups = $popups.filter((item, idx) => item.id !== id)
  }

  const [send, receive] = crossfade({
    duration: (d) => Math.sqrt(d * 200),

    fallback(node, params) {
      const style = getComputedStyle(node)
      const transform = style.transform === 'none' ? '' : style.transform

      return {
        duration: 800,
        easing: quintOut,
        css: (t) => `
					transform: ${transform} translate(${(1 - t) * 200}px, ${
          (1 - t) * 0
        }px) scale(${t});
					opacity: ${t}
				`
      }
    }
  })

  $: $popups.forEach((p) => {
    if (!p.timerId) {
      let timer = setTimeout(() => {
        autoRemove(p.id)
      }, 4000)
      p.timerId = timer
    }
  })
</script>

{#if $popups.length !== 0}
  <div class="popups">
    {#each $popups.filter((p, i) => !p.done) as popup, i (popup.id)}
      <div
        data-notif-index={i}
        on:introstart={() => console.log('at start ', i)}
        animate:flip
        in:receive={{ key: popup.id }}
        out:send={{ key: popup.id }}
        class="popup-msg"
        class:error={/Error/.test(popup.type)}
        class:success={popup.type === 'Success'}
        class:info={popup.type === 'Info'}
      >
        <p>{popup.message}</p>
        <button on:click={deleteNotif} data-id={popup.id}>x</button>
      </div>
    {/each}
  </div>
{/if}

<style lang="scss">
  .popups {
    position: fixed;
    height: calc(100% - 4em);
    width: 350px;
    bottom: 0;
    right: 0;
    opacity: 1;
    transform: translate(0, 0);
  }

  .popup-msg {
    position: relative;

    p {
      margin: 0.5em auto;
      width: 95%;
      padding: 2em;
      box-sizing: border-box;
      text-align: center;
    }

    button {
      position: absolute;
      top: 0.5em;
      right: 0.5em;
      width: 1.5em;
      height: 1.5em;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }

  .success {
    background: hsla(116, 96%, 79%, 0.52);
  }
  .error {
    background: hsla(0, 96%, 79%, 0.52);
  }
  .info {
    background: hsla(207, 100%, 61%, 0.52);
  }
</style>
