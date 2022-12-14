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
   $ git clone https://github.com/{owner}/{repo_slug}.git
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
    
    At this point, your post is visible only to you on https://gitblog.link/blogs/{owner}/{repo_slug}/posts/hello-world.


3. Publish it

    ```console
    $ mv hello-world.md public/hello-world.md
    $ git commit -m 'publishing my first post!'
    $ git push
    ```
    
    That's it! By moving it to the `public/` directory your post is now public!


4. Happy blogging!

    Please report any issues or feed back on https://github.com/mspivak/gitblog/issues


## Publish/Unpublish

All `.md` files on your repo will be treated as separate blog posts. Their name will be turned into a title so 
`my-new-article.md`, `my_new_article.md` and `My New Article.md` will all become My New Article. 

Files on the root `public` directory will be published automatically, those elsewhere will only be readable by you.

## Categories

Moving a file to `public/tech-articles/my-new-article.md` will create the **Tech Articles** category on your blog
and group those on .

## Images

```markdown
![Alt text](path/image.png "Title")
```

The path is relative to your repos root. 
So you can create an `images` directory to place all your images there, but this is not mandatory.
Images includded using this method will be copied to a Gitblog server. If you rather host them yourself, use external links.

## Syntax

Most markdown syntax is available, a little demo:

- You can empasize with *italics* or **bold** using stars.
- Regular HTML works: <a href="https://gitblog.link" target="_blank" style="color: red"><strong>Bold red link</strong></a>
- You can use tables:

   | Item       | Quantity  |    Price |
   |:-----------|:---------:|---------:|
   | Pencil     | 3         | $0.50    |
   | Rubber     | 1         | $0.25    |
   | Notebook   | 2         | $2.00    |

