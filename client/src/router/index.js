// credit to https://github.com/codechips/svelte-pagejs

import page from 'page';
import Router from './Router.svelte';
import Route from './Route.svelte';
import NotFound from './NotFoundError.svelte';

const redirect = path => page.redirect(path);

export { Router, Route, NotFound, redirect };