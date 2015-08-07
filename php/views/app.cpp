
<!DOCTYPE html>
<html>
    <head>
        <title><?cpp view->content += str(title); ?> - An example blog</title>
    </head>
    <body>
        <?cpp if (show_navigation) { ?>
            <ul id="navigation">
            <?cpp for (menu : item) { ?>
                <li><a href="<?cpp view->content += str(item->href); ?>"><?cpp view->content += str(item->caption); ?></a></li>
            <?cpp } ?>
            </ul>
        <?cpp } ?>

        <h1><?cpp view->content += str(post->title); ?></h1>

        <div class="content">
            <?cpp view->content += str(post->content); ?>
        </div>

    </body>
</html>