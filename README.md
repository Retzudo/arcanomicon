Arcanomicon
===========

[Arcanomicon](https://wow.gamepedia.com/Arcanomicon) is supposed to be
a replacement for popular but overloaded WoW interface websites such as
[wow.curse.com](https://mods.curse.com/addons/wow) or the venerable
[wowinterface.com](http://www.wowinterface.com/addons.php). Arcanomicon
will be entirely open source and solely focused on WoW interface add-ons
and nothing else.

There will be a public API and an open source desktop client for
synchronizing add-ons.


Local Installation
------------------

1. `git clone https://github.com/Retzudo/arcanomicon.git`
2. `cd arcanomicon`
3. `python3 -m venv env`
4. `. env/bin/activate`
5. `pip install -r requirements.txt`
6. `python arcanomicon/manage.py migrate`
7. `python arcanomicon/manage.py createsuperuser`
8. `python arcanomicon/manage.py runserver`
