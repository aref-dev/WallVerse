<div align="center">
    <h1>WallVerse - Random Topic Based Quotations as Your Wallpaper</h1>
</div>
With WallVerse you can set different chunks of texts as your wallpaper. There is a textbox for adding your own quotations, jokes, or poetry, or you can download and add "Quotation Packs" that cover different topics.
<div align="center">
  <img src="https://github.com/aref-dev/WallVerse/assets/69017077/de77ca54-1088-4a48-985d-b3df50dc4cba" width="450" alt="Your Image Alt Text">
</div>

<!-- PyPI -->



### Output example:
</br>
<div align="center">
    
<img src="https://github.com/aref-dev/WallVerse/assets/69017077/650b1039-cee4-4e09-beee-716eb5b35f37" width="700" alt="Your Image Alt Text">

</div>
</br>

## Features
- Works with Windows, MacOS, and Linux (GNOME)
- Option to start with the OS
- Automatic dark-mode switching
- Different text-color, background-color, or background-image for dark-mode and light-mode
- Adjustable font style and size
- System tray icon
- Refresh wallpaper at set intervals
</br>

## Using the textbox
Different texts need to be seperated with %. Keep in mind that the textbox does not detect escape characters. If you need a newline character, or a tab charcter, simply use tab or enter.
</br>

## Quotation packs
You can find datastore files that contain quotations, jokes, or poetry on GitHub and other sites. But they need to have the following formatting to work with WallVerse:
<pre>
{
    "Name": "Random Rumi", 
    "Description": "Rumi Quotes To Give You A More Positive Outlook On Life",
    "Quotes": ["Raise your words, not voice. It is rain that grows flowers, not thunder.", "The wound is the place where the Light enters you."]
}
</pre>
Unlike the textbox, the Quotes list in the JSON file can detect escape characters.
</br>
If you are using Python, I suggest using textwrap for all elements in your list to limit the width of your quotations.
</br></br></br></br>
