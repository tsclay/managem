# Welcome to managem!

This `index.html` serves as a placeholder for you to replace with the main entrypoint for your site or app.

If your site or app is to be on a different server, delete the `client` directory altogether, and ensure that your DNS records point a subdomain of your main site/app to your managem backend.

## Two examples

### 1. Different servers

Your main site is `www.example.com`, and it is on a separate server.

You can set a subdomain such as `admin.example.com` to route to the public IP of where your managem backend lives.

### 2. Same servers

If you're hosting a simple website, chances are that you can have your managem backend serve the resources for your website (only an HTML file that would call CSS and JS files from the browser).

Place these assets inside `client/public` and replace this `index.html` with yours.

## Try it out!

Go [here](/admin) and try out the app using the following credentials:

|Username|Password|Role|
|---|---|---|
|jsmith|apples|admin|
|jdoe|apples|curator|

Don't worry about deleting something or adding something. This data is not being used in production.