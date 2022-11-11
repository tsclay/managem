<script lang="ts">
  import { redirect } from '../router'
  import { fade } from 'svelte/transition'
  import { csrfToken, currentUser } from '../lib/store'
	import type { UserData } from 'src/types/user.type'

  let messageTimer
  let showRecoveryModal = false
  let messages = []
  
  // messageTimer = setTimeout(() => {
  //   const allMessages = searchForAll(".messages > *");
  //   allMessages.forEach((m) => {
  //     m.addEventListener("transitionend", (e) => {
  //       m.remove();
  //     });
  //     m.classList.toggle("fade-out");
  //   });
  // }, 3000);

  const handleMessageRemoval = () => {
    messageTimer = setTimeout(() => {
      messages = []
      // const allMessages = searchForAll('.messages > *')
      // allMessages.forEach((m) => {
      //   m.addEventListener('transitionend', (e) => {
      //     m.remove()
      //   })
      //   m.classList.toggle('fade-out')
      // })
    }, 3000)
  }

  const showClientMessage = (message) => {
    // if (messageTimer) clearTimeout(messageTimer)
    messages = [...messages, message]
    messages.pop()
    messages = messages
    // nestElements(div, [
    //   createElement(
    //     'p',
    //     {
    //       class: `${'error' in message ? 'error-msg' : 'success-msg'}`
    //     },
    //     `${'error' in message ? message.error : message.message}`
    //   )
    // ])
    // return handleMessageRemoval()
  }

  const attemptLogin = async (e) => {
    e.preventDefault()
    const payload = {
      username: e.target[0].value,
      password: e.target[1].value
    }
    const response = await fetch('/login', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': $csrfToken
      },
      credentials: 'same-origin',
      body: JSON.stringify(payload)
    })
    console.log(response)
    if (response.status === 200) {
      const user = await response.json()
      $currentUser = {
        username: user.username,
        first_name: user.first_name,
        last_name: user.last_name,
        role: user.role
      }
      localStorage.setItem('managemUser', $currentUser.username)
      return redirect('/')
    }
    // const message = await response.json()
    // return showClientMessage(message)
  }

  const sendRecoveryEmail = async (e) => {
    e.preventDefault()
    const { 0: username, 1: firstName, 2: lastName, 3: email } = e.target
    const request = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username.value,
        first_name: firstName.value,
        last_name: lastName.value,
        email: email.value
      })
    }
    const response = await fetch('/admin/users/recovery', request).then((r) =>
      r.json()
    )

    console.log(response)
  }
</script>

<div class="login-page">
  <div class="logo">
    <svg
      width="100%"
      height="100%"
      version="1.1"
      viewBox="0 0 189.97 46.567"
      xmlns="http://www.w3.org/2000/svg"
    >
      <g
        transform="translate(-8.5391 -23.661)"
        style="fill: #d5e5ff; opacity: 0.67846;"
      >
        <path
          d="m145.65 34.761 26.338 35.226 26.338-35.226-8.5878-10.883h-35.133z"
          style="fill: #d5e5ff; stroke-width: 0.072696; stroke: #000;"
        />
        <path
          d="m145.65 34.768h52.677"
          style="fill: #d5e5ff; stroke-width: 0.061008; stroke: #000;"
        />
        <path
          d="m154.73 34.761 17.299 35.226"
          style="fill: #d5e5ff; stroke-width: 0.061008; stroke: #000;"
        />
        <path
          d="m165 34.761 7.0241 35.226"
          style="fill: #d5e5ff; stroke-width: 0.061008; stroke: #000;"
        />
        <path
          d="m189.62 34.761-17.627 35.226"
          style="fill: #d5e5ff; stroke-width: 0.061008; stroke: #000;"
        />
        <path
          d="m179.77 34.761-7.7835 35.226"
          style="fill: #d5e5ff; stroke-width: 0.061008; stroke: #000;"
        />
        <path
          d="m154.73 34.754 5.6294-10.876"
          style="fill: #d5e5ff; stroke-width: 0.061008; stroke: #000;"
        />
        <path
          d="m165 34.754 3.3284-10.876"
          style="fill: #d5e5ff; stroke-width: 0.061008; stroke: #000;"
        />
        <path
          d="m179.77 34.754-2.7164-10.876"
          style="fill: #d5e5ff; stroke-width: 0.061008; stroke: #000;"
        />
        <path
          d="m189.62 34.754-4.5426-10.876"
          style="fill: #d5e5ff; stroke-width: 0.061008; stroke: #000;"
        />
      </g>
      <path d="m134.08 0.68017h-133.94" style="fill: none; stroke: #000;" />
      <path d="m134.08 45.887h-133.94" style="fill: none; stroke: #000;" />
      <text
        transform="scale(1.0544 .94842)"
        x="-1.8998765"
        y="27.899826"
        style="
          fill: #000000;
          font-family: sans-serif;
          font-size: 29.259px;
          line-height: 1.25;
          stroke-width: 0.73148;
        "
      >
        <tspan
          x="-1.8998765"
          y="27.899826"
          style="font-family: Futura; stroke-width: 0.73148;"
        >
          managem
        </tspan>
      </text>
    </svg>
  </div>
  <div class="login-container">
    <div class="messages">
      {#each messages as m}
        {#if m && Object.hasOwn(m, 'error')}
          <p
            in:fade={{ duration: 400 }}
            out:fade={{ duration: 400, delay: 3000 }}
            class="error-msg"
            style="color: red;"
          >
            {m['error']}
          </p>
        {:else if m && Object.hasOwn(m, 'message')}
          <p
            in:fade={{ duration: 400 }}
            out:fade={{ duration: 400, delay: 3000 }}
            class="success-msg"
            style="color: green;"
          >
            {m['message']}
          </p>
        {/if}
      {/each}
    </div>
    <form on:submit={attemptLogin}>
      <input type="text" name="username" id="username" placeholder="Username" />
      <input
        type="password"
        name="password"
        id="password"
        placeholder="Password"
      />
      <button type="submit">Enter</button>
    </form>
    <button class="login-link" on:click={() => redirect('/')}
      >Main Website</button
    >
    <button class="login-link" on:click={() => (showRecoveryModal = true)}
      >Recover Account</button
    >
  </div>
  {#if showRecoveryModal}
    <div class="acct-recovery">
      <div
        style="
      width: 100%;"
      >
        <h4>Account Recovery</h4>
        <p>
          Fill all of the following fields with your information. You'll receive
          an email with a reset link.<br />
        </p>
      </div>
      <form
        style="
      display: block;
      width: 100%;
      height: auto;"
        on:submit={sendRecoveryEmail}
      >
        <input
          type="text"
          name="username"
          placeholder="Username"
          style="
        width: 100%;
        box-sizing: border-box;"
        /><input
          type="text"
          name="first_name"
          placeholder="First Name"
          style="
        width: 100%;
        box-sizing: border-box;"
        /><input
          type="text"
          name="last_name"
          placeholder="Last Name"
          style="
        width: 100%;
        box-sizing: border-box;"
        /><input
          type="text"
          name="email"
          placeholder="Email Address"
          style="
        width: 100%;
        box-sizing: border-box;"
        /><button
          type="submit"
          style="
          margin-top: 2rem;
          width: 100%;">Confirm</button
        >
      </form>
      <button
        type="button"
        style="position: absolute;
        top: 4px;
        right: 4px;
        height: 20px;
        width: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 15px;
        padding: 0;"
        on:click={(e) => (showRecoveryModal = false)}>X</button
      >
    </div>
  {/if}
</div>

<style>
  .login-page {
    /* height: clamp(450px, 60%, 1000px); */
    height: 100%;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(3, 1fr);
  }

  .login-container {
    grid-area: 2/2/2/2;
    align-self: center;
    justify-self: center;
    width: clamp(365px, 100%, 400px);
  }

  .login-container > form {
    display: flex;
    flex-flow: column nowrap;
  }

  .login-container > form > button {
    margin: 0.75rem 0;
  }

  .login-container > * {
    width: 90%;
    margin: 1rem auto;
  }

  .login-container > h1 {
    text-align: center;
  }

  .logo {
    grid-area: 1/1/1/4;
    align-self: end;
    justify-self: center;
    width: clamp(235px, 90%, 765px);
    padding-top: 1rem;
  }

  .logo > svg {
    display: block;
  }

  .login-link {
    text-align: center;
    display: block;
    margin: 0 auto;
    width: 50%;
    /* text-decoration: underline; */
    background-color: var(--gray);
    color: white;
    cursor: pointer;
  }

  .messages {
    height: 20px;
  }

  /* .messages > * {
    opacity: 1;
    transition: opacity 300ms linear;
  } */

  input[name='csrf_token'] {
    display: none;
  }

  p.error-msg {
    color: red;
  }

  p.success-msg {
    color: green;
  }

  .acct-recovery {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: clamp(320px, 75%, 400px);
    height: 75%;
    padding: 2rem;
    box-sizing: border-box;
    background: var(--gray);
  }
</style>
