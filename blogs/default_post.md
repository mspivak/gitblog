# Welcome to Gitblog. 

Gitblog publishes your markdown files as blog posts nice and easy.

## What just happened?

We just created a repo on your `{owner}` account named `{repo_slug}` to keep the contents of your new 
blog: **{blog_name}**. 

We will be tracking this repo for changes and whenever you add/change/delete a `*.md` file, we'll instantly 
sync those changes with your new blog which new lives at {blog_url}. 


## Getting started

1. Clone your Gitblog repo
      
   Using HTTPS:
   ```console
   $ git clone https://github.com/mspivak/gitblog.git
   ```

   Or if you have your SSH keys set up:
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
    
    At this point, your post is visible only to you on https://gitblog.link/{owner}/{repo_slug}/hello-world.


3. Publish it

    ```console
    $ mv hello-world.md public/hello-world.md
    $ git commit -m 'publishing my first post!'
    $ git push
    ```
    
    That's it! By moving it to the `public/` directory your post is now public!


4. Happy blogging!

    Please report any issues or feed back on https://github.com/mspivak/gitblog/issues


### Publish/Unpublish

All `.md` files on your repo will be treated as separate blog posts. Their name will be turned into a title so 
`my-new-article.md`, `my_new_article.md` and `My New Article.md` will all become 


###
| Syntax       | Description  |     Test Text |
|:-------------|:------------:|--------------:|
| Header       |    Title     |   Here's this |
| Paragraph    |     Text     |      And more |


