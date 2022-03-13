# Stream Deck Controller

A Linux compatiable software for the Elgato Stream Deck with plugin support.

_________________

<img title="" src="readme_photos/colors.jpg" alt="colors.jpg" width="361">

---

## Installation

    1. Download the latest [release](https://github.com/TriLinder/StreamDeckController/releases)

    2. Uncompress the archive into a new directory

    3. Install all the required modules from `requirements.txt`

    4. Install the `streamdeck` module according to their [documentation](https://python-elgato-streamdeck.readthedocs.io/en/stable/pages/installation.html)

    5. Download a font of your choice and place it into the `fonts` directory

    6. Open `config.json` and modify `font` to the name your font of choice.

    7. Run `main.py`

You should be asked to select your device from a list. If you can't see your device, make sure you installed the `streamdeck` module correctly and consider rebooting.

---

## Demo

If you're using the 15 button Stream Deck (the one in the picture above), you will be presented with a demo. Enjoy!

---

## Troubleshooting

<img title="" src="readme_photos/noFont.jpg" alt="noFont.jpg" width="250">

If you're presented with a screen like this, you haven't installed the font correctly. Please double check that the font file is either a `.ttf` or a `.otf` and its in the correct directory.

Then check that you entered the right name into `config.json`.

If you still can't get your font to work, try another font or create an issue here on GitHub.

---

<img title="" src="readme_photos/invalidLayout.jpg" alt="invalidLayout.jpg" width="250">

This error screen means the page you're trying to load is made for a diffrent Stream Deck model. If you see this on the first start, you're probably not using the 15 button model and so can't use the demo. Don't worry however as you can still use your own profiles as is explained below.

---

## Creating your own profiles

This is the fun part.

‏‏‎ ‎

Under the `pages` directory you can find `empty.json`. Use this as a template for your first page.

```json
{
    "images": ["blank"],
    "ticks": [],
    "dimensions": "5x3",
    "created": 1646871751,

    "buttons": {
    }
}
```

First let's start with editing the `dimensions` key. This is used to determine whether or not a page is suitable for the connected Stream Deck. It's in the simple format of `Width X Hight`, so the 15 button Stream Deck in the pictures above has the dimensions of `5x3`.

‏‏‎ ‎

The `created` key is a [UNIX tiestmap](https://en.wikipedia.org/wiki/Unix_time) and while it's not currenlty used by the progam, I still recomenned setting it as it may be used in a future version.

‏‏‎ ‎

We'll get to the `images` and `ticks` keys later.

‏‏‎ ‎‏‏‎ ‎

### Adding buttons

Now let's add some buttons.

First however let's look at coordinates.

| 0x0 | 1x0 | 2x0 | 3x0 | 4x0 |
|:---:| --- | --- | --- | --- |
| 0x1 | 1x1 | 2x1 | 3x1 | 4x1 |
| 0x2 | 1x2 | 2x2 | 3x2 | 4x2 |

Theese are the coordinates for the 15 button Stream Deck. As you can see the coordinates are in the format of  `x/y` with the top left button being  `0x0`.

‎

You can always bring the coordinates up with the `showCoords` action, which we'll talk about later.

‎

Now that you know how to work with the coordinates, we can add our first button.

This is how our `empty.json` template looks with a new button.

```json
{
    "images": ["blank"],
    "ticks": [],
    "dimensions": "5x3",
    "created": 1646871751,

    "buttons": {
        "0x0" : {"caption":"Hello,\nworld.", "fontSize":12, "color":"white", "fontAlignment":"center", "background":"blank", "actions":{"none":""}}
    }
}
```

Let's examine our button a little closer.

```json
"0x0" : {"caption":"Hello,\nworld.",
        "fontSize":12, 
        "color":"white", 
        "fontAlignment":"center", 
        "background":"blank", 
        "actions":{
                    "none":""
                  }
        }
```

The button is under the key `0x0`,  which you may recognize as coordinates. If we look at the table higher up, we can see that `0x0` corresponds to the top-left corner of our Stream Deck.

‏‏‎ ‎

Here is the explation of the keys you can see in the example:

| **KEY**         | **EXPLANATION**                                                                                                          |
| ---------------:|:------------------------------------------------------------------------------------------------------------------------ |
| `caption`       | The text displayed on the button itself                                                                                  |
| `fontSize`      | The size of the font used to display the caption                                                                         |
| `color`         | is the color of the font. You can either use names like `white` or `blue`, or you can use hex codes like `#2a2a2a`.      |
| `fontAlignment` | Vertical alignment of the font. Can either be `top`, `bottom` or `center`. **This tag is optional.**                     |
| `background`    | The background image of your button, we'll talk about how to add your own images below.                                  |
| `actions`       | Actions to trigger when the button is pressed. You can find more info about `actions` below.                             |
| `ticks`         | Not seen in the example above, this tag is used for plugins which we'll also talk about later. **This tag is optional.** |

‏‏‎ ‎

Now let's run our example. Save the example with a new, unique file name such as `test1.json`

‏‏‎ ‎

Since there's currently no link leading to our file, we'll set the program to start on our page automatically.

‏‏‎ ‎

Let's open up `config.json`, that's located in the same directory as `main.py`, and edit it.

This is how the file looks by default.

```json
{
    "startingPage": "welcome.json",
    "startingBrightness": 75,
    "deviceSerial": "selectOnStartup",
    "font": "yourFont.ttf"
}
```

We'll modify the `startingPage` to our page's file name.  So if you named your file `test1.json`, the modified line will look like this:

```json
"startingPage": "test1.json",
```

Now let's start `main.py` again.

‎

If you've done everything correctly, you should see a simple blank page with `Hello, world.` in the top left.
