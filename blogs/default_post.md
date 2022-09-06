# Welcome to Gitblog. 

Gitblog publishes your markdown files as blog posts nice and easy.

## Getting started

1. Clone your Gitblog repo

    ```console
    $ git clone git@github.com:{owner}/{repo_slug}.git
    ```

2. Create your first post as a sketch

    ```console
    $ echo '# My first post\nHello world!' > hello-world.md
    $ git add .
    $ git commit -m 'my first post (draft)'
    $ git push
    ```
    
    At this point, your post is visible only to you on https://gitblog.link/{owner}/{repo_slug}/hello-world


3. Publish it

    ```console
    $ mv hello-world.md public/hello-world.md
    $ git commit -m 'publishing my first post!'
    $ git push
    ```
    
    That's it! By moving it to the `public/` directory your post is now public!


5. Happy blogging!

    Please report any issues or feed back on https://github.com/mspivak/gitblog/issues

