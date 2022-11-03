<script lang="ts">
  import Admin from '../components/Admin.svelte'

  const changeSettings = async (e) => {
    e.preventDefault()
    const [shownFirstName, shownLastName, shownUsername] = searchForAll(
      '[data-id="db_values"]'
    )
    const { 0: firstName, 1: lastName, 2: password, 3: submitBtn } = e.target
    empty(submitBtn, () => {
      const loading = createLoadingSpinner()
      loading.style.cssText = `width: 2rem; position: static; transform: translate(0,0);`
      submitBtn.disabled = true
      nestElements(submitBtn, [loading])
    })
    const request = {
      body: JSON.stringify({
        first_name: firstName.value,
        last_name: lastName.value,
        password: password.value
      }),
      headers: {
        'Content-Type': 'application/json'
      },
      method: 'POST'
    }
    const response = await fetch('/admin/settings', request).then((r) =>
      r.json()
    )
    empty(submitBtn, () => {
      submitBtn.disabled = false
      submitBtn.innerText = 'Confirm'
    })
    shownFirstName.innerText = response.first_name
    shownLastName.innerText = response.last_name
    shownUsername.innerText = response.username
    firstName.value = ''
    lastName.value = ''
    password.value = ''
    searchForOne('#session-username').innerText = response.username
  }
</script>

<div id="root">
  <form on:submit={changeSettings} id="user-settings" style="display: none;" />
  <div class="settings" id="search-container">
    <div class="user-info">
      <h2>User Information</h2>
      <div class="user-info-list">
        <h4 class="attr-names">Name</h4>
        <h4 class="attr-values">
          <span data-id="db_values" id="first_name"
            >{current_user['first_name']}</span
          >
          <span data-id="db_values" id="last_name"
            >{current_user['last_name']}</span
          >
        </h4>
        <h4 class="attr-names">Username</h4>
        <h4 data-id="db_values" id="username" class="attr-values">
          {current_user['username']}
        </h4>
        <h4 id="role-header" class="attr-names">Role</h4>
        <h4 data-id="db_values" id="role-value" class="attr-values">
          {current_user['role']}
        </h4>
        <h4 id="password-header" class="attr-names">Change Password</h4>

        <div class="n-names">
          <input
            form="user-settings"
            type="text"
            name="first_name"
            id="n-firstname"
          />

          <input
            form="user-settings"
            type="text"
            name="last_name"
            id="n-lastname"
          />
        </div>

        <!-- <input
              form="user-settings"
              type="text"
              name="username"
              id="n-username"
            /> -->

        <div class="role-request">
          {#if role == 'admin'}
            🔐
          {:else}
            You may request a change in role to an admin.
          {/if}
        </div>

        <input
          form="user-settings"
          type="password"
          name="password"
          id="n-password"
        />

        <button type="submit" form="user-settings">Confirm</button>
      </div>
    </div>
    {#if role == 'admin' || role == 'manager'}
      <!-- <div class="create-user">
        <form
          on:submit={createUser}
          id="new-user-form"
          style="display: none;"
        />
        <h2>Create User</h2>
        <p>
          Provide the credentials for the new user you wish to create. Password
          and username will automatically be assigned, and the user will receive
          these credentials via email.
        </p>
        <div class="new-user-info">
          <h4 class="attr-names">Name</h4>
          <h4 class="attr-names">Email</h4>
          <h4 class="attr-names">Role</h4>
          <div class="n-names">
            <input
              form="new-user-form"
              type="text"
              name="first_name"
              id="n-firstname"
              placeholder="First Name"
            />
            <input
              form="new-user-form"
              type="text"
              name="last_name"
              id="n-lastname"
              placeholder="Last Name"
            />
          </div>
          <input
            form="new-user-form"
            type="text"
            name="email"
            id="n-email"
            placeholder="Email Address"
          />
          <input
            form="new-user-form"
            type="text"
            name="role"
            id="n-role"
            style="display: none;"
          />
          <div
            tabindex="0"
            on:click={showRoleOptions}
            class="select-role-wrapper"
          >
            <p>Select a role</p>
            <div class="role-options" />
          </div>
          <button type="submit" form="new-user-form">Create User</button>
        </div>
      </div>
      <div class="users">
        <h2>Users</h2>
        <div class="user-list" />
      </div> -->
      <Admin />
    {/if}
  </div>
</div>

<style>
  .user-info-list,
  .new-user-info {
    display: grid;
    grid-template-columns: clamp(100px, 30%, 300px) 60%;
    grid-auto-rows: 50px;
    column-gap: 10%;
    align-content: center;
  }

  .attr-names,
  .attr-values {
    grid-column: 1;
  }

  .attr-values {
    justify-self: end;
  }

  #password-header {
    grid-area: 8/1/8/1;
  }

  #role-value {
    grid-area: 6/1/6/1;
  }

  #role-header {
    grid-area: 5/1/5/1;
  }

  .n-names {
    display: flex;
    flex-flow: row nowrap;
    justify-content: space-between;
  }

  .n-names * {
    width: 49%;
  }
  .user-info .n-names {
    grid-area: 2/2/2/2;
  }
  .user-info input:nth-of-type(1) {
    grid-area: 8/2/8/2;
  }
  .user-info .role-request {
    grid-area: 6/2/6/2;
    display: flex;
    align-items: center;
  }
  /* .user-info input:nth-of-type(2) {
  grid-area: 8/2/8/2;
} */

  .user-info button[type='submit'] {
    grid-area: 10/1/10/3;
    justify-self: center;
    width: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .new-user-info .n-names {
    grid-area: 1/2/1/2;
  }

  .new-user-info h4:nth-of-type(1) {
    grid-area: 1/1/1/1;
  }

  .new-user-info h4:nth-of-type(2) {
    grid-area: 3/1/3/1;
  }

  .new-user-info h4:nth-of-type(3) {
    grid-area: 5/1/5/1;
  }

  .new-user-info > input:nth-of-type(1) {
    grid-area: 3/2/3/2;
  }

  .new-user-info button[type='submit'] {
    grid-area: 7/1/7/3;
    justify-self: center;
    width: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  button[type='submit']:disabled {
    background-color: var(--gray);
    cursor: wait;
  }

  .select-role-wrapper {
    position: relative;
    grid-area: 5/2/5/2;
    border-radius: 4px;
    border: 0.5px solid var(--light);
    cursor: pointer;
    display: flex;
    align-items: center;
    padding: 4px;
  }

  .select-role-wrapper:focus {
    outline-style: auto;
  }

  .select-role-wrapper > p {
    font-size: 1.25rem;
  }

  .role-options {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    max-height: 200px;
    transition: max-height 0.2s linear;
    overflow: hidden;
    background-color: var(--light);
    transform: translate(0, 100%);
    padding: 0.25rem;
    box-sizing: border-box;
  }

  .role-options:empty {
    max-height: 0;
    padding: 0;
  }

  .role-options p {
    cursor: pointer;
    position: relative;
  }

  .role-options p:first-of-type {
    margin-top: 0;
  }

  .role-options p:last-of-type {
    margin-bottom: 0;
  }

  .role-options span.underline {
    position: absolute;
    min-width: 0;
    border-bottom: 0.5px solid var(--gray);
    transition: min-width 0.3s linear;
    bottom: 0;
    left: 0;
  }

  .role-options p:hover span.underline {
    min-width: 30%;
  }

  /* .exit-btn {
  height: 20px;
  width: 20px;
  display: flex;
  font-size: 15px;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
} */
</style>
