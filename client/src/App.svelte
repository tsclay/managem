<script lang="ts">
  // import router from 'page'
  import { Router, Route, NotFound, redirect } from './router'
  import { activeRoute, currentUser, csrfToken } from './lib/store'
  import { onMount } from 'svelte'

  import Home from './pages/Home.svelte'
  import Settings from './pages/Settings.svelte'
  import Login from './pages/Login.svelte'
  import Images from './pages/Images.svelte'
  import Galleries from './pages/Galleries.svelte'
  import Content from './pages/Content.svelte'
  import Nav from './components/Nav.svelte'

  const guard = (ctx, next) => {
    // check for example if user is authenticated
    if ($currentUser === null) {
      redirect('/login')
    } else {
      // go to the next callback in the chain
      next()
    }
  }

  const goToHome = (ctx, next) => {
    if ($currentUser !== null && $activeRoute.path.includes('login')) {
      redirect('/')
    } else {
      next()
    }
  }

  // onMount(async () => {
  //   $csrfToken = await getCSRFToken()
  // })
</script>

{#if $activeRoute.path && !$activeRoute.path.includes('login')}
  <Nav />
{/if}

<!-- <svelte:component this={page} {pathname} /> -->
<Router>
  <Route path="/" component={Home} middleware={[guard]}/>
  <Route path="/login" component={Login} middleware={[goToHome]} />
  <Route path="/settings" component={Settings} middleware={[guard]}/>
  <Route path="/images" component={Images} middleware={[guard]} />
  <Route path="/galleries" component={Galleries} middleware={[guard]} />
  <Route path="/content" component={Content} middleware={[guard]} />
</Router>
