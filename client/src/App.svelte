<script lang="ts">
  // import router from 'page'
  import { Router, Route, NotFound, redirect } from './router'
  import { activeRoute } from './lib/store'

  import Home from './pages/Home.svelte'
  import Settings from './pages/Settings.svelte'
  import Login from './pages/Login.svelte'
  import Images from './pages/Images.svelte'
  import Galleries from './pages/Galleries.svelte'
  import Content from './pages/Content.svelte'
  import Nav from './components/Nav.svelte'

  const guard = (ctx, next) => {
    // check for example if user is authenticated
    if (true) {
      redirect('/login')
    } else {
      // go to the next callback in the chain
      next()
    }
  }
</script>

{#if $activeRoute.path && !$activeRoute.path.includes('login')}
  <Nav />
{/if}

<!-- <svelte:component this={page} {pathname} /> -->
<Router>
  <Route path="/" component={Home} />
  <Route path="/login" component={Login} />
  <Route path="/settings" component={Settings} />
  <Route path="/images" component={Images} />
  <Route path="/galleries" component={Galleries} />
  <Route path="/content" component={Content} />
</Router>
