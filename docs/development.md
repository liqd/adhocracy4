Setting up development env
==========================

To develop a4, a project using it is needed. To start it is recommended to
checkout [adhocracy-plus](https://github.com/liqd/adhocracy-plus).

Preqrequisites:

- checkout of your A4-project
- virtualenv for your A4-project setup
- your `Requirements.txt` and `package.json` states some adhocracy4 version

Development setup
-----------------

This setup allows you to modify both javascript and python code in the
adhocracy4 core repository and your app at the same time.

Checkout and install adhocracy4 

    git clone git@github.com:liqd/adhocracy4.git
    cd adhocracy4
    make install
    
Activate the virtualenv in both project and adhocracy4. 

    source venv/bin/activate

Ensure that
your `~/.npmrc` contains as `prefix` some location you can write.

    echo "prefix = $HOME/.npmprefix" > ~/.npmrc

Start development mode:

    cd adhocracy4
    npm link

    cd ../$PROJECT
    pip install -e ../adhocracy4/
    npm link adhocracy4

Leave development mode:

    cd $PROJECT
    npm unlink adhocracy4
    npm install
    pip install -r requirements.txt

Local installation
------------------

This setup installs your current state of the python and javascript
application. It will use the packing utils and process, but does not
automatically update if you change somehting on the adhocracy4 code

    cd $PROJECT
    vim package.json # remove adhocracy requirement
    npm install ../adhocracy4
    pip install ../adhocracy4
