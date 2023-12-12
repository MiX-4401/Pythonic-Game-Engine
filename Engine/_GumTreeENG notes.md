==================================================================================================
===========================================GumTreeENG=============================================
==================================================================================================

[] TODO:

[]  Lighting
[x]  -> Decide how to manage normal map files
[x]  -> Decide how to associate normal maps with sprites
[x]  -> Associate normal maps with sprites
[]  -> Create new surface layers for normal maps

[]  Graphics
[x] -> Create prototype for replacing pygame surfaces with custom lib
[]  -> Expand on prototype
[]  -> Replace pygame surfaces with custom lib
[]  -> Seperate sprites, surfaces and screen for individual shaders

[]  Misc
[]  -> Internal documentation
[]  -> Sweep the code


===================================================================================================

Notes:
-> Texture Handle Ideas <-
: Have a normal settings file for each normal file which specifies which file is attached to
: Write dir parser where files have 'texture' or 'normal' keywords, joining them

: Expand on sprite parser, attach normal maps to texture spritesheets which some sort of break. 
	Perhaps green (scale) should represent which index of the spritehseet will contain normals

  -> Turns out this was a shit idea

===================================================================================================