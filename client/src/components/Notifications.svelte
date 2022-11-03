<script lang="ts">
  import { notifications, popups, shouldShowNotifications } from '../lib/store'

  const deleteNotif = (e: Event) => {
    const btn = e.target as HTMLButtonElement
    const idxToRemove = Number(btn.dataset.notifIndex)
    $notifications = $notifications.filter((item, idx) => idx !== idxToRemove)
  }

  const clearNotifs = (e: Event) => {
    $notifications = []
  }
</script>

<div class="notifications" class:hide={!$shouldShowNotifications}>
  <div class="header-controls">
    <button
      id="notif-toggler"
      on:click={() => ($shouldShowNotifications = !$shouldShowNotifications)}
      >{$shouldShowNotifications ? '>' : '<'}</button
    >
    {#if $shouldShowNotifications}
      <span>Notifications</span>
      <button name="clear" type="button" on:click={clearNotifs}>Clear</button>
    {/if}
  </div>
  {#if $shouldShowNotifications}
    {#each $notifications as { type, code, message }, i}
      <div
        class="notif-msg"
        class:error={/Error/.test(type)}
        class:success={type === 'Success'}
        class:info={type === 'Info'}
      >
        <p>{message}</p>
        <button on:click={deleteNotif} data-notif-index={i}>x</button>
      </div>
    {/each}
  {/if}
</div>

<style lang="scss">
  .notifications {
    position: fixed;
    background: rgba(78, 78, 78, 0.58);
    height: calc(100% - 4em);
    width: 350px;
    bottom: 0;
    right: 0;
    opacity: 1;
    transform: translate(0, 0);
    transition: all 0.3s ease-in;
    color: white;
  }

  .header-controls {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .hide {
    background: rgba(78, 78, 78, 0);
    transform: translate(90%, 0);
  }

  .notif-msg {
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
