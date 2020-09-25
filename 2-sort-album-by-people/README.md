## Sort Photos by Persons

A python script which sorts photos accoding to the people's faces.

Motivation: Google Photos' feature of sorting your gallery according to different persons. I tried to implement the same using Python3 and [face_recognition](https://github.com/ageitgey/face_recognition) library.

### Running instructions

**(1/5) Install Python3 on your system.**  
  
**(2/5) Download script.py and requirements.txt**  
  
**(3/5) Collect photos of people to be identified**

People are sorted according to the face photos provided by a user. Find a proper picture of the face of a person to be identified and name it `<person's name>.<jpg|jpeg|png|svg>`

For example, to identify a photo of Harry Potter (Daniel Radcliffe) download [this](https://i1.wp.com/metro.co.uk/wp-content/uploads/2013/06/ay_111335926.jpg) picture and rename it as `daniel.jpg`. All the photos of Daniel could then be found in a folder named `daniel`
  
Collect photos of all the people in the same way and put them in a directory `known` (or any other name will do)
  
[Example](https://github.com/zerefwayne/automation/tree/master/2-sort-album-by-people/known)

**(4/5) Collect photos to be sorted**

Collect all the photos in formats `jpg|jpeg|svg|png` and save them in a directory `photos` (or any other name will do)

[Example](https://github.com/zerefwayne/automation/tree/master/2-sort-album-by-people/photos)

**Directory Structure**

Once all the above instructions have been followed the structure of your folder must look like:

```
.
+-- script.py
+-- requirements.txt
+-- known
+-- photos
```

**(5/5) Final steps**:

1. ```pip3 install -r requirements.txt```
2. ```script.py known photos```

Once all the steps are completed, you can find the photos in directory named `album`.
