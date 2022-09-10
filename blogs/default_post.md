# Welcome to Gitblog. 

Gitblog publishes your markdown files as blog posts nice and easy.

## Getting started

1. Clone your Gitblog repo[^1]

    ```console
    $ git clone git@github.com:{owner}/{repo_slug}.git
    ```
   
   ~~double tildes~~

   __bold__

   ==highlight==

   <u>underlined?</u>

   <div style="color: red">you can use HTML</div>
   
   <!-- Comments show up as HTML comments, i.e. not rendered -->

   > Beautiful quotes!
   > 
   > – Right?

   superscript ( x^2 )

   $$ x = a_0 + \frac{1}{\displaystyle a_1 + \frac{1}{\displaystyle a_2 + \frac{1}{\displaystyle a_3 + a_4}}} $$

   ![\Large x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}](https://latex.codecogs.com/svg.latex?\Large&space;x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}{\color{Blue}}) 

   ![title](sealion.png "See Lion!")

   [^1]: Footnotes work!


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



| Syntax       | Description  |     Test Text |
|:-------------|:------------:|--------------:|
| Header       |    Title     |   Here's this |
| Paragraph    |     Text     |      And more |


