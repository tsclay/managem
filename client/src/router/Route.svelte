<script>
  import { register } from './Router.svelte'
  import { activeRoute } from '../lib/store'

  export let path = '/'
  export let component = null
  export let middleware = []

  // page.js params placeholder
  let params = {}

  register({ path, component, middleware })

  $: if ($activeRoute.path === path) {
    params = $activeRoute.params
  }
</script>

<!-- if this is current active route -->
{#if $activeRoute.path === path}
  <!-- prefer component over slot -->
  {#if $activeRoute.component}
    <svelte:component
      this={$activeRoute.component}
      {...$$restProps}
      {...params}
    />
  {:else}
    <slot {params} />
  {/if}
{/if}
